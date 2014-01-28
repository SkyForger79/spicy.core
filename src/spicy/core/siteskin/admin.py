from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from spicy.core.service import api
from spicy.core.siteskin.decorators import render_to, ajax_request
from spicy.utils.models import get_custom_model_class
from spicy.core.profile.decorators import is_staff

from spicy.core.admin.conf import AdminAppBase, AdminLink, Perms
from . import defaults, forms, utils


SiteskinModel = get_custom_model_class(defaults.SITESKIN_SETTINGS_MODEL)


class AdminApp(AdminAppBase):
    name = 'siteskin'
    label = _('Siteskin')
    order_number = 9

    menu_items = (
        AdminLink('siteskin:admin:index', _('Theme settings')),
    )
    perms = Perms(view=[],  write=[], manage=[])

    @render_to('menu.html', use_admin=True)
    def menu(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)

    @render_to('dashboard.html', use_admin=True)
    def dashboard(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)


@is_staff(required_perms=('admin.edit_siteskin',))
@render_to('spicy.core.siteskin/admin/edit.html', use_admin=True)
def edit(request):
    """Handles edit requests, renders template according `action`
    get parameter

    """
    messages = []
    instance = utils.get_siteskin_settings()
    
    if request.method == 'POST':        
        form = forms.ThemeForm(request.POST, instance=instance)
        if form.is_valid():
            # TODO
            # reload UWSGI or DEVserver 
            # update Static and Templates loaders settings
            
            form.save()
        else:
            messages.append(form.errors.as_text())
    else:
        form = forms.ThemeForm(instance=instance)

    return {
        'form': form,
        'messages': messages,
    }

