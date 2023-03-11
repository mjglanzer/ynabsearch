import os
import pytest
import requests_mock

from ynabsearch.ynab import (
    YNAB_API_URL,
    YNABClient, 
    BudgetNotFoundException
)

budget_name = 'Test Budget'


def test_query_success():
    with requests_mock.Mocker() as m:
        res_json = {'data': {'budgets': [{'id': '123', 'name': budget_name}]}}
        m.get(YNAB_API_URL + '/', json=res_json)
        res = YNABClient._query('/')
        assert res == res_json


def test_query_failure():
    with requests_mock.Mocker() as m:
        m.get(YNAB_API_URL + '/', status_code=404)
        with pytest.raises(ValueError):
            YNABClient._query('/')


def test_from_budget_name_success():
    with requests_mock.Mocker() as m:
        res_json = {'data': {'budgets': [{'id': '123', 'name': budget_name}]}}
        m.get(YNAB_API_URL + '/', json=res_json)
        client = YNABClient.from_budget_name(budget_name)
        assert client.budget_id == '123'


def test_from_budget_name_failure():
    with requests_mock.Mocker() as m:
        res_json = {'data': {'budgets': []}}
        m.get(YNAB_API_URL + '/', json=res_json)
        with pytest.raises(BudgetNotFoundException):
            YNABClient.from_budget_name(budget_name)


def test_get_transactions():
    with requests_mock.Mocker() as m:
        res_json = {'data': {'transactions': [{'id': '1', 'amount': 50000, 'subtransactions': []}]}}
        m.get(YNAB_API_URL + '/123/transactions', json=res_json)
        client = YNABClient('123')
        transactions = list(client.get_transactions())
        assert len(transactions) == 1
        assert transactions[0].id == '1'
