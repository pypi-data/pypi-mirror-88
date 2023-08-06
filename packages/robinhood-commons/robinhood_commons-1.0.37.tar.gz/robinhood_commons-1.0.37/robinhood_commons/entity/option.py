from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from robinhood_commons.entity.option_type import OptionType
from robinhood_commons.entity.state import State
from robinhood_commons.entity.tick import Tick, clean_tick
from robinhood_commons.entity.tradability import Tradability
from robinhood_commons.util.date_utils import convert_dates
from robinhood_commons.util.num_utils import convert_floats

EXAMPLE: Dict[str, Any] = {'chain_id': 'f7ed1d28-55c4-4c76-abf5-3b16cb68a2e7', 'chain_symbol': 'MRO',
                           'created_at': '2020-06-10T00:13:05.407629Z', 'expiration_date': '2020-06-19',
                           'id': '7f7720a3-ccc1-45f4-b7be-37cb8ef69cbb', 'issue_date': '1991-05-06',
                           'min_ticks': {'above_tick': '0.05', 'below_tick': '0.01', 'cutoff_price': '3.00'},
                           'rhs_tradability': 'untradable', 'state': 'active', 'strike_price': '13.0000',
                           'tradability': 'tradable', 'type': 'call', 'updated_at': '2020-06-10T00:13:05.407639Z',
                           'url': 'https://api.robinhood.com/options/instruments/7f7720a3-ccc1-45f4-b7be-37cb8ef69cbb/',
                           'sellout_datetime': '2020-06-19T18:45:00+00:00'}

STATS_EXAMPLE: Dict[str, Any] = {'chain_id': 'f7ed1d28-55c4-4c76-abf5-3b16cb68a2e7', 'chain_symbol': 'MRO',
                                 'created_at': '2020-06-10T00:13:05.407629Z', 'expiration_date': '2020-06-19',
                                 'id': '7f7720a3-ccc1-45f4-b7be-37cb8ef69cbb', 'issue_date': '1991-05-06',
                                 'min_ticks': {'above_tick': '0.05', 'below_tick': '0.01', 'cutoff_price': '3.00'},
                                 'rhs_tradability': 'untradable', 'state': 'active', 'strike_price': '13.0000',
                                 'tradability': 'tradable', 'type': 'call', 'updated_at': '2020-06-10T00:13:05.407639Z',
                                 'url': 'https://api.robinhood.com/options/instruments/7f7720a3-ccc1-45f4-b7be-37cb8ef69cbb/',
                                 'sellout_datetime': '2020-06-19T18:45:00+00:00', 'adjusted_mark_price': '0.010000',
                                 'ask_price': '0.020000', 'ask_size': 10, 'bid_price': '0.000000', 'bid_size': 0,
                                 'break_even_price': '13.010000', 'high_price': None,
                                 'instrument': 'https://api.robinhood.com/options/instruments/7f7720a3-ccc1-45f4-b7be-37cb8ef69cbb/',
                                 'last_trade_price': '0.040000', 'last_trade_size': 1, 'low_price': None,
                                 'mark_price': '0.010000', 'open_interest': 1, 'previous_close_date': '2020-06-11',
                                 'previous_close_price': '0.010000', 'volume': 0, 'chance_of_profit_long': '0.007166',
                                 'chance_of_profit_short': '0.992834', 'delta': '0.015780', 'gamma': '0.020289',
                                 'implied_volatility': '2.139463', 'rho': '0.000018', 'theta': '-0.005508',
                                 'vega': '0.000360', 'high_fill_rate_buy_price': '0.020000',
                                 'high_fill_rate_sell_price': '0.000000', 'low_fill_rate_buy_price': '0.000000',
                                 'low_fill_rate_sell_price': '0.010000'}


@dataclass(frozen=True)
class Option:
    chain_id: str
    chain_symbol: str
    created_at: datetime
    expiration_date: datetime
    id: str
    issue_date: datetime
    min_ticks: Tick
    rhs_tradability: Tradability
    state: State
    strike_price: float
    tradability: Tradability
    type: OptionType
    updated_at: datetime
    url: str
    sellout_datetime: datetime
    adjusted_mark_price: Optional[float] = None
    ask_price: Optional[float] = None
    ask_size: Optional[int] = None
    bid_price: Optional[float] = None
    bid_size: Optional[int] = None
    break_even_price: Optional[float] = None
    high_price: Optional[float] = None
    instrument: Optional[str] = None
    last_trade_price: Optional[float] = None
    last_trade_size: Optional[int] = None
    low_price: Optional[float] = None
    mark_price: Optional[float] = None
    open_interest: Optional[int] = None
    previous_close_date: Optional[datetime] = None
    previous_close_price: Optional[float] = None
    volume: Optional[int] = None
    chance_of_profit_long: Optional[float] = None
    chance_of_profit_short: Optional[float] = None
    delta: Optional[float] = None
    gamma: Optional[float] = None
    implied_volatility: Optional[float] = None
    rho: Optional[float] = None
    theta: Optional[float] = None
    vega: Optional[float] = None
    high_fill_rate_buy_price: Optional[float] = None
    high_fill_rate_sell_price: Optional[float] = None
    low_fill_rate_buy_price: Optional[float] = None
    low_fill_rate_sell_price: Optional[float] = None


def clean_option(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data['min_ticks'] = Tick(**clean_tick(data['min_ticks']))
    data['rhs_tradability'] = Tradability.to_enum(data['rhs_tradability'])
    data['state'] = State.to_enum(data['state'])
    data['tradability'] = Tradability.to_enum(data['tradability'])
    data['type'] = OptionType.to_enum(data['type'])

    data = convert_floats(data,
                          ['strike_price', 'adjusted_mark_price', 'ask_price', 'ask_size', 'bid_price', 'bid_size',
                           'break_even_price', 'high_price', 'last_trade_price', 'last_trade_size', 'low_price',
                           'mark_price', 'open_interest', 'previous_close_price', 'volume', 'chance_of_profit_long',
                           'chance_of_profit_short', 'delta', 'gamma', 'implied_volatility', 'rho', 'theta', 'vega',
                           'high_fill_rate_buy_price', 'high_fill_rate_sell_price', 'low_fill_rate_buy_price',
                           'low_fill_rate_sell_price'])

    data = convert_dates(data, ['expiration_date', 'issue_date', 'sellout_datetime', 'previous_close_date'])

    return data


def main() -> None:
    for example in [EXAMPLE, STATS_EXAMPLE]:
        option: Option = Option(**clean_option(example))
        print(option)


if __name__ == '__main__':
    main()
