#!/usr/bin/env python

# Copyright (c) 2021 Jean-Denis Gebhardt <projects@der-jd.de>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from os import path, makedirs
from configparser import ConfigParser


def set_config_parser():
    return ConfigParser(default_section='defaults')


def expand_path(fnc):
    def expand(*args):
        return fnc(path.expanduser(args[0]))

    return expand


@expand_path
def find_cfg(file):
    exists = path.exists(file)

    if not exists:
        raise IOError(
            f'Could not find {file}.'
            f'Run {__file__} --create-example-config and try again!')

    return exists


@expand_path
def load_cfg(file):
    config = set_config_parser()
    config.read(file)

    return config


@expand_path
def create_cfg(file):
    if path.exists(file):
        raise IOError(f'File {file} already exists!')
    else:
        makedirs(path.dirname(file), exist_ok=True)

        config = set_config_parser()
        config.read_dict({
            'defaults': {
                'server': 'mail.example.com',
                'ssl_verify': True,
                'timeout': 15
            },
            'mail.example.com': {
                'url': 'https://mail.example.com',
                'token': '123456-abcde-123456-abcde-123456'
            }
        })

        with open(file, 'w') as configfile:
            config.write(configfile)
