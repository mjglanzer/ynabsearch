import click
from click.testing import CliRunner
from unittest.mock import MagicMock
from ynabsearch.cli import load


def test_load(mocker):
    # Mock the YNABClient and Elasticsearch classes
    ynab_mock = MagicMock()
    elasticsearch_mock = MagicMock()

    # Mock the from_budget_name method to return the YNABClient mock
    from_budget_name_mock = mocker.patch('ynabsearch.cli.YNABClient.from_budget_name', return_value=ynab_mock)

    # Mock the Elasticsearch constructor to return the Elasticsearch mock
    elasticsearch_constructor_mock = mocker.patch('ynabsearch.cli.Elasticsearch', return_value=elasticsearch_mock)

    # Mock the bulk method to return a success response
    bulk_mock = mocker.patch('ynabsearch.cli.helpers.bulk', return_value=(1, []))

    # Run the command with the mocked objects
    runner = CliRunner()
    result = runner.invoke(load, ['--budget-name', 'Test Budget', '--host', 'http://localhost:9200'])

    # Assert that the YNABClient and Elasticsearch constructors were called with the correct arguments
    from_budget_name_mock.assert_called_once_with('Test Budget')
    elasticsearch_constructor_mock.assert_called_once_with(hosts=['http://localhost:9200'])

    # Assert that the bulk method was called with the correct arguments
    bulk_mock.assert_called_once_with(
        client=elasticsearch_mock,
        actions=[
            {
                '_id': transaction.get('id'),
                '_index': 'ynab_transactions',
                '_source': transaction
            }
            for transaction in ynab_mock.get_transactions()
        ]
    )

    # Assert that the command returned the correct output
    assert result.output.strip() == '1 New transactions loaded successfully.'
    assert result.exit_code == 0
