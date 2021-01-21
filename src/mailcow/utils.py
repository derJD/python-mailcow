#!/usr/bin/env python

# Copyright (c) 2021 Jean-Denis Gebhardt <projects@der-jd.de>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import re
import sys
import logging


def chomp(data):
    '''Remove multi-whitespaces and newlines'''
    return re.sub(r'[ ]{2,}', '', data.strip())


def debug_mailcow(debug=False):
    '''Set loglevel to debug and log to stdout'''
    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)
    logging.StreamHandler(sys.stdout)


def debug_msg(data):
    '''Debug what's happening'''
    if isinstance(data, str):
        logging.debug(chomp(data))
    else:
        logging.debug(data)


def build_attributes(**kwargs):
    '''
    Convert argparse arguments into a dict for edit and add requests.

    Arguments:
        **(vars(args))      This function takes all arguments from argparse
        endpoints    (dict) Object provided by MailCowOpenApi()

    Example:
        moo = MailCow()
        sections = MailCowOpenApi(f'{moo.url}/api/openapi.yaml')
        args = menu(sections.endpoints)
        build_attributes(**(vars(args)), routes=sections)
        will return output dependend on argparse
        build_attributes(
            section=alias,
            modifier=edit,
            items=["5"],
            active=True,
            address=example@example.com,
            goto=goto@example.com
            routes=sections)
        will return: {
            'active': "1",
            'address': 'example@example.com',
            'goto': 'goto@example.com'
        }
    '''
    endpoints = kwargs.get('endpoints')
    section = kwargs.get('section')
    modifier = kwargs.get('modifier')
    attrs = dict()

    for arg in endpoints[section][modifier]:
        value = kwargs.get(arg)

        # Bools must be converted into int str
        if isinstance(value, bool):
            # Hack avoid using argparse.BooleanOptionalAction as action
            if f'--no-{arg}' in sys.argv:
                value = False
            attrs.update({arg: str(int(value))})
        else:
            attrs.update({arg: value})
        # items are usually stored in separate list
        if value is None or arg == 'items':
            del attrs[arg]

    return attrs


def parse_fields(fields, vertical):
    '''
    Splitts `fields` if necessary

    Attributes:
        fields      (string)  Will be converted to list if splittable by ','
        vertical    (boolean) Skip splitting if True

    Example:
        Incase someone use fields as commaseparated list ie:
        `[...] --fields address,goto` instead of
        `[...] --fields address --fields goto`
    '''
    if fields and not vertical:
        for field in fields:
            fields = field.split(',') if ',' in field else fields
        debug_msg(f'Filter Fields: {fields}')

    return fields


def prepare_getRequest(**kwargs):
    '''
    Sections in /api​/v1​/get​/ require more manipulation.
    This will compare argparse values with openapi parameters
    and setup url accordingly.

    Arguments:
        **(vars(args))     This function takes all arguments from argparse
        endpoints    (dict) Object provided by MailCowOpenApi()

    Example:
    moo = MailCow()
    sections = MailCowOpenApi(f'{moo.url}/api/openapi.yaml')

    prepare_getRequest(section='syncjobs', all=True, no_log=True)
    will return `syncjobs​/all​/no_log`
    prepare_getRequest(section='logs', api=True, count=5)
    will return `logs/api/5`
    '''
    endpoints = kwargs.get('endpoints')
    section = kwargs.get('section')
    return_section = section
    arguments = endpoints[section]['get']
    count = kwargs.get('count')
    mailbox = kwargs.get('mailbox')

    for argument in arguments.keys():
        if arguments[argument]['type'] == 'bool' and kwargs.get(argument):
            return_section = f'{section}/{argument}'
            if count:
                return_section = f'{return_section}/{count}'

    if kwargs.get('all'):
        return_section = f'{section}/all'

        # its always /api​/v1​/get​/syncjobs​/all​/no_log
        if kwargs.get('no_log'):
            return_section = f'{return_section}/no_log'

    # can be: /api​/v1​/get​/app-passwd/all​/$mailbox
    # or:/api​/v1​/get​/rl-mbox​/$mailbox
    if mailbox:
        return_section = f'{return_section}/{mailbox}'

    # if set id and domain should override return_section
    if kwargs.get('id'):
        return_section = f'{section}/{kwargs["id"]}'
    if kwargs.get('domain'):
        return_section = f'{section}/{kwargs["domain"]}'

    debug_msg(f'Parsed get request: {return_section}')

    return return_section


def filterOpenApiPath(schema):
    '''filter out relevant dicts from OpenApi'''
    method = ''.join(schema)
    parameters = schema[method].get('parameters')
    requestbody = schema[method].get('requestBody')
    schema = {}
    if requestbody:
        schema = requestbody['content']['application/json']['schema']

    return dict(
        parameters=parameters,
        schema=schema
    )


def describeOpenApiPath(path):
    path = list(filter(None, path.split('/')[3:]))
    modifier = path[0]
    section = path[1]
    all = False
    component = 'no_log' if path[-1] == 'no_log' else None
    parameter = path[-1] if '{' in path[-1] else None

    if len(path) > 2:
        all = (path[2] == 'all')
        if '{' not in path[2] and path[2] != 'all':
            component = path[2]

    return dict(
        modifier=modifier,
        section=section,
        all=all,
        component=component,
        parameter=parameter)


def getOpenApiParameters(data):
    '''Extract data from OpenApi that is passed via URL.'''
    arguments = dict()

    if isinstance(data, list):
        for parameter in data:
            if parameter['in'] == 'path':
                arguments.update({
                    parameter['name']: {
                        'description': parameter['description'],
                        'type': parameter['schema']['type']}})

    if isinstance(data, str):
        # This type isn't 'boolean' on purpose. argparse will distinguish
        # between store_true and OptionalBoolean this way
        arguments.update({data: {
            'description': f'get {data} entries',
            'type': 'bool'}})

    return arguments


def getOpenApiProperties(schema):
    '''Extract data from OpenApi that must be send via body.'''
    properties = schema.get('properties', {})
    items = schema.get('items')
    attr = properties.get('attr')

    # schema/items instead of schema/properties/items
    # missing in delete/{alias,dkim}
    if items:
        properties.update({'items': schema['items']})

    # move properties to top and remove redundant properties key
    if attr:
        properties.update(attr['properties'])
        del properties['attr']

    return properties
