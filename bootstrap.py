#!/usr/bin/env python
## -*- coding: utf-8 -*-
"""Create a custom "virtual" Python installation
"""

import virtualenv

from os.path import join as path_join
from tempfile import mkdtemp
from subprocess import call as subprocess_call
from shutil import rmtree

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen  # NOQA

tmp_dir = None


def local_adjust_options(options, args):
    global tmp_dir

    tmp_dir = mkdtemp()
    print('download setuptools...')
    f = open(path_join(tmp_dir, 'setuptools-latest.tar.gz'), 'w')
    f.write(urlopen('https://pypi.python.org/packages/source/s/setuptools/setuptools-5.3.tar.gz#md5=f4e0aa872b3e64de38c5acb478c9452b').read())  # NOQA
    f.close()
    print('setuptools downloaded')

    print('download pip...')
    f = open(path_join(tmp_dir, 'pip-latest.tar.gz'), 'w')
    f.write(urlopen('https://pypi.python.org/packages/source/p/pip/pip-1.5.6.tar.gz#md5=01026f87978932060cc86c1dc527903e').read())  # NOQA
    f.close()
    print('pip downloaded')

    if len(args) == 0:
        options.search_dirs = [tmp_dir]
        args.append('.')


def local_after_install(options, home_dir):
    global tmp_dir

    subprocess_call([
        path_join('bin', 'pip'),
        'install', '-r', 'devel-requirements.txt'
    ])

    rmtree(tmp_dir)

# Monkey patch
virtualenv.adjust_options = local_adjust_options
virtualenv.after_install = local_after_install


virtualenv.main()
