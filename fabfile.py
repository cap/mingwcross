#!/usr/bin/env python

import os
import subprocess
from fabric.api import *


WIN_PATH = '/home/cap/win'
BUILD_PATH = os.path.abspath(os.getcwd())

PACKAGES = [
    'alien',
    'cmake',
    'g++-4.7',
    'git',
    'libboost1.53-all-dev',
    'libsdl-image1.2-dev',
    'libsdl1.2-dev',
    'libyaml-dev',
    'python-dev',
    'python-numpy',
    'virtualenvwrapper',
    ]

FILES = {
    'mingw': (
        'http://downloads.sourceforge.net/project/mingw-w64/'
        'Toolchains%20targetting%20Win64/Automated%20Builds/',
        'mingw-w64-bin_x86_64-linux_20130615.tar.bz2',
        ''),
    'libpng': (
        'http://prdownloads.sourceforge.net/libpng/libpng-1.6.2.tar.gz',
        'libpng-1.6.2.tar.gz',
        'libpng-1.6.2',),
    'sdl': (
        'http://www.libsdl.org/release/',
        'SDL-1.2.15.tar.gz',
        'SDL-1.2.15'),
    'sdl_image': (
        'http://www.libsdl.org/projects/SDL_image/release/',
        'SDL_image-1.2.12.tar.gz',
        'SDL_image-1.2.12'
        ),
    'yaml': (
        'https://yaml-cpp.googlecode.com/files/',
        'yaml-cpp-0.5.1.tar.gz',
        'yaml-cpp-0.5.1'),
    'zlib': (
        'http://zlib.net/',
        'zlib-1.2.8.tar.gz',
        'zlib-1.2.8'),
    }


def _autoconf(pkg):
    _autoconf_configure(pkg)
    _autoconf_build(pkg)


def _autoconf_configure(pkg):
    url, name, path = FILES[pkg]
    build_path = os.path.join(BUILD_PATH, path, 'build')
    conf_path = os.path.join(BUILD_PATH, '..', pkg, 'cross-configure')
    bin_path = os.path.join(WIN_PATH, 'bin')
    local('mkdir -p {}'.format(build_path))
    local('cp {} {}'.format(conf_path, build_path))
    local('export PATH={}:$PATH && '
          'cd {} && ./cross-configure'.format(
            bin_path, build_path))


def _autoconf_build(pkg):
    url, name, path = FILES[pkg]
    build_path = os.path.join(BUILD_PATH, path, 'build')
    bin_path = os.path.join(WIN_PATH, 'bin')
    local('export PATH={}:$PATH && '
          'cd {} && make && make install'.format(
            bin_path, build_path))


def _cmake(pkg):
    url, name, path = FILES[pkg]
    build_path = os.path.join(BUILD_PATH, path, 'build')
    conf_path = os.path.join(BUILD_PATH, '..', 'cmake', 'cross-configure')
    local('mkdir -p {}'.format(build_path))
    local('cp {} {}'.format(conf_path, build_path))
    local('cd {} && ./cross-configure && make && make install'.format(
            build_path))


def download():
    for url, name, path in FILES.itervalues():
        local('wget {}{}'.format(url, name))


def extract():
    for url, name, path in FILES.itervalues():
        if not 'mingw' in name:
            local('tar xzf {}'.format(name))


def zlib():
    _cmake('zlib')


def libpng():
    _cmake('libpng')


def sdl():
    _autoconf('sdl')


def sdl_image():
    pkg = 'sdl_image'
    _autoconf_configure(pkg)

    url, name, path = FILES[pkg]
    build_path = os.path.join(BUILD_PATH, path, 'build')
    make_path = os.path.join(build_path, 'Makefile')
    with open(make_path) as fd:
        make = fd.read()
    with open(make_path, 'wb') as fd:
        fd.write(make.replace('-lz', '-lzlib'))

    _autoconf_build(pkg)


def yaml():
    _cmake('yaml')


def boost():
    include_path = os.path.join(WIN_PATH, 'include')
    local('cp -r /usr/include/boost {}'.format(include_path))


def mingw():
    url, name, path = FILES['mingw']
    local('mkdir -p {} && cd {} && tar xjf {}'.format(
            WIN_PATH,
            WIN_PATH,
            os.path.join(BUILD_PATH, name)))


def packages():
    local('sudo apt-get install -y {}'.format(' '.join(PACKAGES)))


def all():
    packages()
    download()
    extract()
    mingw()
    boost()
    yaml()
    zlib()
    libpng()
    sdl()
    sdl_image()
