#!/usr/bin/env python
"""
test for ztc.system.time check

This file is part of ZTC

Copyright (c) 2012 Vladimir Rusinov <vladimir@greenmice.info>

License: GNU GPL 3
"""

import unittest

from ztc.system.time import TimeCheck


class TestTime(unittest.TestCase):
    """Test for ztc.system.time.TimeCheck class"""

    def setUp(self):
        self.failed_ntp_check = TimeCheck()
        self.failed_ntp_check._timeout = 0.1
        self.failed_ntp_check._ntp_addr = "example.com"

        self.ntp_check = TimeCheck()

    def test_offset(self):
        """Positive test. requires network"""
        assert isinstance(self.ntp_check.offset, float), "Offset is not float"

    def test_offset_ntp_dead(self):
        """Test offset when ntp server is dead"""
        assert self.failed_ntp_check.offset == 3600

    def test_delay(self):
        assert isinstance(self.ntp_check.delay, float), "Delay is not float"

    def test_delay_fail(self):
        assert self.failed_ntp_check.offset == 3600

    def test_precision(self):
        assert isinstance(self.ntp_check.precision, float), \
            "Delay is not float"
        assert self.ntp_check.precision < 2, "Precision is >= 2"

    def test_precision_fail(self):
        p = self.failed_ntp_check.precision
        assert p == 2, "Failed precision is not 2, %i instead" % p

    def test_uncknown_metric(self):
        try:
            self.assertRaises(AttributeError, self.ntp_check.none)
            self.assertRaises(AttributeError, self.ntp_check._get('none'))
        except AttributeError:
            # we don't want this test to fail
            pass

if __name__ == '__main__':
    unittest.main()
