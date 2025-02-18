"""Command-line interface for paper-per-year."""

import click
from . import core

@click.command(help="Generate publication per year plots for academic authors")
@click.argument('author_name', nargs=-1, required=True)
@click.option('-o', '--output-dir', default='.', help='Directory to save the output PDF', 
              type=click.Path(file_okay=False, dir_okay=True, writable=True))
@click.option('--style', type=click.Choice(['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']),
              default='darkgrid', help='Seaborn plot style')
@click.option('--context', type=click.Choice(['paper', 'notebook', 'talk', 'poster']),
              default='talk', help='Seaborn plot context (controls plot scaling)')
def main(author_name, output_dir, style, context):
    """Generate publication per year plots for academic authors."""
    author_name = ' '.join(author_name)
    core.process_author(author_name, output_dir, style, context) 