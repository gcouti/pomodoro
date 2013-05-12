#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import sys
import os.path
import unittest

class TestExample(unittest.TestCase):
    def setUp(self):
        pass

    def test_AboutPomodoreDialog_members(self):
        self.assertEqual(self.AboutPomodoreDialog_members, public_members)
        pass

if __name__ == '__main__':    
    unittest.main()
