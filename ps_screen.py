#!/usr/bin/env python

import click
import psutil
import re
import subprocess
import shlex

from click._compat import strip_ansi
from collections import defaultdict
from operator import methodcaller
from os import getenv
from tabulate import tabulate


def collapse_home(path):
    home = getenv('HOME')

    if home:
        path = re.sub(r'^{}'.format(home), '~', path)

    return path


def terminal_columns():
    try:
        return int(subprocess.check_output(shlex.split('tput cols')))
    except:
        return 0


def clean(cmd):
    if cmd in ['-bash', '/bin/bash']:
        return 'bash'

    return cmd


def print_child(p, depth=1, columns=0):
    output = (('  ' * depth) +
              click.style(str(p.pid), fg='cyan', bold=True) +
              ' ' +
              collapse_home(clean(' '.join(p.cmdline()))))

    stripped_length = len(strip_ansi(output))

    if columns and stripped_length > columns:
        output = output[0:-(stripped_length - columns + 6)] + '...'

    click.echo(output)

    depth += 1

    for c in p.children():
        print_child(c, depth, columns)


def last_cmd(p):
    children = p.children(recursive=True)

    if children:
        return ' '.join(children[-1].cmdline())

    return ''


def format_name(name):
    gray = lambda: 'gray'

    colors = defaultdict(gray, tmux='blue', screen='green')

    return click.style(name, fg=colors[name], bold=True)


def table_row(process, full=False):
    return [
        click.style(str(process.pid), fg='cyan'),
        format_name(process.name()),
        click.style(collapse_home(process.cwd()), fg='green'),
        last_cmd(process) if not full else ''
    ]


@click.command()
@click.option('--full/--compact', is_flag=True, default=False,
              help='full output lists a full subprocess tree')
def ps_screen(full=False):
    screens = [p for p in psutil.process_iter()
               if p.name() in ['screen', 'tmux']]

    screens.sort(key=methodcaller('cwd'))

    columns = terminal_columns()

    table = [table_row(s, full) for s in screens]

    lines = tabulate(table, tablefmt='plain', numalign='left').split('\n')

    for screen, line in zip(screens, lines):
        stripped_length = len(strip_ansi(line))

        if columns and stripped_length > columns:
            line = line[0:-(stripped_length - columns + 6)] + '...'

        click.echo(line)

        if full:
            for c in screen.children():
                print_child(c, columns=columns)

            print


if __name__ == '__main__':
    ps_screen()
