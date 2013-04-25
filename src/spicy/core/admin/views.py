from django.contrib.auth import views
from spicy.core.profile.decorators import is_staff
from spicy.core.service import api
from spicy.core.siteskin.decorators import render_to


@is_staff
@render_to('index1.html')
def index(request):
    return {'services': api.register.get_list()}


def login(request):
    return views.login(
        request, template_name='admin/login.html')
