import os
import sys
from itertools import chain
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.utils import DatabaseError
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django.core.management.color import color_style
from spicy.core.service.forms import ServiceForm, BillingProviderForm
from spicy.core.service.utils import MethodDecoratorAdaptor
from spicy.core.siteskin.decorators import render_to, ViewInterface
from spicy.utils import cached_property, load_module


style = color_style()

GENERIC_CONSUMER = 'GENERIC_CONSUMER'
TEXT_INCLUDE_TEMPLATE = "[inc pk='%s' service='%s']"


class WrongServiceAPI(Exception):
    "Your service must inherit ServiceInterface."


class ServiceDoesNotExist(Exception):
    "Your service must inherit ServiceInterface."


class ProviderSchemaError(Exception):
    "Schema is wrong or not defined."


class ProviderMetaUrlError(Exception):
    pass


class MetaUrl:
    is_public = False

    def __init__(self, pattern, method, name, is_public=False):
        self.pattern = pattern
        self.method = method
        self.name = name
        self.is_public = is_public

    def __iter__(self):
        return iter((self.pattern, self.method, self.name, self.is_public))

    def __eq__(self, other_url):
        return (
            self.pattern == other_url.pattern and
            self.name != other_url.name)

    def __repr__(self):
        return '<%s :: url[%s]>' % (self.name, self.pattern)


# TODO make tests for this meta implementation.
class ProviderMeta(type):
    def __new__(mcs, name, bases, attrs):
        urls = attrs.setdefault('_meta_urls', list())
        for name, inst in attrs.iteritems():
            render_interface = inst
            if isinstance(inst, MethodDecoratorAdaptor):
                render_interface = inst.func

            if isinstance(render_interface, ViewInterface):
                url_name = '-' + name
                if name == '__call__':
                    url_name = ''
                url_pattern_base = r'^%(service_name)s' + url_name
                meta_url = MetaUrl(
                    url_pattern_base +
                    '/(?P<consumer_type>[\w]+)/(?P<consumer_id>[\d]+)/$', inst,
                    name, is_public=render_interface.is_public)
                if inst.url_pattern is not None:
                    meta_url = MetaUrl(
                        url_pattern_base + inst.url_pattern, inst, name,
                        is_public=render_interface.is_public)

                if urls.count(meta_url):
                    raise ProviderMetaUrlError(
                        "You defined the same url pattern for the different "
                        "provider's views. %s, %s" % (meta_url, urls))
                else:
                    urls.append(meta_url)

        return super(ProviderMeta, mcs).__new__(mcs, name, bases, attrs)


class Provider(object):
    """
    @settings - Singleton with predefined settings.
    """
    __metaclass__ = ProviderMeta
    service = None
    model = 'service.models.ProviderTestCaseModel' # TODO refactoring using get_custom_model_class

    create_form_mod = None
    form_mod = None

    is_inline = True
    form_template = None

    @cached_property
    def form(self):
        return self.load_module(self.form_mod)

    @cached_property
    def create_form(self):
        if self.create_form_mod is not None:
            return self.load_module(self.create_form_mod)
        try:
            return self.load_module(self.form_mod)
        except AttributeError:
            raise ImproperlyConfigured(
                _("Setup form_mod attributes at first."))

    def __init__(self, service):
        self.service = service

        self.urls = []
        for meta_url in self._meta_urls:
            pattern, method, name, is_public = meta_url
            if name == '__call__':
                name = service.name
            else:
                name = service.name + '-' + name

            if isinstance(method, MethodDecoratorAdaptor):
                method.func.set_instance(self)
            else:
                method.set_instance(self)
            self.urls.append((
                    url(pattern % {'service_name': service.name}, method,
                        name=name),
                    is_public))

    def load_module(self, path):
        # XXX
        return load_module(path, config='Provider __class__ configuration.')

    def get_or_create(self, consumer, **kwargs):
        instance = self.get_instance(consumer, **kwargs)
        return (
            instance if instance is not None else
            self.create_instance(consumer, **kwargs))

    def create_instance(self, consumer, **kwargs):
        ctype = ContentType.objects.get_for_model(consumer)
        return self.model.objects.create(
            service=self.service.instance, consumer_id=consumer.id,
            consumer_type=ctype, **kwargs)

    def get_instance(self, consumer, **kwargs):
        is_quiet = kwargs.pop('_quiet', False)
        try:
            if not isinstance(consumer, basestring):
                ctype = ContentType.objects.get_for_model(consumer)
                return self.model.objects.get(
                    consumer_type=ctype, consumer_id=consumer.id, **kwargs)

            elif consumer == GENERIC_CONSUMER:
                return self.model.objects.get(**kwargs)

        except self.model.MultipleObjectsReturned:
            # XXX, required for xtag service debugging.
            # dublications delete then, open consumer(document) for editing.
            if not is_quiet:
                ctype = ContentType.objects.get_for_model(consumer)
                print '@Error: dublicates@:', consumer, kwargs, (
                    self.model.objects.filter(
                        consumer_type__model=ctype, consumer_id=consumer.id,
                        **kwargs))

        except self.model.DoesNotExist:
            if not is_quiet:
                print '@Error: instance not found:', consumer, kwargs

    def filter(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def get_instances(self, consumer=None, **kwargs):
        if consumer is not None:
            if isinstance(consumer, basestring):
                kwargs['consumer_type__model'] = consumer
            else:
                ctype = ContentType.objects.get_for_model(consumer)
                kwargs['consumer_type'] = ctype
                kwargs['consumer_id'] = consumer.id

        return self.model.objects.filter(**kwargs)

    def inline_formset(self, request, consumer, prefix='provider'):
        raise NotImplemented()

    def create(self, request):
        # XXX DEPRECATED
        return {'form': (self.create_form or self.form)(prefix='provider')}

    def create_inline_form(self, request, consumer, prefix='provider'):
        post_data = request.POST.copy()

        if request.method == 'POST':
            ctype = ContentType.objects.get_for_model(consumer)

            # XXX REFACTORING
            post_data['%s-service' % prefix] = str(self.service.instance.id)
            post_data['%s-consumer_id' % prefix] = str(consumer.id)
            post_data['%s-consumer_type' % prefix] = str(ctype.id)

            if self.create_form is not None:
                return self.create_form(post_data, prefix=prefix)
            return self.form(post_data, prefix=prefix)

    def edit_inline_form(self, request, consumer, prefix='provider'):
        if request.method == 'POST':
            instance = self.get_instance(consumer)
            return self.form(request.POST, prefix=prefix, instance=instance)
#         # XXX
#         if request.method == 'POST':
#             form = self.form(request.POST, instance=provider.instance)
#             if form.is_valid():
#                 form.save()
#             else:
#                 print '@@@###', form.errors
#         return provider

    # TODO Use decorator render_to and ajax_request for tests.
    #@is_staffx
    @render_to('service/admin/service_preview.html', url_pattern='/$')
    def __call__(self, request):
        return {'provider': self}


class BillingProvider(Provider):
    model = 'spicy.core.service.models.BillingProviderModel'
    form = BillingProviderForm
    form_template = 'services/admin/billed_service_form.html'


# TODO
class Schema(object):
    pass


class Interface(object):
    """
    @stype: service type - character
    @name:
    @label:
    @model: 'app.models.Model'
    @form:
    @provider_schema:
        Multi provider (example):
            provider_schema = dict(
                consumer_content_type_name=ProviderClassOne,
                consumer_content_type_name=ProviderClassTwo,
                GENERIC_CONSUMER=ProviderClass
            )
    def get(...)
    """
    stype = None
    name = 'service'
    label = _('Service title')
    provider_schema = Provider
    model = 'spicy.core.service.models.Service'
    form = ServiceForm
    create_template = None
    template = create_template
    is_default = True
    has_rss = False

    @transaction.commit_on_success
    def __init__(self):
        self.__providers = None
        self.instance = None

        if not isinstance(self.provider_schema, dict):
            raise ProviderSchemaError(
                'Provider schema is not defined correctly.')
        self.model = load_module(self.model)

        self.instance, created = self.model.objects.get_or_create(
            name=self.name)

        self.is_default = self.is_default
        self.instance.save()

        # TODO is service form required?
        self.form = self.form(instance=self.instance)
        self.__providers = dict(
            [(ctype, prv(self))
             for ctype, prv in self.provider_schema.iteritems()])

    def __getitem__(self, ctype):
        """Get provider instance for the content_type.
        """
        if ctype in self.__providers:
            return self.__providers[ctype]
        elif GENERIC_CONSUMER in self.__providers:
            return self.__providers[GENERIC_CONSUMER]

        raise ProviderSchemaError(
            'Provider is not defined for the ContentType "%s"'
            ' service "%s", schema "%s"'
            % (ctype, self.label, self.provider_schema))

    def get_provider(self, consumer):
        """
        Get provider instance for the consumer.

        @return: Return tuple result defined for the consumer
            tuple(provider_instance, consumer_content_type)
        """
        if not isinstance(consumer, basestring):
            ctype = ContentType.objects.get_for_model(consumer)
            consumer = ctype.model

        if consumer in self.__providers:
            return self[consumer]
        elif GENERIC_CONSUMER in self.__providers:
            return self[GENERIC_CONSUMER]

        raise ProviderSchemaError(
            'Provider is not defined for the ContentType "%s"'
            ' service "%s", schema "%s"'
            % (consumer, self.label, self.provider_schema))

    def urls(self, is_public=False):
        return [
            [url for url, is_pub in prv.urls if is_pub == is_public]
            for prv in self.__providers.itervalues()]

    @property
    def content_templates(self):
        templates = [
            (tmpl, tmpl) for tmpl in os.listdir(
                settings.TEMPLATE_DIRS[0] + self.PROVIDER_TEMPLATES_DIR)]
        templates.sort()
        return templates

    # TODO default documentation view for the service
    # register it like a request controller
    # service:admin:service_name
    # or use for public
    def __call__(self, request):
        raise NotImplementedError()

    def remove(self, consumer):
        raise NotImplemented

    def enable_site(self, site):
        self.instance.site.add(site)

    def disable_site(self, site):
        self.instance.site.remove(site)

    def get_sites(self):
        return self.instance.site.all()

    def is_free(self):
        return self.instance.is_free()

    def __unicode__(self):
        return unicode(self.label)
    __str__ = __unicode__


class ServiceList(object):
    def __init__(self, services):
        self.services = set(services)

    def free(self):
        return set(filter(lambda srv: srv.is_free(), self.services))

    def prepaid(self):
        return self.services ^ self.free()

    def with_statistic(self):
        return set(
            [srv for srv in self.services if hasattr(srv, 'statistic_types')])

    def __iter__(self):
        return iter(self.services)


class Register(dict):
    _instance = None
    # TODO. singleton for dict

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Register, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def add(self, path_to_srv_interface):
        interface = load_module(path_to_srv_interface)
        if not issubclass(interface, Interface):
            raise WrongServiceAPI(
                'You must inherit services.Interface at first.')

        # NOT working
        if interface.name in self:
            return

        try:
            self[interface.name] = interface()
        except DatabaseError:
            sys.stderr.write(
                style.ERROR(
                    'Sync database before using service applications.\n'
                    'Can not create service interface "%s"\n' %
                    interface.name))
            transaction.rollback()

    def urls(self, is_public=False):
        # What follows below is not LISP :-P
        return patterns(
            '',
            *chain(*(chain(*(srv.urls(is_public=is_public)
                             for srv in self.get_list())))))

    def remove(self, service_name):
        try:
            del self[service_name]
            self.get_list()

        except KeyError:
            raise ServiceDoesNotExist(service_name)

    def get_list(self, consumer=None, stype=None):
        if consumer is not None:
            # TODO
            # filter services there specific consumer provider are defined
            pass

        return ServiceList(
            self.values() if stype is None else
            [srv for srv in self.itervalues() if srv.stype == stype])

    #return ServiceList(services)

    @cached_property
    def srv_instances(self):
        from spicy.core.service.models import Service
        return Service.objects.all()

    def __getitem__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            raise ServiceDoesNotExist(name)


register = Register()
