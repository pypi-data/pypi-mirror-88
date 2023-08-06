#!/usr/bin/env python3
# encoding: utf-8
# title: update-logfmt
# description: invoke ./share/update/* scripts
# type: virtual
#
# Stub that reimplements run-parts

import os, re

for dir in [re.sub("[.\w]+$", "share/update", __file__), "/usr/share/logfmt/update"]:
    if os.path.exists(dir):
        os.system(f"run-parts {dir}")
        break
