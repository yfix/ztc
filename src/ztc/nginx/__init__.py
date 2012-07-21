#!/usr/bin/env python
#pylint: disable=W0232
"""
ztc.nginx package

Copyright (c) 2010 Vladimir Rusinov <vladimir@greenmice.info>
License: GPL3
This file is part of ZTC [http://bitbucket.org/rvs/ztc/]
"""

import urllib2
import time

#import ztc.commons
from ztc.check import ZTCCheck, CheckFail
from ztc.store import ZTCStore


class NginxStatus(ZTCCheck):
    """ Nginx status page reader and parser """

    OPTPARSE_MIN_NUMBER_OF_ARGS = 1
    OPTPARSE_MAX_NUMBER_OF_ARGS = 1
    name = 'nginx'

    _page_data = None  # data from status page
    ping_time = 0

    #pylint: disable=W0613
    def _get(self, metric=None, *args, **kwargs):
        """ get metric """
        allowed_metrics = ('accepts', 'handled', 'requests',
            'connections_active', 'connections_reading', 'connections_waiting',
            'connections_writing', 'ping')
        if metric in allowed_metrics:
            return self.__getattribute__('get_' + metric)()
        else:
            raise CheckFail("Requested not allowed metric")

    def _read_status(self):
        """ urlopen and save to _page_data text of status page """
        if self._page_data is not None:
            # we've already retrieved it
            return True

        st = ZTCStore('nginx.status_page', self.options)
        try:
            read_start = time.time()
            url = "%s://%s:%s%s?auto" % (
                                         self.config.get('proto', 'http'),
                                         self.config.get('host', 'localhost'),
                                         self.config.get('port', '8080'),
                                         self.config.get('resource',
                                                         '/server-status'))
            try:
                u = urllib2.urlopen(url, None, 1)
            except TypeError:
                u = urllib2.urlopen(url, None)
            self._page_data = u.readlines()
            u.close()
            st.set(self._page_data)
            # calulate how many time was required:
            self.ping_time = time.time() - read_start
            return True
        except urllib2.URLError:
            self.logger.exception('failed to load test page')
            # status page read failed
            self._page_data = st.get()
            self.ping_time = 0  # status page read failed
            return False

    def _get_info(self, name):
        """ Extracts info from status """
        self._read_status()
        ret = None
        for l in self._page_data.split("\n"):
            if l.find(name + ": ") == 0:
                ret = l.split()[-1]
                break
        return ret

    def get_accepts(self):
        """ Number of accept()s since server start """
        self._read_status()
        if self._page_data:
            my_line = self._page_data[2]
            return int(my_line.split()[0])
        else:
            return 0
    accepts = property(get_accepts)

    def get_handled(self):
        """ Number of handled()s since server start """
        self._read_status()
        if self._page_data:
            my_line = self._page_data[2]
            return int(my_line.split()[1])
        else:
            # no data neither in nginx or cache
            return 0
    handled = property(get_handled)

    def get_requests(self):
        """ Number of requests()s since server start """
        self._read_status()
        if self._page_data:
            my_line = self._page_data[2]
            return int(my_line.split()[2])
        else:
            return 0
    requests = property(get_requests)

    def get_connections_active(self):
        """
        first line:
        Active connections: 123
        """
        try:
            self._read_status()
            my = self._page_data[0].split()[-1]
            return int(my)
        except:
            return 0
    connections_active = property(get_connections_active)

    def get_connections_reading(self):
        try:
            self._read_status()
            my = self._page_data[-1].split()[1]
            return int(my)
        except:
            return 0
    connections_reading = property(get_connections_reading)

    def get_connections_waiting(self):
        try:
            self._read_status()
            my = self._page_data[-1].split()[5]
            return int(my)
        except:
            return 0
    connections_waiting = property(get_connections_waiting)

    def get_connections_writing(self):
        try:
            self._read_status()
            my = self._page_data[-1].split()[3]
            return int(my)
        except:
            return 0
    connections_writing = property(get_connections_writing)

    def get_ping(self):
        try:
            self._read_status()
        finally:
            return self.ping_time
    ping = property(get_ping)


if __name__ == '__main__':
    st = NginxStatus()
    print "ping:", st.ping
    print "accepts:", st.get_accepts()
