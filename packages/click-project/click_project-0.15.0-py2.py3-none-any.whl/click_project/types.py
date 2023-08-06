#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import click

from click_project.config import config
from click_project.core import DynamicChoiceType as DynamicChoice # NOQA: just expose the object


class Suggestion(click.Choice):
    def convert(self, value, param, ctx):
        return value

    def get_metavar(self, param):
        return "[{}|...]".format("|".join(self.choices))

    def get_missing_message(self, param):
        return (
            "Either choose from:\n\t{}."
            " or provide a new one".format(",\n\t".join(self.choices))
        )


class ProfileType(DynamicChoice):
    def choices(self):
        return self.profiles.keys()

    @property
    def profiles(self):
        return {
            profile.name: profile
            for profile in config.all_profiles
        }

    def converter(self, value):
        return self.profiles[value]


class DirectoryProfileType(ProfileType):
    @property
    def profiles(self):
        from click_project.profile import DirectoryProfile
        return {
            name: profile
            for name, profile in super().profiles.items()
            if isinstance(profile, DirectoryProfile)
        }
