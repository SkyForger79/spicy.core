import os
from . import defaults, forms
from django.conf import settings
from django.contrib.sites.models import Site
from spicy import utils

SimplePage = utils.get_custom_model_class(defaults.SIMPLE_PAGE_MODEL)


def find_simplepages():
    base_dir = "spicy.core.simplepages/simplepages"
    templates = utils.find_templates(base_dir, name_tuples=False)
    found = []
    existing = []
    site = Site.objects.get_current()
    extensions = 'html', 'txt'
    for filepath in templates:
        ext = filepath.rsplit('.', 1)[-1]
        if ext not in extensions:
            continue

        filename = filepath.rsplit('/simplepages/', 1)[-1]
        original_filename = filename
        if filename.endswith('.html'):
            filename = filename[:-5]

        splitted = filename.rsplit('.')
        if ext != 'html':
            splitted = splitted[:-2] + ['.'.join(splitted[-2:])]
        basename = '.'.join(splitted)
        baseurl = '/'.join(splitted)
        url = ('/{0}/' if ext == 'html' else '/{0}').format(baseurl)
        content = file(filepath).read()
        template_name = os.path.join(base_dir, original_filename)
        page, is_created = SimplePage.objects.get_or_create(
            title=basename, url=url,
            defaults={'content': content, 'template_name': template_name})
        if is_created:
            page.sites = [site]
            found.append(page)
        else:
            existing.append(page)
            page.content = content
            page.save()
    return {'found': found, 'existing': existing}


def edit_simple_page(request, page):
    message = None
    if request.method == 'POST':
        form = forms.SimplePageForm(request.POST, instance=page)
        if form.is_valid():
            page = form.save()
            form = forms.SimplePageForm(instance=page)
        else:
            message = settings.MESSAGES['error']
    else:
        form = forms.SimplePageForm(instance=page)
    return {
        'form': form, 'message': message, 'instance': form.instance,
        'tab': 'page'}
