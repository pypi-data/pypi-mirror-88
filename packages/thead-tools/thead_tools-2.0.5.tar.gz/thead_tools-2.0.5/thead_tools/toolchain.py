# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

import os
import stat
import tarfile
import subprocess
import platform
import codecs
from hashlib import md5, sha1

from .tools import *


toolchain_url_64 = "https://occ-oss-prod.oss-cn-hangzhou.aliyuncs.com/resource/1356021/1606905847044/csky-linux-gnuabiv2-tools-x86_64-glibc-linux-4.9.56-20201126.tar.gz"
toolchain_url_32 = "https://occ-oss-prod.oss-cn-hangzhou.aliyuncs.com/resource/1356021/1606898555130/csky-linux-gnuabiv2-tools-i386-glibc-linux-4.9.56-20201126.tar.gz"

rsicv_url_64 = 'https://occ-oss-prod.oss-cn-hangzhou.aliyuncs.com/resource/1836682/1606703449534/riscv64-linux-x86_64-20201104.tar.gz'
rsicv_url_32 = 'https://occ-oss-prod.oss-cn-hangzhou.aliyuncs.com/resource/1836682/1606703269535/riscv64-linux-i386-20201104.tar.gz'

arm_url_64 = 'http://yoctools.oss-cn-beijing.aliyuncs.com/gcc-arm-none-eabi-9-2020-q2-update-x86_64-linux.tar.gz'
arm_url_32 = ''

all_toolchain_url = {
    'csky-linux': [toolchain_url_32, toolchain_url_64],
    'riscv64-linux': [rsicv_url_32, rsicv_url_64],
}

all_toolchain_sha1 = {
    'csky-linux': ['', ''],
    'riscv64-linux': ['', 'dd8f0e8c5f1f61fe7690b6f84ac7f55e26696f86'],
}

def FileSHA1(filename):
    sha1Obj = sha1()
    with open(filename, 'rb') as f:
        sha1Obj.update(f.read())
    return sha1Obj.hexdigest()

class ToolchainYoC:
    def __init__(self, base_path = ''):
        if base_path:
            self.basepath = base_path
        else:
            if os.getuid() != 0:
                self.basepath = home_path('.thead')
            else:
                self.basepath = '/usr/local/thead/'


    def download(self, arch):
        sha1_str = ''
        need_download = True
        toolchain_path = os.path.join(self.basepath, arch)

        if os.path.exists(toolchain_path) or arch not in all_toolchain_url:
            put_string("toolchain exists: %s" % toolchain_path)
            return

        architecture = platform.architecture()
        if architecture[0] == '64bit':
            toolchain_url = all_toolchain_url[arch][1]
            sha1_str = all_toolchain_sha1[arch][1]
        else:
            toolchain_url = all_toolchain_url[arch][0]
            sha1_str = all_toolchain_sha1[arch][0]
        if not toolchain_url:
            put_string("Url is empty!")
            return

        tar_path = '/tmp/' + os.path.basename(toolchain_url)
        if os.path.isfile(tar_path) and sha1_str:
            if FileSHA1(tar_path) == sha1_str:
                need_download = False
        if need_download:
            put_string("Start to download toolchain: %s" % arch)
            wget(toolchain_url, tar_path)
            put_string("")
            new_sha1 = FileSHA1(tar_path)
            if new_sha1 == sha1_str:
                put_string("%s sha1 error, %s != %s" %s (tar_path, new_sha1, sha1_str))
                exit(-1)
        put_string("Start install, wait half a minute please.")
        if tar_path.endswith('.bz2'):
            with tarfile.open(tar_path, 'r:bz2') as tar:
                tar.extractall(toolchain_path)
        elif tar_path.endswith('.gz'):
            with tarfile.open(tar_path, 'r:gz') as tar:
                tar.extractall(toolchain_path)
        else:
            put_string("%s extra not support." % tar_path)
            return

        # os.remove(tar_path)
        put_string("Congratulations!")
        if os.getuid() == 0:
            self.link_bin(toolchain_path)
        else:
            self.update_env(arch)

    def link_bin(self, toolchain_path):
        toolchain_bin = os.path.join(toolchain_path, 'bin')
        files = os.listdir(toolchain_bin)

        for fil in files:
            p = os.path.join(toolchain_bin, fil)
            if os.path.isfile(p):
                if os.stat(p).st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) != 0:
                    try:
                        os.symlink(p, os.path.join(
                            '/usr/bin', os.path.basename(p)))
                    except FileExistsError:
                        pass
                    except PermissionError:
                        put_string("Please use: sudo", ' '.join(sys.argv))
                        exit(-1)
                    except Exception as e:
                        pass

    def update_env(self, arch):
        toolchain_path = '$HOME/.thead/%s/bin' % arch
        shell = os.getenv('SHELL')
        shell = os.path.basename(shell)

        if shell == 'zsh':
            rc = home_path('.zshrc')

        elif shell == 'bash':
            rc = home_path('.bashrc')

        with codecs.open(rc, 'r', 'UTF-8') as f:
            contents = f.readlines()

        export_path = ''
        for i in range(len(contents)):
            c = contents[i]
            idx = c.find(' PATH')
            if idx > 0:
                idx = c.find('=')
                if idx >= 0:
                    export_path = c[idx + 1:]

                    if export_path.find(toolchain_path) < 0:
                        export_path = 'export PATH=' + toolchain_path + ':' + export_path
                        contents[i] = export_path

        if not export_path:
            contents.insert(0, 'export PATH=' + toolchain_path + ':$PATH\n\n')

        with codecs.open(rc, 'w', 'UTF-8') as f:
            contents = f.writelines(contents)
        put_string("please run command:\n  source %s" % rc)

    def check_toolchain(self, arch='csky-abiv2-elf', verbose=0):
        bin_file = self.check_program(arch)
        if bin_file == '':
            self.download(arch)
            bin_file = self.check_program(arch)
        else:
            if verbose == 1:
                put_string('warn: the toolchains was installed already, path = %s.' % bin_file)
        return bin_file

    def which(self, cmd):
        gcc = subprocess.Popen('which ' + cmd, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = gcc.stdout.readlines()
        for text in lines:
            text = text.decode().strip()
            info = 'which: no ' + os.path.basename(cmd) + ' in'
            if not text.find(info) >= 0:
                return text
        return ''

    def check_program(self, arch='csky-abiv2-elf'):
        path = self.which(arch + '-gcc')
        if path == '':
            path = home_path('.thead/' + arch + '/bin/' + arch + '-gcc')
            path = self.which(path)
            return path
        else:
            return path
