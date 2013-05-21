import os
from setuptools import setup


version = __import__('spicy').get_version()
EXCLUDE_FROM_PACKAGES = [
    'spicy.templates',
]


def fullsplit(path, result=None):
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


def is_package(package_name):
    for pkg in EXCLUDE_FROM_PACKAGES:
        if package_name.startswith(pkg):
            return False
    return True


packages, package_data = [], {}

root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
package_dir = 'spicy'


for dirpath, dirnames, filenames in os.walk(package_dir):
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
    parts = fullsplit(dirpath)
    package_name = '.'.join(parts)
    if '__init__.py' in filenames and is_package(package_name):
        packages.append(package_name)
    elif filenames:
        relative_path = []
        while '.'.join(parts) not in packages:
            relative_path.append(parts.pop())
        relative_path.reverse()
        path = os.path.join(*relative_path)
        package_files = package_data.setdefault('.'.join(parts), [])
        package_files.extend([os.path.join(path, f) for f in filenames])


setup(
    name='spicy',
    version=version,
    packages=packages,
    package_data=package_data,
    install_requires=[
        'Django==1.4.3',
        'Fabric==1.6',
        'Sphinx==1.2b1',
        'numpydoc==0.4',
        'raven==3.2.1',
        'python-memcached==1.48',
        'configparser==3.3.0r2',
        'Jinja2==2.6',

        # ?? siteskin deps.
        'pytils==0.2.3',
        'pytz',
        'html5lib==0.95',

        # profile deps.
        #'sorl-thumbnail==3.2.5',
        'django-crispy-forms==1.2.6',
        #'django-simple-captcha',
        #'django-social-auth==0.6.1',

        # debug deps.
        # 'logutils', #TODO: version?
        'numpydoc',
        'django-nose',
        'django-debug-toolbar',
        'django-devserver',
        'django-extensions',
        'werkzeug',
    ],

    entry_points={
        'console_scripts': [
            'spicy = spicy.script:handle_command_line',
        ],
    },
)
