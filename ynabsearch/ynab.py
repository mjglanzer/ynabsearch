import os
import requests
from requests.exceptions import RequestException
import typing as t

from ynabsearch.model import Transaction


YNAB_API_URL = 'https://api.youneedabudget.com/v1/budgets'
YnabId = t.NewType('YnabId', str)


class BudgetNotFoundException(Exception):
    pass


class YNABClient:
    
    def __init__(self, budget_id):
        self.budget_id = budget_id

    @classmethod
    def from_budget_name(cls, budget_name: str):
        """ Retrieve YNAB Budget UUID with friendly name. """

        res_json = cls._query('/')
        for budget in res_json.get('data', {}).get('budgets', []):
            if budget.get('name') == budget_name:
                return cls(budget.get('id'))

        raise BudgetNotFoundException(budget_name)

    @staticmethod
    def _query(endpoint: str = '') -> t.Dict[str, t.Any]:
        """Authenticated YNAB API request."""

        try:
            res = requests.get(
                url=YNAB_API_URL + endpoint, 
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {os.environ.get("YNAB_API_KEY")}'
                }
            )
            res.raise_for_status()
            return res.json()

        except RequestException as e:
            raise ValueError(f'Error querying YNAB API: {e}') from e

    def _get_transactions(self) -> t.Dict[str, t.Any]:
        """ Retrieve transactions with Budged ID. """

        res = self._query(f'/{self.budget_id}/transactions')
        return res.get('data').get('transactions')
    
    def get_transactions(self) -> t.Generator[Transaction, None, None]:
        """ Preprocess YNAB subtransactions for Elasticsearch. """

        for t in self._get_transactions():
            if t.get('subtransactions'):
                for subt in t.get('subtransactions'):
                    subt['date'] = t.get('date')
                    subt['payee_name'] = t.get('payee_name')

                    yield Transaction.from_dict(subt)
            else:
                
                yield Transaction.from_dict(t)


