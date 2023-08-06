# -*- coding: utf-8
"""
xltoy main cli (Command Line Interface)
"""
import click
from xltoy.collector import Collector, DiffCollector
from xltoy.utils import timeit
from xltoy import *

def set_verb(v=0):
    """

    :param v:  verbosity 1:WARNING,
                         2:INFO,
                         3+:DEBUG
    :return: Nothing,but logging verbosisty was set
    """
    if v>2:
        log.setLevel(DEBUG)
    elif v>1:
        log.setLevel(INFO)
    else:
        log.setLevel(WARNING)

@click.group()
def cli():
    pass

@click.command()
@click.option('--timeit', is_flag=True, help='Print out how many times it takes for the task')
@click.option('--yaml', is_flag=True, help='Print out the yaml hiearchical view')
@click.option('--data', is_flag=True, help='Collect only data, it will ignore formulas')
@click.option('-v', '--verbose', count=True, help="verbose output (repeat for increased verbosity)")
@click.option('--add_fingerprint', is_flag=True, help='Add metadata under section xltoy')
@click.argument('filename')
def collect(filename, **kwargs):
    set_verb(kwargs.get('verbose'))
    click.echo('Collect an excel')
    with timeit("{} collect".format(filename), kwargs.get('timeit')):
        c = Collector(filename,
                      only_data=kwargs.get('data'),
                      add_fingerprint=kwargs.get('add_fingerprint'))
        if kwargs.get('yaml'):
            print(c.to_yaml())


@click.command()
@click.option('--timeit', is_flag=True, help='Print out how many times it takes for the task')
@click.option('--data', is_flag=True, help='Collect only data, it will ignore formulas')
@click.option('--relative', is_flag=True, help='Areas are handled as relative, each starts from row1,col1')
@click.option('-v', '--verbose', count=True, help="verbose output (repeat for increased verbosity)")
@click.option('--add_fingerprint', is_flag=True, help='Add metadata under section xltoy')
@click.argument('filename1')
@click.argument('filename2')
def diff(filename1, filename2, **kwargs):
    set_verb(kwargs.get('verbose'))
    with timeit("collect 2 files", kwargs.get('timeit')):
        d = DiffCollector(filename1,filename2,
                          only_data=kwargs.get('data'),
                          relative=kwargs.get('relative'),
                          add_fingerprint=kwargs.get('add_fingerprint'))
        d.to_yaml()

cli.add_command(collect)
cli.add_command(diff)

if __name__ == '__main__':
    cli()
