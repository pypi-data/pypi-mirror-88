# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

import os
from thead_tools import *


class Toolchain(Command):
    common = True
    helpSummary = "Install toolchain"
    helpUsage = """
%prog [--all] [--csky] [--riscv]
"""
    helpDescription = """
Install toolchain.
"""

    def _Options(self, p):
        p.add_option('-c', '--csky',
                     dest='install_csky', action='store_true',
                     help=' install csky toolchain')
        p.add_option('-r', '--riscv',
                     dest='install_riscv', action='store_true',
                     help=' install riscv toolchain')
        p.add_option('-a', '--all',
                     dest='install_all', action='store_true',
                     help=' install csky toolchain and riscv toolchain')

        p.add_option('-o', '--output',
                     dest='output', action='store', type='str', default=None,
                     help=' install target directory')

    def Execute(self, opt, args):
        need_usage = True
        tool = ToolchainYoC(opt.output)
        if opt.install_all:
            tool.check_toolchain('csky-linux', 1)
            tool.check_toolchain('riscv64-linux', 1)
            need_usage = False
        else:
            if opt.install_csky:
                tool.check_toolchain('csky-linux', 1)
                need_usage = False
            if opt.install_riscv:
                tool.check_toolchain('riscv64-linux', 1)
                need_usage = False
        if need_usage:
            self.Usage()
