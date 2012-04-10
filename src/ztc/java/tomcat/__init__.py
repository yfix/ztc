#!/usr/bin/env python
#
# Tomcat jmx_proxy monitpring class
#
# Copyright (c) 2012 Wrike. Inc.

import urllib2

from ztc.check import ZTCCheck

class TomcatJMXProxy(ZTCCheck):
    """ tomcat jmx_proxy monitoring class
    For more docs see
    http://tomcat.apache.org/tomcat-7.0-doc/manager-howto.html """

    name = "tomcat_jmx_proxy"

    OPTPARSE_MAX_NUMBER_OF_ARGS = 3

    proto = 'http'
    host = 'localhost'
    port = 8080
    username = 'zabbix'
    password = 'zabbix'
    timeout = 10

    def _myinit(self):
        self.proto = self.config.get('proto', self.proto)
        self.host = self.config.get('host', self.host)
        self.port = int(self.config.get('port', self.port))
        self.username = self.config.get('username', self.username)
        self.password = self.config.get('password', self.password)

    # pylint: disable=W0613
    def _get(self, metric, *arg, **kwarg):
        if metric == 'get':
            bean = arg[0]
            attr = arg[1]
            if len(arg) > 2:
                key = arg[2]
            else:
                key = None
            return self.get_jmx_attr(bean, attr, key)
        else:
            raise NotImplementedError("Metric %s is not implemented" % metric)

    def get_jmx_attr(self, bean_name, attr, key=None):
        url = "%s://%s:%s/manager/jmxproxy/?get=%s&att=%s" % (
            self.proto,
            self.host,
            self.port,
            bean_name,
            attr
            )
        if key:
            url = url + "&key=%s" % key

        self.logger.debug("Fetching from %s" % url)

        # get the page
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, self.username, self.password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        response = opener.open(url, None, self.timeout)
        resp_text = response.read()
        (status, req, resp) = resp_text.split('-')
        if status.strip().lower() != 'ok':
            self.logger.error('Response is not ok')
            return None
        contents = resp.split('contents=')[-1].strip()[:-1]
        return contents
