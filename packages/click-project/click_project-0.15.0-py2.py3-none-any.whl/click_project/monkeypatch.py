#!/usr/bin/env python
# -*- coding:utf-8 -*-

from click import Context


old_lookup_default = Context.lookup_default


def context_lookup_default(self, name):
    if not hasattr(self, "click_project_default_catch"):
        self.click_project_default_catch = set()
    self.click_project_default_catch.add(name)
    return old_lookup_default(self, name)


def do():
    Context.lookup_default = context_lookup_default
