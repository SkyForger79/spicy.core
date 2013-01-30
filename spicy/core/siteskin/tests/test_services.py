from django.conf import settings

from django.test import TestCase

from django.core.urlresolvers import reverse

from django.contrib.sites.models import Site
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.webdesign.lorem_ipsum import paragraphs, words

from siteskin.models import Block

from service.api import register
