#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pathlib import Path

import os
import json

import click

from click_project.decorators import (
    argument,
    group,
    use_settings,
    table_format,
    table_fields,
    flag,
    option,
)
from click_project.config import config, merge_settings
from click_project.lib import quote, TablePrinter, call, makedirs, rm, chmod, createfile, move
from click_project.colors import Colorer
from click_project.log import get_logger
from click_project.core import DynamicChoiceType, cache_disk
from click_project.externalcommands import ExternalCommandResolver
from click_project.customcommands import CustomCommandResolver
from click_project.overloads import (
    CommandSettingsKeyType, CommandType,
    get_command, Option, Argument
)
from click_project.flow import get_flow_commands_to_run
from click_project.types import DirectoryProfileType


LOGGER = get_logger(__name__)


class CustomCommandPathType(DynamicChoiceType):
    def __init__(self, type):
        self.type = type

    def choices(self):
        _, settings = merge_settings(config.iter_settings(explicit_only=True))
        return settings["customcommands"].get(self.type, [])


class CustomCommandNameType(DynamicChoiceType):
    def __init__(self):
        self.resolvers = [
            ExternalCommandResolver(),
            CustomCommandResolver(),
        ]

    def choices(self):
        return sum(
            [
                resolver._list_command_paths()
                for resolver in self.resolvers
            ],
            []
        )


class CustomCommandType(CustomCommandNameType):
    def converter(self, path):
        for resolver in self.resolvers:
            if path in resolver._list_command_paths():
                return resolver._get_command(path)
        raise Exception(f"Could not find a resolver matching {path}")


class CustomCommandConfig:
    pass


def format_paths(path):
    return " ".join(map(quote, path))


@group(default_command="show")
@use_settings("customcommands", CustomCommandConfig, override=False)
def customcommands():
    """Manipulate paths where to find extra commands"""


@customcommands.command()
@Colorer.color_options
@table_format(default='key_value')
@table_fields(choices=['name', 'paths'])
def show(fields, format, **kwargs):
    """Show all the custom commands paths"""
    with Colorer(kwargs) as colorer, TablePrinter(fields, format) as tp:
        values = {
            profile.name: format_paths(
                config.customcommands.all_settings.get(
                    profile.name, {}
                ).get(
                    "pythonpaths", []
                )
            )
            for profile in config.all_enabled_profiles
        }
        args = colorer.colorize(values, config.customcommands.readprofile)
        tp.echo("pythonpaths", " ".join(args))
        values = {
            profile.name: format_paths(
                config.customcommands.all_settings.get(
                    profile.name, {}
                ).get(
                    "executablepaths", []
                )
            )
            for profile in config.all_enabled_profiles
        }
        args = colorer.colorize(values, config.customcommands.readprofile)
        tp.echo("executablepaths", " ".join(args))


def custom_command_type():
    return option("--type", help="What kind of object should I find at this locations",
                  type=click.Choice(["executable", "python"]),
                  default="external")


@customcommands.command()
@argument("paths", nargs=-1, type=Path, help="The paths to add to load custom commands")
@custom_command_type()
def add_path(paths, type):
    """Add custom command paths"""
    paths = [str(d) for d in paths]
    config.customcommands.writable[f"{type}paths"] = config.customcommands.writable.get("{type}paths", []) + list(paths)
    config.customcommands.write()
    LOGGER.info(f"Added {format_paths(paths)} ({type}) to the profile {config.customcommands.writeprofile}")


@customcommands.command()
@argument("paths", nargs=-1, type=CustomCommandPathType("pythonpaths"), help="The paths to remove from custom commands")
@custom_command_type()
def remove_path(paths, type):
    """Remove all the custom commands paths from the profile"""
    to_remove = set(config.customcommands.writable.get(f"{type}paths", [])).intersection(paths)
    if not to_remove:
        raise click.UsageError(
            "None of the given path is present. This command would be a no-op."
        )
    config.customcommands.writable[f"{type}paths"] = [
        path for path in config.customcommands.writable.get(f"{type}paths", [])
        if path not in to_remove
    ]
    config.customcommands.write()
    LOGGER.info(f"Removed {format_paths(to_remove)} ({type}) from the profile {config.customcommands.writeprofile}")


@customcommands.command()
@argument("customcommand",
          type=CustomCommandType(),
          help="The custom command to consider")
def which(customcommand):
    """Print the location of the given custom command"""
    print(customcommand.customcommand_path)


@customcommands.command()
@argument("customcommand",
          type=CustomCommandType(),
          help="The custom command to consider")
@flag("--force", help="Don't ask for confirmation")
def remove(force, customcommand):
    """Remove the given custom command"""
    path = Path(customcommand.customcommand_path)
    if force or click.confirm(f"This will remove {path}, are you sure ?"):
        rm(path)


@customcommands.command()
@argument("customcommand",
          type=CustomCommandType(),
          help="The custom command to consider")
def edit(customcommand):
    """Edit the given custom command"""
    path = Path(customcommand.customcommand_path)
    click.edit(filename=path)


class AliasesType(DynamicChoiceType):
    def choices(self):
        return list(config.settings["alias"].keys())


@customcommands.group()
def create():
    """Create custom commands directly from the command line."""


@create.command()
@argument(
    "name",
    help="The name of the new command"
)
@flag("--open/--no-open", help="Also open the file after its creation", default=True)
@flag("--force", help="Overwrite a file if it already exists")
@option("--body", help="The initial body to put", default="")
@option("--from-alias", help="The alias to use as base", type=AliasesType())
@option("--flowdeps", help="Add a flowdeps", multiple=True, type=CommandType())
@option("--description", help="The initial description to put", default="Description")
@option("--source-bash-helpers/--no-source-bash-helpers",
        help="Source the bash helpers",
        default=True
)
def bash(name, open, force, description, body, from_alias, flowdeps, source_bash_helpers):
    """Create a bash custom command"""
    if not name.endswith(".sh"):
        name += ".sh"
    script_path = Path(config.customcommands.profile.location) / "bin" / name
    makedirs(script_path.parent)
    if script_path.exists() and not force:
        raise click.UsageError(
            f"Won't overwrite {script_path} unless"
            " explicitly asked so with --force"
        )
    options = []
    arguments = []
    flags = []
    remaining = ""
    args = ""

    if from_alias:
        if body:
            body = body + "\n"
        body = body + "\n".join(
            config.main_command.path + " " + " ".join(map(quote, command))
            for command in config.settings["alias"][from_alias]["commands"]
        )
        flowdeps = list(flowdeps) + get_flow_commands_to_run(from_alias)
        alias_cmd = get_command(from_alias)
        if description:
            description = description + "\n"
        description = description + f"Converted from the alias {from_alias}"

        def guess_type(param):
            if type(param.type) == click.Choice:
                return json.dumps(list(param.type.choices))
            elif param.type == int:
                return "int"
            elif param.type == float:
                return "float"
            else:
                return "str"

        for param in alias_cmd.params:
            if type(param) == Option:
                if param.is_flag:
                    flags.append(f"F:{','.join(param.opts)}:{param.help}:{param.default}")
                    args += f"""
if [ "${{{config.main_command.path.upper()}___{param.name.upper()}}}" == "True" ]
then
    args+=({param.opts[-1]})
fi"""
                else:
                    options.append(f"O:{','.join(param.opts)}:{guess_type(param)}:{param.help}")
                    args += f"""
if [ -n "${{{config.main_command.path.upper()}___{param.name.upper()}}}" ]
then
    args+=({param.opts[-1]} "${{{config.main_command.path.upper()}___{param.name.upper()}}}")
fi"""
            elif type(param) == Argument:
                if param.nargs == -1:
                    remaining = param.help
                else:
                    arguments.append(f"A:{','.join(param.opts)}:{guess_type(param)}:{param.help}")
                    args += f"""
args+=("${{{config.main_command.path.upper()}___{param.name.upper()}}}")
"""
        if args:
            args = """# Build the arguments of the last command of the alias
args=()""" + args
            body += ' "${args[@]}"'
        if remaining:
            body += ' "${@}"'

    if flowdeps:
        flowdeps_str = "flowdepends: " + ", ".join(flowdeps) + "\n"
    else:
        flowdeps_str = ""
    if options:
        options_str = "\n".join(options) + "\n"
    else:
        options_str = ""
    if arguments:
        arguments_str = "\n".join(arguments) + "\n"
    else:
        arguments_str = ""
    if flags:
        flags_str = "\n".join(flags) + "\n"
    else:
        flags_str = ""
    if remaining:
        remaining_str = f"N:{remaining}\n"
    else:
        remaining_str = ""

    script_path.write_text(f"""#!/bin/bash -eu

source "${{CLK_INSTALL_LOCATION}}/commands/customcommands/_clk.sh"

clk_usage () {{
    cat<<EOF
$0

{description}
--
{flowdeps_str}{options_str}{flags_str}{arguments_str}{remaining_str}
EOF
}}

clk_help_handler "$@"

{args}
{body}
""")
    chmod(script_path, 0o755)
    if open:
        click.edit(filename=str(script_path))


@create.command()
@argument(
    "name",
    help="The name of the new command"
)
@flag("--open/--no-open", help="Also open the file after its creation", default=True)
@flag("--force", help="Overwrite a file if it already exists")
@option("--body", help="The initial body to put", default="")
@option("--description", help="The initial description to put", default="Description")
def python(name, open, force, description, body):
    """Create a bash custom command"""
    if not name.endswith(".py"):
        name += ".py"
    script_path = Path(config.customcommands.profile.location) / "python" / name
    makedirs(script_path.parent)
    if script_path.exists() and not force:
        raise click.UsageError(
            f"Won't overwrite {script_path} unless"
            " explicitly asked so with --force"
        )
    command_name = script_path.name[:-len(".py")]
    script_path.write_text(f"""#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pathlib import Path

import click

from click_project.decorators import (
    argument,
    flag,
    option,
    command,
    use_settings,
    table_format,
    table_fields,
)
from click_project.lib import (
    TablePrinter,
    call,
)
from click_project.config import config
from click_project.log import get_logger
from click_project.types import DynamicChoice


LOGGER = get_logger(__name__)


@command()
def {command_name}():
   "{description}"
   {body}
""")
    if open:
        click.edit(filename=str(script_path))


@customcommands.command()
@argument("customcommand",
          type=CustomCommandType(),
          help="The custom command to consider")
@argument("new-name", help="The new name to use for the custom command")
@flag("--force", help="Overwrite destination")
def rename(customcommand, new_name, force):
    """Rename a custom commands"""
    ext = os.path.splitext(customcommand.customcommand_path)[1]
    if not new_name.endswith(ext):
        new_name += ext
    new_path = Path(customcommand.customcommand_path).parent / new_name
    if new_path.exists() and not force:
        raise click.UsageError(
            f"I won't overwrite {new_path},"
            " unless called with --force"
        )
    Path(customcommand.customcommand_path).rename(new_path)
    LOGGER.status(f"Renamed {customcommand.customcommand_path} into {new_path}")


@customcommands.command()
@argument("customcommand",
          type=CustomCommandType(),
          help="The custom command to move")
@argument("profile",
          type=DirectoryProfileType(),
          help="The profile where to move the command")
@flag("--force", help="Overwrite destination")
def _move(customcommand, profile, force):
    """Move a custom commands"""
    new_location = Path(profile.location) / "bin" / Path(customcommand.customcommand_path).name
    if new_location.exists() and not force:
        raise click.UsageError(
            f"I won't overwrite {new_location},"
            " unless called with --force"
        )
    makedirs(new_location.parent)
    move(customcommand.customcommand_path, new_location)
    LOGGER.status(f"Moved {customcommand.customcommand_path} into {new_location}")


@customcommands.command()
def list():
    """List the path of all custom commands."""
    type = CustomCommandType()

    @cache_disk(expire=600)
    def customcommand_path(command_path):
        return type.converter(command_path).customcommand_path

    for path in type.choices():
        print(customcommand_path(path))
