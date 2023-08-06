from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, Optional

from robinhood_commons.entity.price import Price, clean_price
from robinhood_commons.entity.printable import Printable
from robinhood_commons.util.date_utils import convert_dates
from robinhood_commons.util.num_utils import convert_floats

EXAMPLE: Dict[str, Any] = {'id': 'ea49e4b7-1f01-55ce-9393-e95a9fc505fa',
                           'url': 'https://api.robinhood.com/dividends/ea49e4b7-1f01-55ce-9393-e95a9fc505fa/',
                           'account': 'https://api.robinhood.com/accounts/5PY78241/',
                           'instrument': 'https://api.robinhood.com/instruments/62463799-a202-4cbe-9b7d-ae3caacc3412/',
                           'amount': '4.96', 'rate': '0.0935150000', 'position': '53.00000000', 'withholding': '0.00',
                           'record_date': '2020-05-29', 'payable_date': '2020-06-02', 'paid_at': '2020-06-03T02:25:41Z',
                           'state': 'reinvested', 'nra_withholding': '0', 'drip_enabled': True,
                           'drip_order_id': 'ba3b3c4d-f0ef-44ee-aa13-77a75d911b4c', 'drip_order_state': 'filled',
                           'drip_order_quantity': '0.14794900',
                           'drip_order_execution_price': {'currency_id': '1072fc76-1862-41ab-82c2-485837590762',
                                                          'currency_code': 'USD',
                                                          'amount': '33.53'}}


class DividendState(Printable, Enum):
    PAID = auto()
    PENDING = auto()
    REINVESTED = auto()
    VOIDED = auto()
    UNKNOWN = auto()

    @staticmethod
    def to_enum(value: str) -> Optional[DividendState]:
        if value is None:
            return DividendState.UNKNOWN
        v: str = value.upper().replace(' ', '-').replace('-', '_')
        return DividendState[v]

    def value(self) -> str:
        return self.name.lower()


@dataclass(frozen=True)
class Dividend:
    id: str
    url: str
    account: str
    instrument: str
    amount: float
    rate: float
    position: float
    withholding: float
    record_date: datetime
    payable_date: datetime
    paid_at: datetime
    state: DividendState
    nra_withholding: str
    drip_enabled: bool
    drip_order_id: Optional[str] = None
    drip_order_state: Optional[str] = None
    drip_order_quantity: Optional[float] = None
    drip_order_execution_price: Optional[Price] = None


def clean_dividend(input_data: Dict[str, str]) -> Dict[str, Any]:
    data: Dict[str, Any] = deepcopy(input_data)

    data['drip_order_execution_price'] = Price(
        **clean_price(data['drip_order_execution_price'])) if 'drip_order_execution_price' in data else None

    data['state'] = DividendState.to_enum(data['state'])
    data = convert_floats(data, ['amount', 'rate', 'position', 'withholding', 'drip_order_quantity'])
    data = convert_dates(data, ['record_date', 'payable_date', 'paid_at'])

    return data


def main() -> None:
    dividend = Dividend(**clean_dividend(EXAMPLE))
    print(dividend)


if __name__ == '__main__':
    main()
