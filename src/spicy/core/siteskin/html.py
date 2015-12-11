# -*- coding: utf-8 -*-
import html5lib
import re
from xml.sax.saxutils import escape, unescape
from html5lib import sanitizer, treebuilders, treewalkers, serializer


try:
    from html5lib.constants import tokenTypes
    # dirty hack to support both html5lib v0.11 and v0.90
except ImportError:
    # html5lib v 0.11
    tokenTypes = ("StartTag", "EndTag", "EmptyTag",
                  "selfClosing", 'Comment', 'Characters')
    tokenTypes = dict((x, x) for x in tokenTypes)

SAFE_CLASSES = {}


class TokenSanitazer(sanitizer.HTMLSanitizer):
    escape_invalid_tags = False
    
    # only html (not SVG or MathML) elements and attributes
    allowed_elements = sanitizer.HTMLSanitizer.acceptable_elements
    allowed_attributes = sanitizer.HTMLSanitizer.acceptable_attributes
    allowed_classes = SAFE_CLASSES
    
    options = (
        'allowed_elements', 'allowed_attributes', 'allowed_css_properties',
        'allowed_css_keywords', 'allowed_protocols', 'escape_invalid_tags',
        'allowed_classes', 'attr_val_is_uri')
    # names from genshi-like style for backward compatibility
    property_aliases = [
        ('safe_tags', 'allowed_elements'),
        ('safe_attrs', 'allowed_attributes'), ('uri_attrs', 'attr_val_is_uri'),
        ('classes', 'allowed_classes'), ('safe_schemes', 'allowed_protocols')]

    def __init__(self, *args, **kwargs):
        for old, new in self.property_aliases:
            if old in kwargs:
                # XXX write warning
                kwargs[new] = kwargs.pop(old)

        for key in kwargs.keys():
            if key in self.options:
                setattr(self, key, kwargs.pop(key))
            elif key not in (
                    'encoding', 'parseMeta', 'useChardet',
                    'lowercaseElementName', 'lowercaseAttrName'):
                kwargs.pop(key)
        super(TokenSanitazer, self).__init__(*args, **kwargs)
    
    def sanitize_token(self, token):
        if token["type"] in (
                tokenTypes["StartTag"], tokenTypes["EndTag"],
                tokenTypes["EmptyTag"]):
            if token["name"] in self.allowed_elements:
                if 'data' in token:
                    # Copypasted from html5lib
                    attrs = dict(
                        [(name, val) for name, val in token["data"][::-1]
                         if name in self.allowed_attributes])
                    for attr in self.attr_val_is_uri:
                        if not attr in attrs:
                            continue
                        val_unescaped = re.sub(
                            "[`\000-\040\177-\240\s]+", '',
                            unescape(attrs[attr])).lower()
                        # remove replacement characters from unescaped
                        # characters
                        val_unescaped = val_unescaped.replace(u"\ufffd", "")
                        if (
                                re.match(
                                    "^[a-z0-9][-+.a-z0-9]*:", val_unescaped)
                                and (
                                    val_unescaped.split(':')[0] not in
                                    self.allowed_protocols)):
                            del attrs[attr]
                    # end copypasted
                    
                    if 'style' in attrs:
                        styles = self.sanitize_css(attrs.pop('style'))
                        if styles:
                            attrs['style'] = styles
                    if 'class' in attrs:
                        attrs = self.sanitize_classes(token, attrs)
                    token["data"] = [
                        [name, val] for name, val in attrs.items()]
                return token
            elif self.escape_invalid_tags:
                return self.escape_token(token)
        elif token["type"] == tokenTypes["Comment"]:
            pass
        else:
            return token

    def sanitize_classes(self, token, attrs):
        # drop restricted classes
        classes = attrs.pop('class').split()
        if token['name'] in self.allowed_classes:
            allowed = self.allowed_classes[token['name']]
            condition = callable(allowed) and allowed or (
                lambda cls: cls in allowed)
            value = ' '.join(filter(condition, classes))
            if value:
                attrs['class'] = value
        return attrs

    def escape_token(self, token):
        # a part of html5lib sanitize_token method
        if token["type"] == tokenTypes["EndTag"]:
            token["data"] = "</%s>" % token["name"]
        elif token["data"]:
            attrs = ''.join(
                [' %s="%s"' % (k, escape(v)) for k, v in token["data"]])
            token["data"] = "<%s%s>" % (token["name"], attrs)
        else:
            token["data"] = "<%s>" % token["name"]
        if token["type"] == tokenTypes["EmptyTag"]:
            token["data"] = token["data"][:-1] + "/>"
        token["type"] = tokenTypes["Characters"]
        del token["name"]
        return token


class Sanitizer(object):
    dom_callbacks = []
    string_callbacks = []
    method = 'xhtml'
    strip_whitespace = True
    tokensanitazer = TokenSanitazer

    options = (
        'dom_callbacks', 'string_callbacks', 'method', 'strip_whitespace')

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key in self.options:
                setattr(self, key, kwargs.pop(key))
        self.kwargs = kwargs

    def token_sanitizer(self):
        '''Proxy function to pass arguments into Sanitizer constructor'''
        def func(*args, **kwargs):
            kwargs.update(self.kwargs)
            return self.tokensanitazer(*args, **kwargs)
        return func

    def get_dom(self, buf):
        buf = buf.strip()
        if not buf:
            return None
        p = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"),
                                tokenizer=self.token_sanitizer())
        return p.parseFragment(buf)

    def render(self, dom_tree):
        walker = treewalkers.getTreeWalker("dom")
        stream = walker(dom_tree)
        if self.method == "xhtml":
            Serializer = serializer.xhtmlserializer.XHTMLSerializer
        else:
            Serializer = serializer.htmlserializer.HTMLSerializer
        ser = Serializer(
            strip_whitespace=self.strip_whitespace,
            quote_attr_values=True, omit_optional_tags=False)
        return ser.render(stream)

    def sanitize(self, buf):
        '''
            HTML sanitirization with html5lib-like style interface
        '''
        dom_tree = self.get_dom(buf)
        if dom_tree is None:
            return ''

        for callback in self.dom_callbacks:
            dom_tree = callback(dom_tree, **self.kwargs)

        clean = self.render(dom_tree)

        for callback in self.string_callbacks:
            clean = callback(clean, **self.kwargs)

        return unicode(clean)
