from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict

from robinhood_commons.entity.state import State
from robinhood_commons.util.date_utils import convert_dates
from robinhood_commons.util.num_utils import convert_floats

EXAMPLE: Dict[str, str] = {'id': '96d878fc-2023-40e9-bd6f-ff43d349fce0',
                           'ref_id': '96d878fc-2023-40e9-bd6f-ff43d349fce0',
                           'url': 'https://api.robinhood.com/ach/transfers/96d878fc-2023-40e9-bd6f-ff43d349fce0/',
                           'cancel': None,
                           'ach_relationship': 'https://api.robinhood.com/ach/relationships/2a0861b2-7bb3-41fc-8737-c7646dc9e1c6/',
                           'account': 'https://api.robinhood.com/accounts/5PY78241/', 'amount': '1010.28',
                           'direction': 'deposit', 'state': 'pending', 'fees': '0.00', 'status_description': '',
                           'scheduled': False, 'expected_landing_date': '2020-06-15', 'early_access_amount': '1000.00',
                           'created_at': '2020-06-11T23:19:40.250436Z', 'updated_at': '2020-06-11T23:19:43.262917Z',
                           'rhs_state': None, 'expected_sweep_at': None,
                           'expected_landing_datetime': '2020-06-15T13:00:00Z', 'investment_schedule_id': None}


class TransferDirection(Enum):
    DEPOSIT = auto()

    @staticmethod
    def to_enum(value: str) -> TransferDirection:
        v: str = value.upper().replace(' ', '-').replace('-', '_')
        return TransferDirection[v]

    def value(self) -> str:
        return self.name.lower()


@dataclass(frozen=True)
class BankTransfer:
    id: str
    ref_id: str
    url: str
    cancel: str
    ach_relationship: str
    account: str
    amount: float
    direction: TransferDirection
    state: State
    fees: float
    status_description: str
    scheduled: bool
    expected_landing_date: datetime
    early_access_amount: float
    created_at: datetime
    updated_at: datetime
    rhs_state: State
    expected_sweep_at: str
    expected_landing_datetime: datetime
    investment_schedule_id: str


def clean_transfer(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data['direction'] = TransferDirection.to_enum(data['direction'])
    data['state'] = State.to_enum(data['state'])
    data['rhs_state'] = State.to_enum(data['rhs_state'])

    data = convert_floats(data, ['amount', 'fees', 'early_access_amount'])

    data = convert_dates(data, ['expected_landing_date', 'expected_landing_datetime'])

    return data


def main() -> None:
    bank_transfer = BankTransfer(**clean_transfer(EXAMPLE))
    print(bank_transfer)


if __name__ == '__main__':
    main()
