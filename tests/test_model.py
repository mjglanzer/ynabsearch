import pytest
from typing import Dict

from ynabsearch.model import Transaction


sample_data = {
    'id': '1',
    'date': '2022-01-01',
    'category_name': 'Groceries',
    'payee_name': 'Costco',
    'memo': 'Bought groceries',
    'amount': -150500
}


def test_from_dict():
    transaction = Transaction.from_dict(sample_data)
    assert transaction.id == '1'
    assert transaction.date == '2022-01-01'
    assert transaction.category == 'Groceries'
    assert transaction.payee == 'Costco'
    assert transaction.memo == 'Bought groceries'
    assert transaction.amount == 150.50
    assert transaction.flow == 'out'


def test_to_dict():
    transaction = Transaction.from_dict(sample_data)
    dict_data = transaction.to_dict()
    assert dict_data == {
        'id': '1', 
        'date': '2022-01-01', 
        'category': 'Groceries', 
        'payee': 'Costco', 
        'memo': 'Bought groceries', 
        'amount': 150.50, 
        'flow': 'out'
    }
