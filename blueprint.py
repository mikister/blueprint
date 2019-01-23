#!/usr/bin/python3

import json
import subprocess
import os
import click
from distutils.dir_util import copy_tree
import re
import shutil


BLUEPRINT_DATA_PATH = os.path.expanduser("~") + "/.blueprint/.blueprint_data/"


class DefaultGroup(click.Group):

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


@cli.command()
@click.argument('name')
def blueprint(name):
    print("Blueprint | " + name)
    copy_tree(BLUEPRINT_DATA_PATH + name, os.getcwd())


@cli.command()
@click.argument('name')
def new(name):
    print(name)
    if not blueprint_exists(name):
        os.makedirs(BLUEPRINT_DATA_PATH + name)
    subprocess.call("xdg-open " + BLUEPRINT_DATA_PATH + name, shell=True)


@cli.command()
@click.argument('name')
def delete(name):
    print(name)
    if blueprint_exists(name):
        shutil.rmtree(BLUEPRINT_DATA_PATH + name)


@cli.command()
@click.argument('name')
def showfiles(name):
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
    """Lists all blueprints."""
    if regexing:
        regexQuerry = regexing[0]
    else:
        regexQuerry = ".*"
    
    regex = re.compile(regexQuerry)

    print("\nAvaiable blueprints:")
    blueprints_list = os.listdir(BLUEPRINT_DATA_PATH)
    blueprints_list.sort()

    maxNameSize = max([len(blp) for blp in blueprints_list])
    indexPadSize = len(str(len(blueprints_list))) + 1

    print(" i".ljust(indexPadSize) + " │ " + "name".ljust(maxNameSize) + " │ size")
    print("──".ljust(indexPadSize, "─") + "─┼─" + '─'*maxNameSize + "─┼─" + '─'*6)

    for ii in range(len(blueprints_list)):
        blp_name = blueprints_list[ii]
        if regex.match(blp_name):
            print(" " + str(ii) + " │ " + blp_name.ljust(maxNameSize) + " │ " + get_size(BLUEPRINT_DATA_PATH + blp_name))
    print("")


# Utility functions

def blueprint_exists(name):
    if os.path.exists(BLUEPRINT_DATA_PATH + name):
        if os.path.isdir(BLUEPRINT_DATA_PATH + name):
            return True
    return False


def get_size(path):
    """disk usage in human readable format (e.g. '2,1GB')"""
    return subprocess.check_output(['du', '-sh', path]).split()[0].decode('utf-8')




if __name__ == '__main__':
    cli()
