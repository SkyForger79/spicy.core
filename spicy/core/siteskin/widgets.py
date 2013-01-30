from django.conf import settings

from django.db.models import ObjectDoesNotExist

from django import forms
from django.contrib.admin import widgets as admin_widget
from django.core.urlresolvers import reverse, NoReverseMatch
from django.forms.util import flatatt
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.simplejson import JSONEncoder
from django.utils.translation import ugettext
from django.core.validators import EMPTY_VALUES
from django.db import models


### NEW 

class BaseLabledField(forms.Field):
    pass
    #def validate(self, value):
    #    if value == unicode(self.label):
    #        value = None
    #    return super(BaseLabledField, self).validate(value)

class BaseLabledWidget(forms.Widget):
    def get_value_and_attrs(self, name, value, attrs):        
        final_attrs = self.build_attrs(attrs, name=name)
        style = ''
        if 'class' in final_attrs:
            style = '%s ' % final_attrs['class']

        #if value == unicode(self.label):
        #    final_attrs['class'] = style + 'label'
        
        return value, final_attrs



class LabledTextarea(BaseLabledWidget, forms.Textarea):
    def render(self, name, value, attrs=None):
        value, final_attrs = self.get_value_and_attrs(name, value, attrs)        
        value = ''
        if not value in EMPTY_VALUES: 
            value = conditional_escape(force_unicode(value))
        else:
            final_attrs['placeholder'] = self.label
        return mark_safe(u'<textarea%s>%s</textarea>' % 
                         (flatatt(final_attrs),
                          value)
                         )               

class LabledTextInput(BaseLabledWidget, forms.TextInput):
    def render(self, name, value, attrs=None):
        value, final_attrs = self.get_value_and_attrs(name, value, attrs)
        final_attrs['placeholder'] = self.label

        if not value in EMPTY_VALUES: 
            final_attrs['value'] = force_unicode(self._format_value(value))                        
        return mark_safe(u'<input%s type="text"/>' % flatatt(final_attrs))


class LabledCharField(BaseLabledField, forms.CharField):
    widget = LabledTextInput

    def __init__(self, *args, **kwargs):
        super(LabledCharField, self).__init__(*args, **kwargs)
        self.widget.label = self.label


class LabledTextField(BaseLabledField, forms.CharField):
    widget = LabledTextarea

    def __init__(self, *args, **kwargs):
        super(LabledTextField, self).__init__(*args, **kwargs)
        self.widget.label = self.label


class LabledRegexField(BaseLabledField, forms.RegexField):
    widget = LabledTextInput

    def __init__(self, *args, **kwargs):
        super(LabledRegexField, self).__init__(*args, **kwargs)
        self.widget.label = self.label


class LabledEmailField(BaseLabledField, forms.EmailField):
    widget = LabledTextInput

    def __init__(self, *args, **kwargs):
        super(LabledEmailField, self).__init__(*args, **kwargs)
        self.widget.label = self.label



class AutoCompleteModelSelect(forms.Select):
    tmpl = '''<input %(style)s id="id_input_%(name)s" type="text" placeholder="%(label)s">
    <input name="%(name)s" id="id_%(name)s" type='hidden' value="%(value)s">'''

    def render(self, name, value, attrs=None, choices=()):
        attrs = self.build_attrs(attrs, name=name)
        style = 'class="label"'

        try:
            value = self.choices.queryset.get(pk=value)
        except (ObjectDoesNotExist, ValueError):
            label = self.label

            if not value in EMPTY_VALUES and \
                    not (value == unicode(self.label)):
                label = value
                style = ''

            html = self.tmpl % dict(
                style=style,
                name=name,
                label=escape(unicode(label)),
                value='')
        else:
            html = self.tmpl % dict(
                style='',
                name=name,
                label=escape(unicode(value)),
                value=escape(force_unicode(value.pk)))
        return mark_safe(html)


class AutocompleteGenericModelField(forms.ModelChoiceField):
    widget = AutoCompleteModelSelect

    def __init__(self, *args, **kwargs):
        super(AutocompleteGenericModelField, self).__init__(*args, **kwargs)
        self.widget.label = self.label

    def to_python(self, value):
        if value in EMPTY_VALUES or (value == unicode(self.label)):
            return None
        try:
            key = self.to_field_name or 'pk'
            value = self.queryset.get(**{key: value})
        except self.queryset.model.DoesNotExist:
            raise forms.ValidationError(self.error_messages['invalid_choice'])
        except ValueError:
            # Hack
            # required for creating new instance in the form validation method
            pass
        return value



# OLD


class AutoCompleteChooser(forms.Select):
    txt = '''<input type="button" name="%(name_all)s" id="%(name_value)s_input" value="%(text)s">
             <div id="%(name_value)s_hidden_data">
                 <input type="hidden" value="%(value)s" name="%(name_value)s">
             </div>
          '''
    def render(self, name, value, attrs=None, choices=()):
        prefix= ''
        # XXX remove 
        #prefix = (name.split('-', 1)[0] if '-' in name else '')
        fmtdict = dict(name_all=prefix + '-text',
                       name_text=prefix + '-text' if prefix else 'text',
                       name_value=name, text='')

        try:
            value = self.choices.queryset.get(pk=value)
        except ObjectDoesNotExist:
            text = '''<input type="button" name="%(name_all)s" id="%(name_value)s_input" value="%(text)s">
                      <div id="%(name_value)s_hidden_data"></div>''' % fmtdict
        else:
            text = self.txt % dict(
                fmtdict,
                text=escape(unicode(value)),
                value=escape(force_unicode(value.pk)))
        return mark_safe(text)



class FilteredSelectMultiple(admin_widget.FilteredSelectMultiple):
    class Media:
        extend = False
        js = (settings.MEDIA_URL + "js/lib/SelectBox/core.js",
              settings.MEDIA_URL + "js/lib/SelectBox/SelectBox.js",
              settings.MEDIA_URL + "js/lib/SelectBox/SelectFilter2.js"
              )


class Autocomplete(forms.TextInput):
    class Media:
        css = {
            'all': ('css/jquery.autocomplete.css', 'css/thickbox.css'),
            }
        js = ('js/jquery.ajaxQueue.js',
              'js/jquery.bgiframe.min.js',
              'js/jquery.autocomplete.js')

    def __init__(self, callback, options={}, attrs={}, 
                 choices=(), fk_field_name=None):
        self.fk_field_name = fk_field_name
        self.options = None
        self.callback = callback
        self.attrs = {'autocomplete': 'off'}
        if len(options) > 0:
            self.options = JSONEncoder().encode(options)
        self.attrs.update(attrs)
        self.choices = list(choices)
    
    def value_from_datadict(self, data, files, name):
        if self.fk_field_name is not None:
            return data.get(name + '_id', None)
        return data.get(name, None)

    def render(self, name, value, attrs=None, choices=()):
        final_attrs = self.build_attrs(attrs, name=name)

        if isinstance(value, models.Model):
            output = ['<input type="text" %s value="%s"/>'
                      %(flatatt(final_attrs), getattr(value, self.fk_field_name))]
        else:
            output = ['<input type="text" %s/>'%flatatt(final_attrs)]

        options = self.render_options(choices, value, attrs['id'], name)
        output.append(options)
        return mark_safe(u'\n'.join(output))

    def render_options(self, choices, selected_choice, field_id, name):
        if isinstance(self.callback, list):
            callback = JSONEncoder().encode(self.callback)
        elif isinstance(self.callback, basestring):
            try:
                callback = reverse(self.callback)
            except NoReverseMatch:
                callback = escape(self.callback)
            callback = "'%s'" % callback
        else:
            raise ValueError, callback

        options = ''
        if self.options: options += '%s' % self.options

        output = [u'<script type="text/javascript">']
        output.append(u'var userFieldOptions = %s;' % options) # XXX rename
        output.append(u'var userFieldCallback = %s;' % callback) 
        output.append(u'$("#%s").autocomplete(userFieldCallback, userFieldOptions);'%field_id)
        
        if self.fk_field_name is not None:
             output.append(
                 u'$("#%s").result(function(event, data, formatted){$("#%s" + "_id").val(data[1]);});'%(field_id, field_id))
             output.append(u'</script>')
             value = selected_choice
             if isinstance(selected_choice, models.Model):
                 value = selected_choice.id
             output.append(
                 u'<input id="%s_id" type="hidden" name="%s_id" value="%s"/>' 
                 % (field_id, name, value))
        else:
             output.append(u'</script>')
        return u'\n'.join(output)
 

class ModelChoiceAutocompleteField(forms.ModelChoiceField):
    widget = Autocomplete

    def __init__(self, queryset, callback, options={}, attrs={},
                 empty_label=u"---------", cache_choices=False,
                 required=True, widget=None, label=None, 
                 initial=None, help_text=None, to_field_name=None, 
                 fk_field_name=None, *args, **kwargs):

        #choices = choices or self.choices
        widget = widget or self.widget
        fk_field_name = fk_field_name or \
            queryset.model._meta.object_name.lower()
        initial = initial
        if isinstance(widget, type):
            widget = widget(callback, options, attrs, 
                            fk_field_name=fk_field_name)
        super(ModelChoiceAutocompleteField, 
              self).__init__(queryset, empty_label=empty_label, 
                             cache_choices=cache_choices,
                             required=required, widget=widget, label=label, 
                             initial=initial, help_text=help_text, 
                             to_field_name=to_field_name, *args, **kwargs)


class DatePicker(forms.TextInput):
    def __init__(self, options={}, attrs={}):
        self.options = JSONEncoder().encode(options)
        self.attrs = attrs

    def render_js(self, field_id):
        return u'''<script type="text/javascript">
        $('#%s').datepicker(%s);</script>''' % (field_id, self.options)
    
    def render(self, name, value=None, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(super(DatePicker, self).render(name, value, attrs) + \
               self.render_js(final_attrs['id']))

class DateTimePicker(forms.TextInput):
    def __init__(self, options={}, attrs={}):
        self.options = JSONEncoder().encode(options)
        self.attrs = attrs

    def render_js(self, field_id):
        return u'''<script type="text/javascript">
        $('#%s').datepicker(%s);</script>''' % (field_id, self.options)
    
    def render(self, name, value=None, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(super(DatePicker, self).render(name, value, attrs) + \
               self.render_js(final_attrs['id']))


class Spinner(forms.TextInput):
    
    class Media:
        css = {
            'all': ('css/ui.spinner.css',),
            }
        js = ('js/jquery.mousewheel.js',
              'js/ui.spinner.js',)
    
    def __init__(self, options={}, attrs={}):
        self.options = JSONEncoder().encode(options)
        self.attrs = attrs

    def render_js(self, field_id):
        return u'''<script type="text/javascript">var priorityFieldOptions = %(options)s;
            $(function(){$('#%(id)s').spinner(priorityFieldOptions);});</script>''' % {"options":self.options, "id":field_id}
    
    def render(self, name, value=None, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(super(Spinner, self).render(name, value, attrs) + \
               self.render_js(final_attrs['id']))


class CustomNullBooleanSelect(forms.NullBooleanSelect):
    def __init__(self, attrs=None, choices=None):
        current_choices = {
            None: ugettext('Unknown'), True: ugettext('Yes'),
            False: ugettext('No')}
        if choices:
            current_choices.update(choices)
        choices = (
            (u'1', current_choices[None]), (u'2', current_choices[True]),
            (u'3', current_choices[False]))
        super(forms.NullBooleanSelect, self).__init__(attrs, choices)
