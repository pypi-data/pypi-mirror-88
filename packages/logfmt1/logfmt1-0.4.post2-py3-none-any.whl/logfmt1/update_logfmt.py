#!/usr/bin/env python3
# encoding: utf-8
# title: update-logfmt
# description: invoke ./share/update/* scripts
# type: virtual
#
# Stub that reimplements run-parts

import os, re

def main():
    pass

for dir in ["/usr/share/logfmt/update", re.sub("[.\w]+$", "share/update", __file__)]:
    if os.path.exists(dir):
        os.system(f"run-parts {dir}")
        break
