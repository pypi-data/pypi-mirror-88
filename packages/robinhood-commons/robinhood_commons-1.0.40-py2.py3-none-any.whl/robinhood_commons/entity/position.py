from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from robinhood_commons.util.date_utils import convert_dates
from robinhood_commons.util.num_utils import convert_floats

EXAMPLE: Dict[str, str] = {'url': 'https://api.robinhood.com/positions/5PY78241/e5fdefaa-bb90-4af1-9dee-c9782b1519fd/',
                           'instrument': 'https://api.robinhood.com/instruments/e5fdefaa-bb90-4af1-9dee-c9782b1519fd/',
                           'account': 'https://api.robinhood.com/accounts/5PY78241/', 'account_number': '5PY78241',
                           'average_buy_price': '9.0429', 'pending_average_buy_price': '9.0429',
                           'quantity': '7.00000000', 'intraday_average_buy_price': '0.0000',
                           'intraday_quantity': '0.00000000', 'shares_held_for_buys': '0.00000000',
                           'shares_held_for_sells': '0.00000000', 'shares_held_for_stock_grants': '0.00000000',
                           'shares_held_for_options_collateral': '0.00000000',
                           'shares_held_for_options_events': '0.00000000',
                           'shares_pending_from_options_events': '0.00000000',
                           'shares_available_for_closing_short_position': '0.000000',
                           'updated_at': '2018-05-04T13:33:05.364913Z', 'created_at': '2018-04-23T14:38:07.373841Z',
                           'symbol': 'ARCO', 'shares_available_for_exercise': '0.0000000'}


@dataclass(frozen=True)
class Position:
    symbol: str
    quantity: float
    intraday_quantity: float
    created_at: datetime
    updated_at: datetime
    average_buy_price: float
    pending_average_buy_price: float
    intraday_average_buy_price: float
    instrument: str
    shares_available_for_exercise: float
    shares_held_for_buys: float
    shares_held_for_options_collateral: float
    shares_held_for_options_events: float
    shares_held_for_sells: float
    shares_held_for_stock_grants: float
    shares_pending_from_options_events: float
    url: str
    account: str
    account_number: str
    shares_available_for_closing_short_position: float = 0.00


def clean_position(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data = convert_floats(data, ['quantity', 'intraday_quantity', 'average_buy_price', 'pending_average_buy_price',
                                 'intraday_average_buy_price', 'shares_available_for_exercise', 'shares_held_for_buys',
                                 'shares_held_for_options_collateral', 'shares_held_for_options_events',
                                 'shares_held_for_sells', 'shares_held_for_stock_grants',
                                 'shares_pending_from_options_events'])

    data = convert_dates(data)

    return data


def main() -> None:
    position = Position(**EXAMPLE)
    print(position)


if __name__ == "__main__":
    main()
