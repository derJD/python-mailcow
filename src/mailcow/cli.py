#!/usr/bin/env python

# Copyright (c) 2021 Jean-Denis Gebhardt <projects@der-jd.de>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import sys
from mailcow import MailCow
from mailcow.globals import CONF, FIELDS
from mailcow.menu import menu
from mailcow.config import create_cfg
from mailcow.utils import (
    debug_mailcow,
    debug_msg,
    build_attributes,
    parse_fields,
    prepare_getRequest)


def main():
    # Allow creation of example configuration file
    # before building argparse menu
    if '--create-example-config' in sys.argv:
        create_cfg(CONF)
        exit(0)

    moo = MailCow()
    # add `--fields` argument before creating menu
    for section, modifiers in moo.endpoints.items():
        if 'get' in modifiers:
            moo.endpoints[section]['get'].update(FIELDS)
    args = menu(moo.endpoints)
    args_as_dict = vars(args)

    debug_mailcow(args.debug)
    debug_msg(f'ArgParse Object: {args}')
    for msg in [f'MailCow Server: {moo.server}',
                f'MailCow Server URL: {moo.url}']:
        debug_msg(msg)

    if args.modifier == 'delete':
        moo.data = moo.deleteRequest(args.section, args.items)

    if args.modifier == 'get':
        moo.data = moo.getRequest(
            prepare_getRequest(**args_as_dict, endpoints=moo.endpoints))

    attrs = build_attributes(**args_as_dict, endpoints=moo.endpoints)
    debug_msg(f'Attributes build: {attrs}')

    if args.modifier == 'add':
        # /api/v1/add/transport/all - The only API endpoint that differ in uri
        if args.section == 'transport':
            section = 'transport/all'
        else:
            section = args.section

        moo.data = moo.addRequest(section, attrs)

    if args.modifier == 'edit':
        # /api/v1/edit/mailq - The only API endpoint that's payload differ
        if args.section == 'mailq' and args.flush:
            moo.data = moo.editRequest(args.section, action='flush')
        else:
            moo.data = moo.editRequest(args.section, args.items, attrs)

    if moo.data:
        if args.yaml:
            print(moo.as_yaml())

        if args.json and not args.yaml:
            print(moo.as_json())

        if args.table and not (args.yaml or args.json):
            tables = moo.as_table(vertical=args.vertical)

            for table in tables:
                fields = parse_fields(
                    args_as_dict.get('fields'),
                    args.vertical)

                if fields:
                    print(table.get_string(fields=fields))
                else:
                    print(table)


if __name__ == '__main__':
    main()
