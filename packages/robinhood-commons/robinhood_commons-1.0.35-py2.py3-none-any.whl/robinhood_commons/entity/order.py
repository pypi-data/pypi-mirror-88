from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union

from robinhood_commons.entity.execution_type import ExecutionType
from robinhood_commons.entity.price import Price, clean_price
from robinhood_commons.entity.state import State
from robinhood_commons.entity.time_in_force import TimeInForce
from robinhood_commons.util.date_utils import convert_dates
from robinhood_commons.util.num_utils import convert_floats

ERROR_DETAIL_KEY: str = 'detail'

EXAMPLE: Dict[str, Union[str, bool, List[Any], Dict[str, str]]] = {'id': '845aa52f-f6b4-42e4-9ec7-6f4978a90bbb',
                                                                   'ref_id': 'ee2e875c-dbff-463d-8a12-3d3e00b76a5f',
                                                                   'url': 'https://api.robinhood.com/orders/845aa52f-f6b4-42e4-9ec7-6f4978a90bbb/',
                                                                   'account': 'https://api.robinhood.com/accounts/5PY78241/',
                                                                   'position': 'https://api.robinhood.com/positions/5PY78241/ab4f79fc-f84a-4f7b-8132-4f3e5fb38075/',
                                                                   'cancel': 'https://api.robinhood.com/orders/845aa52f-f6b4-42e4-9ec7-6f4978a90bbb/cancel/',
                                                                   'instrument': 'https://api.robinhood.com/instruments/ab4f79fc-f84a-4f7b-8132-4f3e5fb38075/',
                                                                   'cumulative_quantity': '0.00000000',
                                                                   'average_price': None, 'fees': '0.00',
                                                                   'state': 'unconfirmed', 'type': 'market',
                                                                   'side': 'buy', 'time_in_force': 'gtc',
                                                                   'trigger': 'immediate', 'price': '6.70000000',
                                                                   'stop_price': None, 'quantity': '5.00000000',
                                                                   'reject_reason': None,
                                                                   'created_at': '2020-06-16T23:39:38.319481Z',
                                                                   'updated_at': '2020-06-16T23:39:38.374303Z',
                                                                   'last_transaction_at': '2020-06-16T23:39:38.319481Z',
                                                                   'executions': [],
                                                                   'extended_hours': True,
                                                                   'override_dtbp_checks': False,
                                                                   'override_day_trade_checks': False,
                                                                   'response_category': None, 'stop_triggered_at': None,
                                                                   'last_trail_price': None,
                                                                   'last_trail_price_updated_at': None,
                                                                   'dollar_based_amount': None,
                                                                   'drip_dividend_id': None,
                                                                   'total_notional': {'amount': '33.50',
                                                                                      'currency_code': 'USD',
                                                                                      'currency_id': '1072fc76-1862-41ab-82c2-485837590762'},
                                                                   'executed_notional': None,
                                                                   'investment_schedule_id': None}


class OrderType(Enum):
    LIMIT = auto()
    MARKET = auto()

    @staticmethod
    def to_enum(value: str) -> Optional[OrderType]:
        v: str = value.upper().replace(' ', '-').replace('-', '_')
        return OrderType[v]

    def value(self) -> str:
        return self.name.lower()


@dataclass(frozen=True)
class OptionalOrder:
    order: Optional[Order] = None
    detail: Optional[str] = None


@dataclass(frozen=True)
class Order:
    id: str
    ref_id: str
    url: str
    account: str
    position: str
    cancel: str
    instrument: str
    cumulative_quantity: float
    state: State
    type: OrderType
    side: ExecutionType
    time_in_force: TimeInForce
    trigger: str  # TODO: enum
    price: Price
    quantity: float
    created_at: datetime
    updated_at: datetime
    last_transaction_at: datetime
    executions: List[Any]
    extended_hours: bool
    override_dtbp_checks: bool
    override_day_trade_checks: bool
    stop_triggered_at: datetime
    last_trail_price: float
    last_trail_price_updated_at: datetime
    average_price: Optional[float] = None
    fees: Optional[float] = None
    stop_price: Optional[Price] = None
    reject_reason: Optional[str] = None
    response_category: Optional[str] = None
    dollar_based_amount: Optional[Price] = None
    drip_dividend_id: Optional[str] = None
    total_notional: Optional[Price] = None
    executed_notional: Optional[Price] = None
    investment_schedule_id: Optional[str] = None
    details: Optional[str] = None


def clean_optional_order(input_data: Dict[str, Any]) -> Dict[str, Any]:
    if ERROR_DETAIL_KEY not in input_data:
        return {'order': clean_order(deepcopy(input_data))}

    return deepcopy(input_data)


def clean_order(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data['state'] = State.to_enum(data['state'])
    data['time_in_force'] = TimeInForce.to_enum(data['time_in_force'])
    data['side'] = ExecutionType.to_enum(data['side'])
    data['type'] = OrderType.to_enum(data['type'])

    consolidate_price_data(data, ['price', 'stop_price', 'dollar_based_amount', 'total_notional', 'executed_notional'])

    data = convert_floats(data, ['cumulative_quantity', 'quantity', 'average_price', 'fees', 'stop_price',
                                 'last_trail_price'])
    data = convert_dates(data, ['last_transaction_at', 'stop_triggered_at', 'last_trail_price_updated_at'])

    return data


def consolidate_price_data(input_data: Dict[str, Any], keys: List[str]) -> None:
    """In some cases, the price is a primitive, in others its in a single item list so handle both cases

    Args:
        input_data: input data
        keys: price keys
    """
    for key in keys:
        if key not in input_data:
            #  Skip missing key
            print(f'Skipping missing key: {key}')
        elif type(input_data[key]) in [str, float]:
            input_data[key] = Price(**clean_price({'amount': input_data[key]}))
        else:
            input_data[key] = Price(**clean_price(input_data[key])) if input_data[key] is not None else None


def main() -> None:
    order = Order(**clean_order(EXAMPLE))
    print(order)

    optional_order_1 = OptionalOrder(**clean_optional_order(EXAMPLE))
    print(optional_order_1)

    optional_order_2 = OptionalOrder(
        **clean_optional_order({ERROR_DETAIL_KEY: 'Request was throttled. Expected available in 28 seconds.'}))
    print(optional_order_2)


if __name__ == '__main__':
    main()
