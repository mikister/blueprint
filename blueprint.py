#!/usr/bin/python3

import subprocess
import os
import click
from distutils.dir_util import copy_tree, remove_tree
import re


# The path where blueprints are stored
BLUEPRINT_DATA_PATH = os.path.expanduser("~") + "/.blueprint/"


class DefaultGroup(click.Group):
    """Modified version the default group that allows for setting of a default command."""

    ignore_unknown_options = True

    def __init__(self, *args, **kwargs):
        default_command = kwargs.pop('default_command', None)
        super(DefaultGroup, self).__init__(*args, **kwargs)
        self.default_cmd_name = None
        if default_command is not None:
            self.set_default_command(default_command)

    def set_default_command(self, command):
        if isinstance(command, str):
            cmd_name = command
        else:
            cmd_name = command.name
            self.add_command(command)
        self.default_cmd_name = cmd_name

    def parse_args(self, ctx, args):
        if not args and self.default_cmd_name is not None:
            args.insert(0, self.default_cmd_name)
        return super(DefaultGroup, self).parse_args(ctx, args)

    def get_command(self, ctx, cmd_name):
        if cmd_name not in self.commands and self.default_cmd_name is not None:
            ctx.args0 = cmd_name
            cmd_name = self.default_cmd_name
        return super(DefaultGroup, self).get_command(ctx, cmd_name)

    def resolve_command(self, ctx, args):
        cmd_name, cmd, args = super(
            DefaultGroup, self).resolve_command(ctx, args)
        args0 = getattr(ctx, 'args0', None)
        if args0 is not None:
            args.insert(0, args0)
        return cmd_name, cmd, args


@click.group(cls=DefaultGroup, default_command='blueprint')
@click.pass_context
def cli(ctx):
    pass


# ---------------------------------------------------
#                User exposed commands
# ---------------------------------------------------


@cli.command()
@click.argument('name')
def blueprint(name):
    """Create a local copy of blueprint contents."""
    copy_tree(BLUEPRINT_DATA_PATH + name, os.getcwd())


@cli.command()
@click.argument('name')
@click.option('--no-file-explorer', '-nfe', is_flag=True, help='Doesn\'t open the file explorer')
@click.option('-cwd', is_flag=True, help='Copy contents of the current directory to the new blueprint')
def create(name, no_file_explorer, cwd):
    """Create a new blueprint."""
    if not blueprint_exists(name):
        os.makedirs(BLUEPRINT_DATA_PATH + name)

    if not no_file_explorer:
        subprocess.call("xdg-open " + BLUEPRINT_DATA_PATH + name, shell=True)
    
    if cwd:
        copy_tree(os.getcwd(), BLUEPRINT_DATA_PATH + name)


@cli.command()
@click.argument('name')
def getpath(name):
    """Print the absolute path to blueprint contents."""
    if blueprint_exists(name):
        print(BLUEPRINT_DATA_PATH + name)
    else:
        print("Blueprint doesn't exist!")


@cli.command()
@click.argument('name')
def delete(name):
    """Delete a blueprint."""
    if blueprint_exists(name):
        remove_tree(BLUEPRINT_DATA_PATH + name)


@cli.command()
@click.argument('name')
def showfiles(name):
    """Print contents of a blueprint."""
    print("Showing file for blueprint: " + name)
    if blueprint_exists(name):
        files = os.listdir(BLUEPRINT_DATA_PATH + name)
        for ff in files:
            ftype = " "
            filepath = BLUEPRINT_DATA_PATH + name + "/" + ff
            if os.path.isdir(filepath):
                ftype = "D"
            elif os.path.isfile(filepath):
                ftype = "F"
            print("   " + ftype + " | " + ff)


@cli.command()
@click.argument('regexing', nargs=-1, required=False)
def list(regexing):
    """List all blueprints that match a regex query."""
    if regexing:
        regexQuerry = regexing[0]
    else:
        regexQuerry = ".*"

    regex = re.compile(regexQuerry)

    blueprints_list = os.listdir(BLUEPRINT_DATA_PATH)
    blueprints_list.sort()

    # Edge case check in case there are no blueprints created
    if len(blueprints_list) == 0:
        print("There are no existing blueprints!")
        return None

    print("\nAvaiable blueprints:")

    maxNameSize = max([len(blp) for blp in blueprints_list])
    indexPadSize = len(str(len(blueprints_list))) + 1

    print(" i".ljust(indexPadSize) + " │ " + "name".ljust(maxNameSize) + " │ size")
    print("──".ljust(indexPadSize, "─") + "─┼─" + '─'*maxNameSize + "─┼─" + '─'*6)

    for ii in range(len(blueprints_list)):
        blp_name = blueprints_list[ii]
        if regex.match(blp_name):
            print(" " + str(ii) + " │ " + blp_name.ljust(maxNameSize) + " │ " + get_size(BLUEPRINT_DATA_PATH + blp_name))
    print("")


# -----------------------------------------------
#                Utility functions
# -----------------------------------------------

def blueprint_exists(name):
    """Check if a blueprint exists."""
    if os.path.exists(BLUEPRINT_DATA_PATH + name):
        if os.path.isdir(BLUEPRINT_DATA_PATH + name):
            return True
    return False


def get_size(path):
    """Disk usage in human readable format (e.g. '2,1GB')"""
    return subprocess.check_output(['du', '-sh', path]).split()[0].decode('utf-8')


if __name__ == '__main__':
    cli()
