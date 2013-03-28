from . import forms, models
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from spicy.core.siteskin.decorators import ajax_request, render_to, multi_view


@login_required
@ajax_request
def delete(request, account_id):
    account = get_object_or_404(models.Account, pk=account_id)
    status = 'ok'
    message = _('Account deleted')

    if not request.user.account.filter(pk=account_id).exists():
        status = 'error'
        message = _('Account not stored')
    else:
        request.user.account.remove(account)
        
    return {'status': status, 'message': message}


@login_required
@render_to('account/view.html', use_siteskin=True)
def view(request, account_id):
    account = get_object_or_404(
        models.Account, pk=account_id, is_approved=True)
    return {'account': account}

