from datetime import datetime, timedelta
from typing import TypedDict


class TimeStampDict(TypedDict):
    identifier: str
    timestamp: datetime


class LapTimeDict(TypedDict):
    identifier: str
    lap_time: timedelta
