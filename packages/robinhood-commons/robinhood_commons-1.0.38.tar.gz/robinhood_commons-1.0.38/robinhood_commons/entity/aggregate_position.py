from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from robinhood_commons.entity.option_type import OptionType
from robinhood_commons.util.date_utils import convert_dates
from robinhood_commons.util.num_utils import convert_floats

# TODO: create strategy enum...short_call...etc.
EXAMPLES: List[Dict[str, Any]] = [{'id': '9cb5159b-9450-4772-a2bb-0949f487ee97',
                                   'chain': 'https://api.robinhood.com/options/chains/f7ed1d28-55c4-4c76-abf5-3b16cb68a2e7/',
                                   'symbol': 'MRO', 'strategy': 'short_call', 'average_open_price': '39.0000', 'legs': [
        {'id': '4f46d8fc-7fad-4f41-a938-5d087945d52c',
         'position': 'https://api.robinhood.com/options/positions/bfc6da87-c8c2-4532-b03e-34a9812503b0/',
         'position_type': 'short',
         'option': 'https://api.robinhood.com/options/instruments/664ae954-0d19-4126-a985-efaddd77ceec/',
         'ratio_quantity': 1, 'expiration_date': '2020-06-26', 'strike_price': '6.5000', 'option_type': 'call'}],
                                   'quantity': '2.0000', 'intraday_average_open_price': '0.0000',
                                   'intraday_quantity': '0.0000', 'direction': 'credit', 'intraday_direction': 'debit',
                                   'trade_value_multiplier': '100.0000', 'created_at': '2020-05-21T13:35:21.353974Z',
                                   'updated_at': '2020-05-21T13:36:10.830280Z'},
                                  {'id': '5bef3293-55d1-48cc-afa5-627f2946eb01',
                                   'chain': 'https://api.robinhood.com/options/chains/f7ed1d28-55c4-4c76-abf5-3b16cb68a2e7/',
                                   'symbol': 'MRO', 'strategy': 'short_call', 'average_open_price': '55.0000', 'legs': [
                                      {'id': '2f3ed3f1-2ced-4e6a-8d59-34b690f84da1',
                                       'position': 'https://api.robinhood.com/options/positions/4fe8bc89-dea1-4f53-996d-d660f31cb64e/',
                                       'position_type': 'short',
                                       'option': 'https://api.robinhood.com/options/instruments/e84ca9cd-89a1-4697-8801-6bc1573726cf/',
                                       'ratio_quantity': 1, 'expiration_date': '2020-06-19', 'strike_price': '6.0000',
                                       'option_type': 'call'}], 'quantity': '2.0000',
                                   'intraday_average_open_price': '0.0000', 'intraday_quantity': '0.0000',
                                   'direction': 'credit', 'intraday_direction': 'debit',
                                   'trade_value_multiplier': '100.0000', 'created_at': '2020-05-08T13:33:24.102329Z',
                                   'updated_at': '2020-05-08T13:33:24.291919Z'}]


@dataclass(frozen=True)
class AggregatePosition:
    id: str
    chain: str
    symbol: str
    strategy: str
    average_open_price: float
    legs: List[Leg]
    quantity: float
    intraday_average_open_price: float
    intraday_quantity: float
    direction: str
    intraday_direction: str
    trade_value_multiplier: float
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class Leg:
    id: str
    position: str
    position_type: str  # TODO: enum
    option: str
    ratio_quantity: int
    expiration_date: datetime
    strike_price: float
    option_type: OptionType


def clean_aggregate_position(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data['legs'] = [Leg(**clean_leg(leg)) for leg in data['legs']]

    data = convert_floats(data, ['average_open_price', 'quantity', 'intraday_average_open_price', 'intraday_quantity',
                                 'trade_value_multiplier'])

    data = convert_dates(data, ['expiration_date'])

    return data


def clean_leg(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data['option_type'] = OptionType.to_enum(data['option_type'])

    data = convert_floats(data, ['strike_price'])
    data = convert_dates(data, ['expiration_date'])

    return data


def main() -> None:
    aggregate_positions = [AggregatePosition(**clean_aggregate_position(a)) for a in EXAMPLES]
    print(aggregate_positions)


if __name__ == '__main__':
    main()
