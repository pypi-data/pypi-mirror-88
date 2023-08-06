#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function, absolute_import

from click_project.log import get_logger
from click_project.config import config
from click_project.core import run


LOGGER = get_logger(__name__)


def run_triggers(name, path, commands):
    if commands:
        LOGGER.debug("Running the {} trigger for {}".format(name, path))
    for command in commands:
        if isinstance(command, type(lambda x: x)):
            command()
        else:
            run(command)


class TriggerMixin(object):
    def invoke(self, *args, **kwargs):
        trigger = config.settings2.get("triggers", {}).get(self.path, {})
        pre = trigger.get("pre", [])
        post = trigger.get("post", [])
        onsuccess = trigger.get("onsuccess", [])
        onerror = trigger.get("onerror", [])
        run_triggers("pre", self.path, pre)
        try:
            res = super(TriggerMixin, self).invoke(*args, **kwargs)
        except:  # NOQA: E722
            run_triggers("onerror", self.path, onerror)
            run_triggers("post", self.path, post)
            raise
        run_triggers("onsuccess", self.path, onsuccess)
        run_triggers("post", self.path, post)
        return res
