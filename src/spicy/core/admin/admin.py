from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from spicy.core.service import api
from spicy.core.siteskin.decorators import render_to, ajax_request
from spicy.utils.models import get_custom_model_class
from spicy.core.profile.decorators import is_staff

from .conf import AdminAppBase, AdminLink, Perms
from . import defaults, forms


SettingsModel = get_custom_model_class(defaults.ADMIN_CUSTOM_SETTINGS_MODEL)


class AdminApp(AdminAppBase):
    name = 'spicyadmin'
    label = _('Admin')
    order_number = 10

    menu_items = (
        AdminLink('spicyadmin:admin:edit', _('Settings')),
    )

    perms = Perms(view=[],  write=[], manage=[])

    @render_to('menu.html', use_admin=True)
    def menu(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)

    @render_to('dashboard.html', use_admin=True)
    def dashboard(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)



@is_staff(required_perms=('admin.edit_settings',))
@render_to('edit.html', use_admin=True)
def edit(request):
    """Handles edit requests, renders template according `action`
    get parameter

    """
    message = None
    action = request.GET.get('action')
    profile = get_object_or_404(Profile, id=profile_id)

    if action == 'new':
        message = _('New account created, welcome to editing.')

    if (request.method == 'POST' and request.user.has_perm(
            'extprofile.change_profile')):
        form = forms.ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            message = settings.MESSAGES['success']
        else:
            message = settings.MESSAGES['error']
    else:
        form = forms.ProfileForm(instance=profile)

    passwd_form = forms.AdminPasswdForm(profile)

    return {
        'action': action,
        'profile': profile,
        'form': form,
        'passwd_form': passwd_form,
        'message': message,
        'services': api.register.get_list(consumer=profile)
    }

