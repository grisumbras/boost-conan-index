#!/usr/bin/env python

#
# Copyright (c) 2025 Dmitry Arkhipov (grisumbras@yandex.ru)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#


import argparse
import os
import os.path
import shutil
import sys
import yaml


def main(argv, FS):
    args = parse_args(argv)

    fs = FS()
    for src_root, dirs, files in fs.walk(args.src):
        if files:
            rel_path = os.path.relpath(src_root, start=args.src)
            tgt_root = os.path.join(args.tgt, rel_path)
            fs.create_path(tgt_root)
        for file in files:
            update_file(
                os.path.join(src_root, file), os.path.join(tgt_root, file), fs,
            )


class FileSystem():
    @staticmethod
    def open(path, mode='r'):
        return open(path, mode, encoding='utf-8', errors='replace')

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def walk(path):
        return os.walk(path)

    @staticmethod
    def create_path(path):
        return os.makedirs(path, exist_ok=True)

    @staticmethod
    def copy_file(src_path, tgt_path):
        shutil.copyfile(src_path, tgt_path)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='Update one Conan recipe index from another.',
    )
    parser.add_argument('src', help=f'directory with the new recipes')
    parser.add_argument('tgt', help=f'directory with the old recipes')
    return parser.parse_args(argv[1:])


def update_file(src_path, tgt_path, fs):
    if not fs.exists(tgt_path) or os.path.splitext(src_path)[1] != '.yml':
        fs.copy_file(src_path, tgt_path)
        return

    with fs.open(src_path, 'r') as src_file:
        src =  yaml.load(src_file, yaml.Loader)
        with fs.open(tgt_path, 'r') as tgt_file:
            tgt =  yaml.load(tgt_file, yaml.Loader)
            data = merge_data(src, tgt)
        with fs.open(tgt_path, 'w') as tgt_file:
            yaml.dump(data, tgt_file)


def merge_data(src, tgt):
    if not isinstance(src, dict) or not isinstance(tgt, dict):
        return src

    for k in src:
        tgt[k] = merge_data(src[k], tgt.get(k))
    return tgt


if __name__ == '__main__':
    main(sys.argv, FileSystem)
