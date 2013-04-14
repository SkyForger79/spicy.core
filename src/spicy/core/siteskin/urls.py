from django.conf.urls import patterns, url, include

from . import defaults

public_urls = patterns(
    '',
    url(r'^$', defaults.SITESKIN_INDEX_VIEW,
        {'template': 'index.html', 'page_slug': 'index'},
        name='index'),
)

public_urls += patterns(
    'spicy.core.siteskin.views',

    url(r'^robots.txt$', 'render',
        {'template': 'robots.txt', 'mimetype': 'text/plain'},
        name='robots.txt'),

)

admin_urls = patterns(
    'spicy.core.siteskin.admin',
    url(r'^list/$', 'block_list', name='index'),
    url(r'^create/(?P<content_service_name>[-\w]+)/$', 'create',
        name='create'),
    url(r'^edit/(?P<block_id>[-\d]+)/$', 'edit', name='edit'),
    url(r'^edit/(?P<slug>[-\w_]+)/$', 'edit_by_slug', name='edit_by_slug'),
    url(r'^delete/(?P<block_id>[-\d]+)/$', 'delete', name='delete'),
    url(r'^delete/block-list/$', 'delete_block_list',
        name='delete-block-list'),
    url(r'^deleted/$', 'deleted', name='deleted-in-dialog'),
    url(r'^is-deleted/$', 'is_deleted', name='is-deleted'),
    url(r'^create_rss/$', 'create_rss', name='create_rss')
    )


urlpatterns = patterns('',)
if defaults.USE_CUSTOM_ADMIN:
    urlpatterns += patterns(
        '',
        url(r'^admin/siteskin/', include(admin_urls, namespace='admin')),
)

urlpatterns += patterns(
    '',
    url(r'^', include(public_urls, namespace='public')),
    )
