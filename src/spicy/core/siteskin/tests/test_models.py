# coding: utf-8
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.sites.models import Site

# нет такой модели
# from siteskin.models import Block
# нет такого модуля
# from siteskin.editor import Renderer

TEMPLATE_RESULT = '''
<div class="place">
    <div class="left-column">
        <div class="block" id="block_1"><!--#include virtual="/" --></div>
        <div class="block" id="block_2"><!--#include virtual="/" --></div>
        <div class="block" id="block_3"><!--#include virtual="/" --></div>
    </div>
    <div class="right-column">
        <div class="block" id="block_4"><!--#include virtual="/" --></div>
        <div class="block" id="block_5"><!--#include virtual="/" --></div>
        <div class="block" id="block_6"><!--#include virtual="/" --></div>
    </div>
</div>

<div class="place">
    <div class="column">
        <div class="block" id="block_7"><!--#include virtual="/" --></div>
        <div class="block" id="block_8"><!--#include virtual="/" --></div>
    </div>
</div>

<div class="place">
    <div class="column">
        <div class="block" id="block_9"><!--#include virtual="/" --></div>
    </div>
</div>

<div class="place">
    <div class="left-column">
        <div class="block" id="10"><!--#include virtual="/" --></div>
        <div class="block" id="11"><!--#include virtual="/" --></div>
    </div>
    <div class="right-column">
        <div class="block" id="12"><!--#include virtual="/" --></div>
    </div>
</div>

'''

class BlockTestCase(TestCase):
   fixtures = ['siteskin_testdata.json']

   def setUp(self):
      self.site = Site.objects.get_current()

   def tearDown(self):
      settings.SITE_ID = 1

   # def test_create_block(self):
   #    rdr = Renderer(Block.objects.all())
   #
   #    print '@@@', rdr.html()
   #
   #    self.assertEqual(rdr.html(), TEMPLATE_RESULT)
