from spicy.core.profile.decorators import is_staff

from spicy.core.siteskin.decorators import render_to

from spicy.core.service import api


@is_staff
@render_to('index.html')
def index(request):
    return {'services': api.register.get_list()}
