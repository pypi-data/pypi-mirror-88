from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from robinhood_commons.entity.execution_type import ExecutionType
from robinhood_commons.entity.investor import Investor
from robinhood_commons.entity.lot import Lot


@dataclass(frozen=True)
class ExecutionResult:
    status: bool
    lot: Lot
    sell_time: datetime
    buy_time: datetime
    investor: Investor
    execution_type: ExecutionType
    symbol: str
    sell_price: float
    buy_price: float
    quantity: float
    notes: str
    error_message: Optional[str] = None
    error_code: int = 0
