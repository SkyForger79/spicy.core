import os
import traceback
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from itertools import chain
from spicy.core.service.utils import MethodDecoratorAdaptor
from spicy.core.siteskin.decorators import render_to, ViewInterface
from spicy.utils import cached_property, load_module
from spicy.utils.models import get_custom_model_class
from spicy.utils.printing import print_error, print_text, print_success, print_warning


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
    """
    Meta URL class used to define dynamic url pattern for class based Provider
    or service views.
    """
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


class ProviderMeta(type):
    """
    Meta Provider class

    class A(Provider):
        @render_to('template.html')
        def view(self, consumer_type, consumer_id)
             return dict()

        @ajax_request
        def view(self, consumer_type, consumer_id)
             return APIResponse()
    """

    # TODO make tests for this meta implementation.
    def __new__(mcs, name, bases, attrs):
        urls = attrs.setdefault('_meta_urls', list())
        for attr, inst in attrs.iteritems():
            render_interface = inst
            if isinstance(inst, MethodDecoratorAdaptor):
                render_interface = inst.func

            if isinstance(render_interface, ViewInterface):
                url_name = '' if attr == '__call__' else ('-' + attr)
                url_pattern_base = r'^%(service_name)s' + url_name
                if inst.url_pattern is None:
                    meta_url = MetaUrl(
                        url_pattern_base +
                        '/(?P<consumer_type>[\w]+)/(?P<consumer_id>[\d]+)/$',
                        inst, attr, is_public=render_interface.is_public)
                else:
                    meta_url = MetaUrl(
                        url_pattern_base + inst.url_pattern, inst, attr,
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
    Provide common views, api methods for defined web-application service.
    Service choose provider instance using own schema.

    provider = api.register['service_name'].get_provider(ConsumerDjangoModel)

    :param model: ManyToMany model for consumer 'app.ModelName'
    :type str:
    """
    __metaclass__ = ProviderMeta
    service = None
    model = 'service.TestProviderModel'

    create_form_mod = None
    form_mod = None

    is_inline = True
    form_template = None

    def __init__(self, service):
        self.service = service
        self.model = get_custom_model_class(self.model)

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

    def get_or_create(self, consumer, **kwargs):        
        """
        Checking if ``self.model`` instance is exists. Creating new instance if does not exists.
        And allways return boolean flag is_created=True id if new instance was created while executing.

        return tuple: is_created, instance
        """
        print_warning(
            'TODO: Deprecated method api.'
            'Returning instace instead tuple of (is_created, instance)')

        instance = self.get_instance(consumer, **kwargs)
        kwargs.pop('_quiet', None)
        return (
            instance if instance is not None else
            self.create_instance(consumer, **kwargs))

    def create_instance(self, consumer, **kwargs):
        ctype = ContentType.objects.get_for_model(consumer)
        return self.model.objects.create(
            consumer_id=consumer.id, consumer_type=ctype, **kwargs)

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
                if not isinstance(consumer, basestring):
                    ctype = ContentType.objects.get_for_model(consumer)
                    print '@Error: dublicates@:', consumer, kwargs, (
                        self.model.objects.filter(
                            consumer_type__model=ctype,
                            consumer_id=consumer.id, **kwargs))
                elif consumer == GENERIC_CONSUMER:
                    print '@Error: dublicates@:', consumer, kwargs, (
                        self.model.objects.filter(**kwargs))

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

        return self.filter(**kwargs)

    @cached_property
    def form(self):
        return load_module(self.form_mod)

    @cached_property
    def create_form(self):
        """Create provider form method

        :return form
        """
        if self.create_form_mod is not None:
            return load_module(self.create_form_mod)
        try:
            return load_module(self.form_mod)
        except AttributeError:
            raise ImproperlyConfigured(
                _("Setup form_mod attributes at first."))

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
            #post_data['%s-service' % prefix] = str(self.service.instance.id)
            post_data['%s-consumer_id' % prefix] = str(consumer.id)
            post_data['%s-consumer_type' % prefix] = str(ctype.id)

            if self.create_form is not None:
                return self.create_form(post_data, prefix=prefix)
            return self.form(post_data, prefix=prefix)

    def edit_inline_form(self, request, consumer, prefix='provider'):
        if request.method == 'POST':
            instance = self.get_instance(consumer)
            return self.form(request.POST, prefix=prefix, instance=instance)

    # TODO Use decorator render_to and ajax_request for tests.
    #@is_staffx
    @render_to('service/admin/service_preview.html', url_pattern='/$')
    def __call__(self, request):
        return {'provider': self}


class BillingProvider(Provider):
    model = None  # 'service.BillingProviderModel'


class Interface(object):
    """
    Service interface

    Service register providers for different type of consumer using
    content_type schema.

    :param stype:
    :type: str
    :param name:
    :type: str
    :param label:
    :type: str

    :param template:
    :type: str
    :param is_default: ???
    :type: str
    """
    stype = None
    name = 'service'
    label = _('Service label')
    schema = dict(GENERIC_CONSUMER=Provider)

    template = None
    is_default = True

    def __init__(self):
        self.__providers = None

        if not isinstance(self.schema, dict):
            raise ProviderSchemaError(
                'Provider schema is not defined correctly.')

        self.is_default = self.is_default

        # initialize all providers
        self.__providers = dict(
            [(ctype, prv(self))
             for ctype, prv in self.schema.iteritems()])

    def print_schema(self):
        return '%s' % self.__providers

    def __getitem__(self, consumer):
        """
        Get provider instance for the defined content_type.

        :param consumer: consumer content_type string
        :type: str or model

        :return : concrete provider for defined consumer
        """
        if not isinstance(consumer, basestring):
            ctype = ContentType.objects.get_for_model(consumer)
            consumer = ctype.model

        if consumer in self.__providers:
            return self.__providers[consumer]
        elif GENERIC_CONSUMER in self.__providers:
            if settings.DEBUG:
                print_text('[{0}] Use GENERIC provider for: {1}'.format(
                        self.name, consumer))
            return self.__providers[GENERIC_CONSUMER]

        raise ProviderSchemaError(
            'Provider is not defined for the ContentType "%s"'
            ' service "%s", schema "%s"'

            % (consumer, self.label, self.schema))

    def create_provider_instance(self, consumer, **kwargs):
        return self[consumer].create_instance(consumer, **kwargs)
        
    def get_provider_instance(self, consumer, **kwargs):
        return self[consumer].get_instance(consumer, **kwargs)

    def get_provider_instances(self, consumer=None, **kwargs):
        if consumer is not None:            
            return self[consumer].get_instances(consumer=consumer, **kwargs)
        elif GENERIC_CONSUMER in self.__providers:            
            return self[GENERIC_CONSUMER].get_instances(**kwargs)

    def get_or_create_provider_instance(self, consumer, **kwargs):
        return self[consumer].get_or_create(consumer, **kwargs)

    def get_provider(self, consumer):
        print_error('Deprecated method Sevice.get_provider(consumer). Use service[consumer] to get prvoder instance.'
                    'For common provider methods use (get|create|get_or_create)_provider_instance|s call.'
                    'Will be deleted in versin Spicy-1.6')
        return self[consumer]

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
        """Default service view.

        dashboard ????

        Use it for something...
        """
        raise NotImplementedError()

    # TODO admin app
    
    def create_url(self):
        return 

    def dashboard(self, request):
        return NotImplementedError()


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
        service = load_module(path_to_srv_interface)

        if not issubclass(service, Interface):
            raise WrongServiceAPI(
                'You must inherit services.Interface at first.')

        # NOT working
        if service.name in self:
            return

        try:
            service_instance = service()
            service_instance[
                'GENERIC_CONSUMER'].model.service = service_instance
            self[service.name] = service_instance
            if settings.DEBUG:
                print_success(
                    'Initialize [%s] service %s compatible with '
                    'consumer_types: %s' % (
                        service.name, service_instance,
                        service_instance.print_schema()))
        except Exception:
            print_error('Error while initialize service %s\n' % service.name)
            print_text(traceback.format_exc())

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

    def __getitem__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            raise ServiceDoesNotExist(name)


register = Register()
