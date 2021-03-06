# -*- coding: utf-8 -*-

import inspect
import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

current_path = os.path.abspath(inspect.getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)
from tools import FeaturesMenu

# noinspection PyUnusedLocal
class TestAddCmdClass(unittest.TestCase):
    test_dir = None
    plugin_dir = None
    class_dir = None
    features_menu = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = self.test_dir + os.sep + 'plugin-Test'
        self.class_dir = os.path.join(self.plugin_dir, 'core', 'class')
        self.features_menu = FeaturesMenu(self.plugin_dir, 'Test')
        os.mkdir(self.plugin_dir)
        os.mkdir(self.plugin_dir + os.sep + 'core')
        os.mkdir(self.class_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('builtins.input', side_effect=['o', 'o'])
    # pylint: disable=unused-argument
    def test_without_core_class_and_separate_files(self, side_effect):
        self.features_menu.add_cmd_class()
        self.assertTrue(os.path.exists(self.class_dir + os.sep +
                                       'Test.class.php'))
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            self.assertIn('require_once \'./TestCmd', test_file.read())
        self.assertTrue(os.path.exists(self.class_dir + os.sep +
                                       'TestCmd.class.php'))

    @patch('builtins.input', side_effect=['o', 'n'])
    # pylint: disable=unused-argument
    def test_without_core_class_and_one_file(self, side_effect):
        self.features_menu.add_cmd_class()
        self.assertTrue(os.path.exists(self.class_dir + os.sep +
                                       'Test.class.php'))
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            test_file_content = test_file.read()
            self.assertNotIn('require_once \'./TestCmd', test_file_content)
            self.assertIn('TestCmd', test_file_content)

    @patch('builtins.input', side_effect=['o'])
    # pylint: disable=unused-argument
    def test_with_core_class_and_separate_files(self, side_effect):
        with open(self.class_dir + os.sep + 'Test.class.php', 'w') as test_file:
            test_file.write('require_once dirname(__FILE__)\nclass Test '
                            'extends eqLogic {\n\n}\n')
        self.features_menu.add_cmd_class()
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            self.assertIn('require_once \'./TestCmd', test_file.read())
        self.assertTrue(os.path.exists(self.class_dir + os.sep +
                                       'TestCmd.class.php'))

    @patch('builtins.input', side_effect=['n'])
    # pylint: disable=unused-argument
    def test_with_core_class_and_one_file(self, side_effect):
        with open(self.class_dir + os.sep + 'Test.class.php', 'w') as test_file:
            test_file.write('require_once dirname(__FILE__)\nclass Test '
                            'extends eqLogic {\n\n}\n')
        self.features_menu.add_cmd_class()
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            test_file_content = test_file.read()
            self.assertNotIn('require_once \'./TestCmd', test_file_content)
            self.assertIn('TestCmd', test_file_content)
