#!/usr/bin/env python

# Copyright (c) 2021 Jean-Denis Gebhardt <projects@der-jd.de>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

'''This module is for building argumentparser needed by CLI'''

import argparse
import sys
from mailcow.globals import CONF


def menu(sections=None):
    '''Function building CLI menu'''
    parser = argparse.ArgumentParser(
        description='Interact with mailcow\'s API. ')
    parser.add_argument('--create-example-config', action='store_true',
                        dest='create_cfg', help='Create configuration file')
    parser.add_argument('--conf', '-c', action='store', dest='conf',
                        default=CONF,
                        help='Defaults to: %(default)s')
    parser.add_argument('--vertical', '-v', action='store_true',
                        dest='vertical', default=False,
                        help='Print (table) results vertically')
    parser.add_argument('--json', '-j', action='store_true', dest='json',
                        default=False, help='Print results as JSON')
    parser.add_argument('--yaml', '-y', action='store_true', dest='yaml',
                        default=False, help='Print results as YAML')
    parser.add_argument('--table', '-t', action='store_true', dest='table',
                        default=True, help='Print results as Table')
    parser.add_argument('--debug', '-d', action='store_true', dest='debug',
                        default=False, help='Enable debugging')
    section_subparser = parser.add_subparsers(dest='section')

    if isinstance(sections, dict):
        for section, modifiers in sections.items():
            section_parser = section_subparser.add_parser(section)
            modify_subparser = section_parser.add_subparsers(dest='modifier')

            for modifier in modifiers:
                modify_parser = modify_subparser.add_parser(modifier)
                arguments = modifiers[modifier]
                build_argument(modify_parser, arguments)

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    return args


def build_argument(data, arguments):
    '''Parse endpoints and build arguments accordingly'''
    for argument, values in arguments.items():
        data_help = values['description'] if 'description' in values else None
        choices = values['enum'] if 'enum' in values else None
        action = 'store'
        options = [f'--{argument}']

        # API catches...
        # add/tls-policy-map - "'dane" in enum
        #
        # edit/fail2ban - only `items` without types
        if 'type' not in values:
            values.update({'type': None})
        # active in add/{bcc,domain-add,pushover,recipient_map,
        #   resource,tls-policy-map,transport}
        #   is number instead of boolean like the rest
        if argument == 'active':
            values['type'] = 'boolean'
        # edit/fail2ban - only items that is actually a string
        if argument == 'items' and values['type'] is not None:
            action = 'append'

        # translating types into `actions` and `type`
        if values['type'] in ['bool', 'boolean']:
            action = 'store_true'
        if values['type'] in ['object', 'array']:
            data_help = f'{data_help}. Can be used multiple times.'
        # would rather use argparse.BooleanOptionalAction action
        # but it's a bit too new
        if values['type'] == 'boolean':
            options.append(f'--no-{argument}')

        if choices:
            data.add_argument(
                *options, action=action, help=data_help, choices=choices)
        elif values['type'] == 'number':
            data.add_argument(
                *options, action=action, help=data_help, type=int)
        else:
            data.add_argument(
                *options, action=action, help=data_help, default=None)

    return data


def main():
    '''Main'''
    m = menu()
    print(m)


if __name__ == "__main__":
    main()
