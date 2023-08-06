#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function, absolute_import

import shlex
import click

from click_project.lib import ParameterType, quote
from click_project.config import config
from click_project.completion import startswith
from click_project.overloads import option


class LauncherCommandType(ParameterType):
    def complete(self, ctx, incomplete):
        choices = [
            " ".join([quote(v) for v in value])
            for value in config.settings.get("launchers", {}).values()
        ]
        return [
            launcher
            for launcher in choices
            if startswith(launcher, incomplete)
        ]

    def convert(self, value, param, ctx):
        return shlex.split(value)


class LauncherType(ParameterType):
    def __init__(self, missing_ok=False):
        ParameterType.__init__(self)
        self.missing_ok = missing_ok

    def complete(self, ctx, incomplete):
        choices = config.settings.get("launchers", {}).keys()
        return [
            launcher
            for launcher in choices
            if startswith(launcher, incomplete)
        ]

    def convert(self, value, param, ctx):
        if self.missing_ok:
            return value
        choices = config.settings.get("launchers", {}).keys()
        if value not in choices:
            self.fail('invalid choice: %s. (choose from %s)' %
                      (value, ', '.join(choices)), param, ctx)
        return value


def launcher(func):
    """Option decorator fer the commands using a launcher"""
    opts = [
        option("--launcher-command", help=(
            "Extra arguments to prepend to the simulation command."
            " Ignored if --launcher is given."),
               type=LauncherCommandType(),
               group="launcher"),
        option("-l", "--launcher", help=(
            "Name of the launcher to prepend to the simulation command."
            " It overrides --launcher-command."
            " See the launchers commands for more information"),
               type=LauncherType(),
               group="launcher")
    ]
    for opt in reversed(opts):
        func = opt(func)
    return func
