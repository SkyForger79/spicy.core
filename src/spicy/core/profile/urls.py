from django.conf.urls import patterns, url, include
#from django_authopenid import views as oid

public_urls = patterns(
    'spicy.core.profile.views',    

    # done
    url(r'^signin/$', 'signin', name='signin'),
    url(r'^signup/$', 'signup', name='signup'),
    url(r'^signout/$', 'signout', name='signout'),
    url(r'^email-notify/$', 'email_notify', name='email-notify'),
    url(r'^activate/(?P<profile_id>\d+)/(?P<activation_key>\w+)/$', 'activate', name='activate'),  
    url(r'^restore-passwd/$', 'restorepass', name='restorepass'),
    url(r'^user-agreement/$', 'user_agreement', name='user-agreement'),

    # refactoring required
    url(r'^users/(?P<username>[\w\-_.]+)/$', 'profile', name='index'),
    url(r'^users/(?P<username>[\w\-_.]+)/edit/$', 'edit', name='edit'),

    # settings
    url(r'^users/(?P<username>[\w\-_.]+)/settings/$', 'user_settings',
        name='settings'),
    url(r'^users/(?P<username>[\w\-_.]+)/passwd/$', 'passwd', name='passwd'),

    url(r'^login/widget/$', 'login_widget', name='login-widget'),
    url(r'^registration/widget/$', 'registration_widget', name='registration-widget'),



    # XXX ???
    url(r'^set_email/$', 'set_email', name='set_email'),

    url(r'^checkusername/$', 'check_unic_username', name='check_username'),


    # django-social-auth.
	#    url(r'^signin/social/new_user/$', 'new_social_user',
    #    name='socialauth_new_user'),
#    url(r'^signin/social/complete/(?P<backend>[\w-]+)/$', 'socialauth_complete',
#        name='socialauth_complete'),
    #url(r'^signin/social/begin/(?P<backend>[\w-]+)/$', 'signin_social',
    #    name='signin_social'),
    #url(r'^signin/social/',
    #    include('social_auth.urls', namespace='social-auth')),
)


#     url(r'^password/reset/$', auth_views.password_reset,  name='auth_password_reset'),
#     url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
#         auth_views.password_reset_confirm,
#         name='auth_password_reset_confirm'),
#     url(r'^password/reset/complete/$',
#         auth_views.password_reset_complete,
#         name='auth_password_reset_complete'),
#     url(r'^password/reset/done/$',
#         auth_views.password_reset_done,
#         name='auth_password_reset_done'),
#     url(r'^password/$',oid_views.password_change, name='auth_password_change'),


# XXX
from django.contrib.auth.models import User
info_dict = {'queryset': User.objects.all(), 'search_by': 'username'}

admin_urls = patterns(
    'spicy.core.profile.admin',
    url(r'^list/$', 'profiles_list', name='index'),
    url(r'^groups/$', 'groups', name='groups'),
    url(r'^groups/create/$', 'create_group', name='create-group'),
    url(r'^groups/(?P<group_id>\d+)/delete/$', 'delete_group',
        name='delete-group'),
    url(r'^create/$', 'create', name='create'),
    #url(r'^role-sequences/$', 'create', name='create'),
    #url(r'^changepass/$', 'changepass', name='changepass'),
    url(r'^(?P<profile_id>\d+)/$', 'edit', name='edit'),
    url(r'^(?P<profile_id>\d+)/moderate/$', 'moderate', name='moderate'),
    url(r'^(?P<profile_id>\d+)/passwd/$', 'passwd', name='passwd'),
    url(r'^(?P<profile_id>\d+)/activation/$', 'resend_activation',
        name='resend-activation'),
    url(r'^delete/profile-list/$', 'delete_profile_list', name='delete-profile-list'),

    url(r'^profile_autocomplete/(?P<form_input_name>[\w\-]+)/$',
        'profile_autocomplete', name='profile-autocomplete'),
    url(r'^profile_autocomplete/(?P<form_input_name>[\w\-]+)/(?P<staff>staff)/$',
        'profile_autocomplete', name='profile-autocomplete'),

    url(r'^last_created/(?P<form_input_name>[\w\-]+)/$', 'last_created',
        name='last-created'),
    url(r'^last_created_staff/(?P<form_input_name>[\w\-]+)/$', 'last_created',
        {'staff_only': True}, 'last-created-staff'),
    url(r'^blacklisted/$', 'blacklisted_ips', name='blacklisted-ips'),
    url(r'^blacklisted/delete/$', 'delete_blacklisted_ips',
        name='delete-blacklisted-ips'),
    )


urlpatterns = patterns('',)
urlpatterns += patterns(
    '', 
    url(r'^admin/profile/', include(admin_urls, namespace='admin')),
    url(r'^', include(public_urls, namespace='public')),

    url(r'^captcha/', include('captcha.urls')),
    )
