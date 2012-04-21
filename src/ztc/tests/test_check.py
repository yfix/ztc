#!/usr/bin/env python

import unittest

from ztc.check import ZTCCheck

class ZTCCheckTest(unittest.TestCase):
    class ZTCTestCheck(ZTCCheck):
        name = 'test'

        def _get(self, *args, **kwargs):
            if len(args) == 1:
                return args[0]

    def test_floatformat(self):
        """ Zabbix only accepts floating-point numbers in xx.xx format.
        Test that we are returning correct string for every float """

        ch = self.ZTCTestCheck()
        self.assertEqual(ch.get_val(8.1e-05), '0.000081')
        self.assertEqual(ch.get_val(100000.0), '100000')
        self.assertEqual(ch.get_val(0.0), '0')
        self.assertEqual(ch.get_val(0.33333333333333333333333), '0.333333')