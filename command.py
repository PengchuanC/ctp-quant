"""
@author: chuanchao.peng
@date: 2021/12/20 19:02
@file command.py.py
@desc: cli
"""

import click

from database.models import create_tables


@click.group()
def root():
    pass


@root.group()
def database():
    pass


@database.command()
def migrate():
    create_tables()


if __name__ == '__main__':
    root()
