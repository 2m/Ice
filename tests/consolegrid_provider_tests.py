# encoding: utf-8
"""
consolegrid_provider_tests.py

Created by Scott on 2014-08-18.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import os
import unittest
from mockito import *

from six.moves.urllib.error import URLError

# I need to do this instead of importing the class explicitly so that I can
# override the urllib2 function.
# TODO: Use dependency injection so I don't need to use that hack.
from ice.gridproviders import consolegrid_provider


class ConsoleGridProviderTests(unittest.TestCase):

  def setUp(self):
    self.provider = consolegrid_provider.ConsoleGridProvider()

  def tearDown(self):
    pass

  def dummy_urlopen_function(self, code=200, data="Data", err=None):
    def f(url):
      if err:
        raise err
      m = mock()
      when(m).getcode().thenReturn(code)
      when(m).read().thenReturn(data)
      return m
    return f

  def create_mock_rom(self, rom_name="Test ROM", console_name="Test"):
    console = mock()
    console.fullname = console_name
    console.shortname = console_name

    rom = mock()
    rom.name = rom_name
    rom.console = console
    return rom

  def test_is_enabled_returns_true(self):
    self.assertTrue(self.provider.is_enabled())

  def test_consolegrid_top_picture_url(self):
    rom = self.create_mock_rom("Megaman")
    url = self.provider.consolegrid_top_picture_url(rom)
    self.assertIn("consolegrid.com", url)
    self.assertIn("game=Megaman", url)
    self.assertIn("console=Test", url)

  def test_consolegrid_top_picture_url_quotes_special_characters(self):
    rom = self.create_mock_rom("Dankey Kang#Country")
    url = self.provider.consolegrid_top_picture_url(rom)
    self.assertNotIn("Dankey Kang#Country", url)
    self.assertIn("Dankey%20Kang%23Country", url)

  def test_find_url_returns_none_on_204(self):
    rom = self.create_mock_rom("Megaman")
    #consolegrid_provider.six.moves.urllib.request.urlopen = self.dummy_urlopen_function(204)
    self.assertIsNone(self.provider.find_url_for_rom(rom))

  def test_find_url_returns_none_on_urlerror(self):
    rom = self.create_mock_rom("Megaman")
    err = URLError("")
    #consolegrid_provider.six.moves.urllib.request.urlopen = self.dummy_urlopen_function(err=err)
    self.assertIsNone(self.provider.find_url_for_rom(rom))

  def test_image_for_rom_returns_none_when_empty_image_url(self):
    def dummy_find_url_for_rom(rom):
      return ""
    self.provider.find_url_for_rom = dummy_find_url_for_rom
    self.assertIsNone(self.provider.image_for_rom(None))
