import click
from elasticsearch import (
    Elasticsearch, 
    helpers
)

from ynabsearch.ynab import YNABClient


@click.group()
def cli():
    pass


@cli.command()
@click.option('-b', '--budget-name', required=True, help='The YNAB budget name.')
@click.option('-h', '--host', default='http://localhost:9200', help='The Elasticsearch host.')
def load(budget_name, host):

    ynab = YNABClient.from_budget_name(budget_name)
    es = Elasticsearch(hosts=[host])

    result = helpers.bulk(
        client=es, 
        actions=[
            {
                '_id': transaction.get('id'),
                '_index': 'ynab_transactions',
                '_source': transaction
            }
            for transaction in ynab.get_transactions()
        ]
    )
    print(result)

    click.echo(f'{result[0]} New transactions loaded successfully.')


if __name__ == '__main__':
    cli()
