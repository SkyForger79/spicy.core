import datetime
import gzip
import os
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sitemaps import ping_google
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.db.models.loading import get_model
from math import ceil
from optparse import make_option
from spicy.mediacenter.defaults import MEDIACENTER_ROOT
from spicy.presscenter.defaults import DOC_THUMB_SIZE, CUSTOM_DOCUMENT_MODEL
from spicy.core.service import api
from spicy.core.simplepages.defaults import SIMPLE_PAGE_MODEL
from spicy.core.siteskin import defaults
from spicy.core.siteskin.common import cdata
from cStringIO import StringIO


now = datetime.datetime.now()

SITEMAP = [
    {
        'model': CUSTOM_DOCUMENT_MODEL,
        'filter': {'is_public': True, 'pub_date__lte': now},
        'gen': {
            'loc': lambda x: x.get_absolute_url(),
            'changefreq': 'daily',
            'priority':'0.8'
        },
        'has_media': True,
    },
    {
        'model': SIMPLE_PAGE_MODEL,
        'filter': {'sites__id__exact': settings.SITE_ID},
        'exclude': {'url__startswith': '/test/'},
        'gen': {
            'loc': lambda x: x.get_absolute_url(),
            'changefreq': 'daily',
            'priority': '0.7'
        }
    }]
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S+03:00'
OBJECTS_LIMIT = 20000


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--limit', default=None, help='Limit number of objects'),
    )

    sub_dir = ''
    text_start = (
        u'<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" '
        'xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">')
    text_end = u'</urlset>'
    main_text_start = (
        u'<?xml version="1.0" encoding="UTF-8"?>'
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    main_text_end = u'</sitemapindex>'
    string_cnt = 0
    broken_cnt = 0
    file_i = 1

    sitemap_file = None

    def __init__(self):
        self.file_obj = None
        self.sitemap_dir = os.path.join(MEDIACENTER_ROOT, 'sitemaps')

        if not os.path.exists(self.sitemap_dir):
            try:
                os.mkdir(self.sitemap_dir)
            except Exception:
                print (
                    "Sitemap dir doesn't exist at '%s', unable to create" %
                    self.sitemap_dir)
                raise

        self.sitemap_sub_dir = os.path.join(self.sitemap_dir, self.sub_dir)
        self.domain = Site.objects.get_current().domain
        self.main_sitemap_file_name = '%s/sitemap.xml' % self.sitemap_dir

    def gen_url(self, obj, gen):
        result_gen = {}
        for key, value in gen.iteritems():
            if isinstance(value, basestring):
                result_gen[key] = value
            else:
                try:
                    result_gen[key] = value(obj)
                except Exception, e:
                    print e
                    pass

        locs = result_gen['loc']
        if isinstance(locs, basestring):
            locs = [locs]

        results = []
        for loc in locs:
            if not loc:
                self.broken_cnt += 1
                continue

            self.string_cnt += 1
            data = {}

            data['loc'] = u'<loc>http://%s%s</loc>' % (self.domain, loc)
            lastmod = result_gen.get('lastmod')
            data['lastmod'] = (
                u'<lastmod>%s</lastmod>' % lastmod if lastmod else '')
            data['changefreq'] = u'<changefreq>%s</changefreq>' % result_gen[
                'changefreq']
            data['priority'] = u'<priority>%s</priority>' % result_gen[
                'priority']

            results.append(
                u'<url>%(loc)s%(lastmod)s%(changefreq)s%(priority)s%%s</url>' %
                data)
        return results

    def write(self, string, *data):
        try:
            self.file_obj.write((string % u''.join(data)).encode('utf-8'))
        except Exception:
            print u'Unable to write to file: %s with data %s' % (string, data)
            raise
        # Check if we've reached objects limit.
        if self.string_cnt >= OBJECTS_LIMIT:
            self.string_cnt = 0
            self.change_file()

    def file_close(self):
        self.file_obj.write(self.text_end)

        # Compress with gzip.
        name = '%ssitemap_%s.xml.gz' % (self.sitemap_sub_dir, self.file_i)
        gzip_file = gzip.GzipFile(
            name, 'wb', defaults.SITEMAP_GZIP_COMPRESSION)
        self.file_obj.seek(0)
        for line in self.file_obj:
            gzip_file.write(line)
        gzip_file.close()
        self.main_sitemap_file.write(
            u'<sitemap><loc>http://%s/%ssitemap_%i.xml.gz</loc>'
            '</sitemap>' % (
                self.domain, defaults.SITEMAP_URL.lstrip('/'), self.file_i))

    def file_create(self):
        self.file_obj = StringIO()
        self.file_obj.write(self.text_start)

    def change_file(self):
        self.file_close()
        self.file_i += 1
        self.file_create()

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 1))

        for f in os.listdir(self.sitemap_sub_dir):
            if f.endswith('.xml.gz') and f.startswith('sitemap'):
                os.remove('%s%s' % (self.sitemap_sub_dir, f,))

        self.main_sitemap_file = open(self.main_sitemap_file_name, 'w+')
        self.main_sitemap_file.write(self.main_text_start)
        self.file_create()

        sitemap = SITEMAP
        for import_object in sitemap:
            module, object_model = import_object['model'].split('.')
            model = get_model(module, object_model)
            manager = import_object.get('manager', '_default_manager')
            limit = options.get('limit')
            gen = import_object['gen']
            content_type = ContentType.objects.get_for_model(model)

            query = getattr(model, manager)

            # Get filter params for query.
            filter_params = import_object.get('filter')
            if filter_params:
                query = query.filter(**filter_params)
            else:
                query = query.all()

            # Get exclude params for query.
            exclude_params = import_object.get('exclude')
            if exclude_params:
                query = query.exclude(**exclude_params)

            # Select_related parmas.
            select_related_params = import_object.get('select_related')
            if select_related_params:
                query = query.select_related(*select_related_params)

            only = import_object.get('only')
            if only:
                query = query.only(*only)
            if limit is not None:
                query = query[:int(limit)]
            num_cycles = int(ceil(query.count() / float(OBJECTS_LIMIT)))
            for i in xrange(num_cycles):
                sub_query = query[
                    OBJECTS_LIMIT * i: OBJECTS_LIMIT * (i + 1)]
                if import_object.get('load_thumbs', False):
                    api.register['media'].load_thumbs(
                        sub_query, *DOC_THUMB_SIZE)
                #media_attrs = import_object.get('media_attrs')
                #if media_attrs:
                #    api.register['media'].load_media(sub_query, media_attrs) 
                self.handle_normal(
                    sub_query, gen, content_type, object_model, verbosity)

        self.file_close()
        self.main_sitemap_file.write(self.main_text_end)
        self.main_sitemap_file.close()

        if verbosity > 1 or (self.broken_cnt and verbosity == 1):
            print '%i broken URLs' % self.broken_cnt

        if verbosity > 1:
            from django.db import connection
            #for q in connection.queries[:100]:
            #    print q
            print 'Total queries made: %i' % len(connection.queries)
        ping_google(defaults.SITEMAP_URL + 'sitemap.xml')

    def handle_normal(self, query, gen, content_type, object_model, verbosity):
        thumb_width, thumb_height = DOC_THUMB_SIZE
        for i, data in enumerate(query):
            if verbosity > 1 and i % 1000 == 0:
                print i, '...'
            extras = []
            for url in self.gen_url(data, gen):
                for prov in api.register['media'][data].get_instances(
                        data, view_type__in=('photo', 'video')):
                    title = prov.title or prov.media.title or unicode(prov)
                    desc = prov.desc or prov.media.desc or unicode(prov)

                    if prov.view_type == 'photo':
                        # Image media.
                        extra = (
                            u'<image:loc>http://%s%s</image:loc>' % (
                                self.domain, prov.get_absolute_url()))
                        extra += (
                            u'<image:title>%s</image:title>' % cdata(title))
                        extra += (
                            u'<image:caption>%s</image:caption>' % cdata(desc))

                        extras.append(
                            u'<image:image>%s</image:image>' % extra)
                    elif prov.view_type == 'video':
                        preview = getattr(prov.media, 'preview')
                        preview = preview or prov.consumer.preview
                        thumbnail_url = (
                            preview.get_absolute_url() if preview else None)
                        #thumbnail_url = THUMBNAILS.get_thumbnail(
                        #    thumb_width, thumb_height, data, 'preview', False)
                        # Thumbnails are required by google's standard.
                        if not thumbnail_url:
                            if verbosity > 1:
                                print (
                                    u'Unable to generate video without '
                                    'preview for %s (%s: %s)' %
                                    (data, object_model, data.pk))
                            continue

                        # Video media.
                        extra = (
                            u'<video:thumbnail_loc>http://%s%s'
                            '</video:thumbnail_loc>' % (
                                self.domain, thumbnail_url))

                        extra += u'<video:title>%s</video:title>' % cdata(
                            title or unicode(prov))

                        extra += (
                            u'<video:description>%s</video:description>' %
                            cdata(desc or unicode(prov)))

                        extra += (
                            u'<video:content_loc>http://%s%s'
                            '</video:content_loc>'
                            % (self.domain, prov.get_absolute_url()))

                        extra += (
                            u'<video:publication_date>%s'
                            '</video:publication_date>'
                            % prov.date_joined.strftime(DATETIME_FORMAT))
                        extras.append(u'<video:video>%s</video:video>' % extra)

                self.write(url, u''.join(extras))
