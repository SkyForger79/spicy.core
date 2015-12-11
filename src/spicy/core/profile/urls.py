from django.conf.urls import patterns, url, include
#from django_authopenid import views as oid

public_urls = patterns(
    'spicy.core.profile.views',
    url(r'^login/$', 'signin_or_register', name='signin-or-register'),
    url(r'^signin/$', 'signin', name='signin'),
    url(r'^signup/$', 'signup', name='signup'),
    url(r'^signout/$', 'signout', name='signout'),
    url(r'^success-signup/$', 'success_signup', name='success-signup'),
    url(
        r'^activate/(?P<profile_id>\d+)/(?P<activation_key>\w+)/$', 'activate',
        name='activate'),
    url(r'^set_email/$', 'set_email', name='set_email'),
    url(r'^restore-passwd/$', 'restorepass', name='restorepass'),
    url(r'^user-agreement/$', 'user_agreement', name='user-agreement'),
    url(r'^users/(?P<username>[\w\-_.]+)/$', 'profile', name='index'),
    url(r'^users/(?P<username>[\w\-_.]+)/edit/$', 'edit', name='edit'),
    url(r'^users/(?P<username>[\w\-_.]+)/passwd/$', 'passwd', name='passwd'),
    url(r'^login/widget/$', 'login_widget', name='login-widget'),
    url(
        r'^registration/widget/$', 'registration_widget',
        name='registration-widget'),
    url(r'^checkusername/$', 'check_unic_username', name='check_username'),
)


admin_urls = patterns(
    'spicy.core.profile.admin',
    url(r'^list/$', 'profiles_list', name='index'),
    url(r'^groups/$', 'groups', name='groups'),
    url(r'^groups/create/$', 'create_group', name='create-group'),
    url(r'^groups/(?P<group_id>\d+)/delete/$', 'delete_group',
        name='delete-group'),
    url(r'^create/$', 'create', name='create'),
    url(r'^(?P<profile_id>\d+)/$', 'edit', name='edit'),
    url(r'^(?P<profile_id>\d+)/media/$', 'edit_media', name='edit-media'),
    url(r'^(?P<profile_id>\d+)/delete/$', 'delete', name='delete'),
    url(r'^(?P<profile_id>\d+)/moderate/$', 'moderate', name='moderate'),
    url(r'^(?P<profile_id>\d+)/passwd/$', 'passwd', name='passwd'),
    url(
        r'^(?P<profile_id>\d+)/activation/$', 'resend_activation',
        name='resend-activation'),
    url(
        r'^delete/profile-list/$', 'delete_profile_list',
        name='delete-profile-list'),
    url(r'^profile_autocomplete/(?P<form_input_name>[\w\-]+)/$',
        'profile_autocomplete', name='profile-autocomplete'),
    url(
        r'^profile_autocomplete/(?P<form_input_name>[\w\-]+)/'
        r'(?P<staff>staff)/$',
        'profile_autocomplete', name='profile-autocomplete'),
    url(
        r'^last_created/(?P<form_input_name>[\w\-]+)/$', 'last_created',
        name='last-created'),
    url(
        r'^last_created_staff/(?P<form_input_name>[\w\-]+)/$', 'last_created',
        {'staff_only': True}, 'last-created-staff'),
    url(r'^blacklisted/$', 'blacklisted_ips', name='blacklisted-ips'),
    url(
        r'^blacklisted/delete/$', 'delete_blacklisted_ips',
        name='delete-blacklisted-ips'),
)


urlpatterns = patterns(
    '',
    url(r'^admin/profile/', include(admin_urls, namespace='admin')),
    url(r'^', include(public_urls, namespace='public')),
    url(r'^captcha/', include('captcha.urls')),
)
