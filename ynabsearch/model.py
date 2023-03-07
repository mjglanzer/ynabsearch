from dataclasses import (
    dataclass,
    asdict
)
import typing as t

@dataclass
class Transaction:
    id: str
    date: str
    category: str
    payee: str
    memo: str
    amount: float
    flow: t.Literal['in', 'out']

    @classmethod
    def from_dict(cls, data: t.Dict[str, t.Any]):
        amount = data.get('amount')/1000

        return cls(
            id=data.get('id'),
            date=data.get('date'),
            category=data.get('category_name'),
            payee=data.get('payee_name'),
            memo=data.get('memo'),
            amount=abs(amount),
            flow='in' if amount > 0 else 'out'
        )

    def to_dict(self) -> t.Dict[str, t.Any]:
        return asdict(self)
