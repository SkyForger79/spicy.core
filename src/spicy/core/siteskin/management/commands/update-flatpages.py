# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.flatpages import models

from spicy.core.siteskin.defaults import SITESKIN


class CommandFailed(OSError):
    pass

all_sites = Site.objects.all()
current_site = Site.objects.get_current()


class Command(BaseCommand):
    def handle(self, app='', *args, **options):
        # deleting all old flatpages
        #models.FlatPage.objects.all().delete()
 
        print "  SCANNING FLATPAGES FOR SITESKIN: %s" % SITESKIN
        base_dir = "%s/flatpages" % SITESKIN
        path = os.path.join(settings.TEMPLATE_DIRS[0], base_dir)
        if os.path.isdir(path):
            for filename in os.listdir(path):
                self.install_flatpage(filename, site=current_site,
                                      base_dir='flatpages')

        base_dir = "%s/flatpages/test" % SITESKIN
        path = os.path.join(settings.TEMPLATE_DIRS[0], base_dir)
        print "    TEST PAGES:"
        if os.path.isdir(path):
            for filename in os.listdir(path):
                self.install_flatpage(filename, site=current_site, test=True, 
                                      base_dir='flatpages/test')


    def install_flatpage(self, filename, site=None, test=False,
                         base_dir='flatpages'):
        if not filename.endswith('.html'):
            return

        splitted = filename.split('.')
        basename = '.'.join(splitted[:-1])
        baseurl = '/'.join(splitted[:-1])
        #extension = splitted[-1]

        url = ("/test/%s/" % baseurl) if test else ('/%s/' % baseurl)
        print filename, ' --> ', url

        page, page_exists = models.FlatPage.objects.get_or_create(
            title=basename, url=url,
            content="autocreated", enable_comments=True, registration_required=False,
            template_name="%s/%s"%(base_dir, filename))

        page.sites = [site] if (site is not None) else all_sites

