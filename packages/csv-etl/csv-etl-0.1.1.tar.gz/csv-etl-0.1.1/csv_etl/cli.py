import click

from .rules import load_rules_from_yaml
from .csv_etl import CSVConverter

@click.command()
@click.option('--config', help='File path to the yaml configuration')
@click.option('--csv', help='File path to the csv to convert')
@click.option('--outfile', default=None, help='File path to write the result to')
@click.option('--format', default='json', help='File path to the csv to convert')
def main(config, csv, outfile, format):
    rules = load_rules_from_yaml(config)
    converter = CSVConverter(rules)
    result = converter.convert(csv, to=format, outfile=outfile)
    if outfile:
        print('Done')
    else:
        print(result)
