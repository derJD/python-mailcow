#!/usr/bin/env python3

# Copyright (c) 2021 Jean-Denis Gebhardt <projects@der-jd.de>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

'''Class for mailcow interaction'''

import json
import requests
from prettytable import PrettyTable
from mailcow.config import find_cfg, load_cfg
from mailcow.globals import SSL_TIMEOUT, SSL_VERIFY, CONF
from mailcow.utils import (
    debug_msg,
    describeOpenApiPath, filterOpenApiPath,
    getOpenApiParameters,
    getOpenApiProperties, validate_response)
import yaml
import urllib3

class MailCow:
    '''
    Connect to MailCow instance defined in config file and
    interact via API Requests

    | Argument | Type | Description |
    | -------- | ---- | ----------- |
    | conf | String | Path to config file |
    | server | String | Name of the section providing further server information |
    |url  | String | Base URL (MailCow UI location) for connection ie: https://demo.mailcow.io |
    | token | String | Token for API-Access |
    | ssl_verify | Boolean | Enable/Disable ssl verification |
    | timeout | Integer | Connection timeout |

    Example:
    ```
    moo = MailCow()
    logs = moo.getRequest(section='logs/api/5')
    moo.data = logs
    print(moo.as_table())
    # returns:
    # +------------+----------------------------------+--------+-----------+------+
    # |    time    |               uri                | method |   remote  | data |
    # +------------+----------------------------------+--------+-----------+------+
    # | 1611102437 |      /api/v1/get/logs/api/5      |  GET   | xx.x.xx.x |      |
    # | 1611096182 | /api/v1/get/rl-mbox/xx@examp.com |  GET   | xx.x.xx.x |      |
    # | 1611087846 | /api/v1/get/rl-mbox/xx@examp.com |  GET   | xx.x.xx.x |      |
    # | 1611087808 |    /api/v1/get/logs/dovecot/5    |  GET   | xx.x.xx.x |      |
    # | 1611087797 | /api/v1/get/syncjobs/all/no_log  |  GET   | xx.x.xx.x |      |
    # +------------+----------------------------------+--------+-----------+------+
    ```
    '''  # noqa
    def __init__(self, **kwargs):
        cfg = None
        conf = kwargs.get('conf', CONF)
        if find_cfg(conf):
            cfg = load_cfg(conf)
            debug_msg(f'cfg: {cfg}')

        self.server = kwargs.get('server', cfg['defaults']['server'])
        self.url = kwargs.get('url', cfg[self.server]['url'])
        self.token = kwargs.get('token', cfg[self.server]['token'])
        self.ssl_verify = kwargs.get('ssl_verify', cfg['defaults'].get('ssl_verify', cfg[self.server].get('ssl_verify', f'{SSL_VERIFY}'))).lower() not in ["false", "no", "f"]
        if not self.ssl_verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.timeout = int(kwargs.get('timeout', cfg['defaults'].get('timeout', cfg[self.server].get('timeout', f'{SSL_TIMEOUT}'))))
        self.data = None
        self.json = None

        self.request_url = f'{self.url}/api/v1'
        self.session = self._establish_session()
        self.schema = self.getOpenApiSchema()
        self.endpoints = self._endpoints()

    def getOpenApiSchema(self):
        '''Read OpenApi Schema from `self.url`'''
        response = self._request(
            url=f'{self.url}/api/openapi.yaml',
            method='get')

        return yaml.safe_load(response)

    def endpoint(self, endpoint):
        '''Return specific endpoint'''
        return self.endpoints.get(endpoint)

    def _endpoints(self):
        '''Return all endpoints provided by OpenApi'''
        endpoints = dict()

        for path in self.schema['paths'].keys():
            schema = filterOpenApiPath(self.schema['paths'][path])
            p = describeOpenApiPath(path)
            section = p['section']
            modifier = p['modifier']
            arguments = dict()

            if p.get('all') or p.get('parameter') == '{id}':
                arguments.update(getOpenApiParameters('all'))

            arguments.update(getOpenApiParameters(p.get('component')))
            arguments.update(getOpenApiParameters(schema.get('parameters')))
            arguments.update(getOpenApiProperties(schema.get('schema')))

            if section not in endpoints.keys():
                endpoints.update({section: dict()})

            if modifier not in endpoints[section].keys():
                endpoints[section].update({modifier: dict()})

            endpoints[section][modifier].update(arguments)

        return endpoints

    def _establish_session(self):
        '''Connect to mailcow instance'''
        for msg in [f'Request Session verify: {self.ssl_verify}',
                    f'Request Session timeout: {self.timeout}']:
            debug_msg(msg)

        session = requests.Session()
        session.verify = self.ssl_verify
        session.timeout = self.timeout

        return session

    @validate_response
    def _request(self, **kwargs):
        '''Send requests to mailcow instance'''
        url = kwargs.get('url', self.url)
        token = kwargs.get('token', self.token)
        method = kwargs.get('method')
        data = kwargs.get('json', self.json)
        headers = {'X-API-Key': token}

        debug_msg(f'Request URL: {url}')
        debug_msg(f'Request Payload: {json}')

        request = self.session.request(
            headers=headers,
            method=method,
            url=url,
            json=data)

        return request

    def deleteRequest(self, section, items):
        '''
        Send DELETE request to MailCow instance.

        Example:
        ```
        moo = MailCow()
        moo.deleteRequest('alias', ['5'])
        # {moo.server}/api/v1/delete/alias
        # JSON Body: ["5"]
        ```
        '''
        url = f'{self.request_url}/delete/{section}'

        return self._request(url=url, method='post', json=items)

    def getRequest(self, section):
        '''
        Send GET request to MailCow instance.

        Example:
        ```
        moo = MailCow()
        moo.deleteRequest('alias/all')
        # {moo.server}/api/v1/alias/all
        ```
        '''
        url = f'{self.request_url}/get/{section}'

        return self._request(url=url, method='get')

    def addRequest(self, section, data=None):
        '''
        Send PUT request to MailCow instance.

        Example:
        ```
        moo = MailCow()
        attributes = dict(
            address="example@example.com",
            goto="mailbox@example.com")
        moo.deleteRequest('alias', attributes)
        # {moo.server}/api/v1/add/alias
        # JSON Body:
        #   {"address": "example@example.com", "goto": "mailbox@example.com"}
        ```
        '''
        url = f'{self.request_url}/add/{section}'

        return self._request(url=url, method='post', json=data)

    def editRequest(self, section=None, items=None, attr=None, action=None):
        '''
        Send POST request to MailCow instance.

        Example:
        ```
        moo = MailCow()
        attributes = dict(
            address="new_example@example.com",
            goto="mailbox@example.com")
        items = ['5']
        moo.deleteRequest('alias', items, attributes)
        # {moo.server}/api/v1/edit/alias
        # JSON Body: {
        #   "items": ["5"],
        #   "attr": {
        #       "address": "new_example@example.com",
        #       "goto": "mailbox@example.com"
        #   }
        # }
        ```
        '''
        url = f'{self.request_url}/edit/{section}'
        data = dict(items=items, attr=attr, action=action)

        if not items:
            del data['items']
        if not attr:
            del data['attr']
        if not action:
            del data['action']

        return self._request(url=url, method='post', json=data)

    def as_json(self):
        '''Convert self.data into JSON'''
        return json.dumps(self.data, indent=4)

    def as_yaml(self):
        '''Convert self.data into YAML'''
        return yaml.dump(self.data)

    def as_table(self, vertical=False):
        '''Convert self.data into PrettyTable'''
        tables = []
        table = PrettyTable()

        for data in self.data if isinstance(self.data, list) else [self.data]:
            if vertical:
                table.add_column('Key', list(data.keys()))
                table.add_column('Value', list(data.values()))
                tables.append(table)
                table = PrettyTable()
            else:
                table.field_names = data.keys()
                table.add_row(data.values())

        if not vertical:
            tables.append(table)

        return tables
