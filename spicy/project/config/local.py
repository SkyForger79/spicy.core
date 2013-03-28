# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _


###################
# COMMON

DEBUG = True # turn off for the perfomance in the production server
TEMPLATE_DEBUG = DEBUG 

#USE_TZ = False
#TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'ru'
USE_I18N = True
USE_L10N = True

SITE_ID = 1
MEDIA_URL = '/st/'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
PROJECT_ADMINS = ('support@example.com',)

CACHE_BACKEND = 'memcached://127.0.0.1:11311/'#'locmem:///'
CACHE_TIMEOUT = 1*60 # seconds

####################
# CALLGRAPH

#CALLGRAPH_INCLUDE = ['account.*']
#CALLGRAPH_EXCLUDE = ['django.*']
#DB_LOGGER_URL = 'pg.example.com'

####################
# SITESKIN & STATIC
SITESKIN = 'example.com'
SITESKIN_ADMIN = 'spicy-admin'
TEMPLATE_DIRS = ('templates/',)
MEDIA_ROOT = '/static'
#USE_RENDER_FROM_RESPONSE_LIKE_SSI = True
#SITESKIN_CSS_VERSION_PATH = '../templates/VERSION' # TODO version control for the static-media


###################
# PROFILE 

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/signin/'
REGISTRATION_OPEN = True
CUSTOM_USER_MODEL = 'account.Account'


####################
# PRESSCENTER

#OBJECTS_PER_PAGE = 10 # TODO siteskin ?? settings
#DEFAULTS_DOCS_PER_PAGE = 8
#DEFAULTS_DOCS_PER_PAGE_ALL = 5
#CUSTOM_DOCUMENT_MODEL = 'account.Document'


####################
# MAIL

SERVER_EMAIL = 'no-reply@example.com'
DEFAULT_FROM_EMAIL = 'no-reply@example.com'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
#EMAIL_HOST_PASSWORD=''
#EMAIL_HOST_USER='support'
#EMAIL_BACKEND


###################
# MEDIACENTER

#MEDIACENTER_ROOT = '/tmp/mediacenter/'
#MEDIACENTER_URL_PREFIX = '/admin/media/'
#MEDIACENTER_SOURCES = {
#  'ftp':  {'path': 'ftp_sourcedir',  'label':_('Test_lable')}, 
#  'ftp1': {'path': 'ftp1_sourcedir', 'label':_('Test1_lable')}, 
#  'ftp2': {'path': 'ftp2_sourcedir', 'label':_('Test2_lable')}, 
#}

# Custom processor for sorl.
#THUMBNAIL_PROCESSORS = (
#    'spicy.core.mediacenter.utils.pre_crop',
#    'sorl.thumbnail.processors.scale_and_crop',
#)
# TODO thumbnails 


###################
# SPHINX SEARCH ENGINE

#SPHINX_API_VERSION = 0x116


###################
# RMANAGER

REPOSITORY_TYPE = 'hg'
APP_SOURCE_PATH = 'src/'
ADDITIONAL_PYTHON_PATH = 'dev_apps/'

###################
# OTHER settings
