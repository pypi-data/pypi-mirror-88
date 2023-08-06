import unittest
import shutil
import re
import os
from os import walk

from pyBaseApp import Configuration

class TestConfiguration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.target_folder = 'tests/output/configuration/log'
        shutil.rmtree(cls.target_folder, ignore_errors=True)
        cls.conf = Configuration(cls.target_folder)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.target_folder, ignore_errors=True)

    def test_init(self):
        f = []
        for (_, _, filenames) in walk(self.target_folder):
            f.extend(filenames)
            break

        self.assertTrue(f, '{} has not been created or no log file has been created inside'.format(self.target_folder))

        with open(os.path.join(self.target_folder, f[0]),'r') as log:
            line = log.readline()
            result = re.match(r'.*INFO.*configuration.py.*[0-9]+.*app initialised', line)
            self.assertTrue(result, 'log line does not comply with expected regex')

    def test_settings(self):
        settings_file = 'tests/unit/resources/settings.yml'
        settings = self.conf.settings(settings_file)
        self.assertTrue(settings, 'no setting loaded from file {}'.format(os.path.abspath(settings_file)))
        self.assertTrue('mykey' in settings, 'no key "mykey" in settings')
        self.assertEqual(settings['mykey'], 'myvalue', 'expected "my value" but received {}'.format(settings['mykey']))

    def test_settings_no_extension(self):
        settings_file = 'tests/unit/resources/settings'
        settings = self.conf.settings(settings_file)
        self.assertTrue(settings, 'no setting loaded from file {}'.format(os.path.abspath(settings_file)))
        self.assertTrue('mykey' in settings, 'no key "mykey" in settings')
        self.assertEqual(settings['mykey'], 'myvalue', 'expected "my value" but received {}'.format(settings['mykey']))

    def test_substitution(self):
        settings_file = 'tests/unit/resources/settings'
        settings = self.conf.settings(settings_file)
        self.assertTrue(settings, 'no setting loaded from file {}'.format(os.path.abspath(settings_file)))
        self.assertTrue('value_to_substitute' in settings, 'no key "value_to_substitute" in settings')
        self.assertEqual(settings['value_to_substitute'], '3', 'expected "3" but received {}'.format(settings['value_to_substitute']))