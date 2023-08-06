from dataclasses import dataclass
from datetime import datetime
from typing import List

from robinhood_commons.entity.investor import Investor
from robinhood_commons.entity.lot import Lot
from robinhood_commons.entity.order_type.order_request import OrderRequest


@dataclass(frozen=True)
class ExecutionRequest:
    datetime: datetime
    investor: Investor
    lot: Lot
    symbol: str
    price: float
    actions: List[OrderRequest]
    notes: str
