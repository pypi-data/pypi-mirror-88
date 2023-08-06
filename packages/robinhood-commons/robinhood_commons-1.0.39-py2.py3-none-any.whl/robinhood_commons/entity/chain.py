from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from robinhood_commons.entity.tick import Tick, clean_tick
from robinhood_commons.util.date_utils import date_parse
from robinhood_commons.util.num_utils import convert_floats

EXAMPLE: Dict[str, Any] = {'id': 'f7ed1d28-55c4-4c76-abf5-3b16cb68a2e7', 'symbol': 'MRO', 'can_open_position': True,
                           'cash_component': None,
                           'expiration_dates': ['2020-06-19', '2020-06-26', '2020-07-02', '2020-07-10', '2020-07-17',
                                                '2020-07-24', '2020-07-31', '2020-10-16', '2021-01-15', '2021-06-18',
                                                '2021-09-17', '2022-01-21'],
                           'trade_value_multiplier': '100.0000',
                           'underlying_instruments': [{'id': '35f7f10a-3163-4889-a64c-df0166b2dcec',
                                                       'instrument': 'https://api.robinhood.com/instruments/ab4f79fc-f84a-4f7b-8132-4f3e5fb38075/',
                                                       'quantity': 100}],
                           'min_ticks': {'above_tick': '0.05', 'below_tick': '0.01', 'cutoff_price': '3.00'}}


@dataclass(frozen=True)
class Chain:
    id: str
    symbol: str
    can_open_position: bool
    cash_component: str
    expiration_dates: List[datetime]
    trade_value_multiplier: float
    underlying_instruments: List[UnderlyingInstruments]
    min_ticks: Tick


@dataclass(frozen=True)
class UnderlyingInstruments:
    id: str
    instrument: str
    quantity: float


def clean_chain(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data['expiration_dates'] = [date_parse(d) for d in data['expiration_dates']]
    data['underlying_instruments'] = [UnderlyingInstruments(**clean_underlying_instruments(u)) for u in
                                      data['underlying_instruments']]
    data['min_ticks'] = Tick(**clean_tick(data['min_ticks']))

    data = convert_floats(data, ['trade_value_multiplier'])

    return data


def clean_underlying_instruments(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data = convert_floats(data, ['quantity'])

    return data


def main() -> None:
    chain = Chain(**clean_chain(EXAMPLE))
    print(chain)


if __name__ == '__main__':
    main()
