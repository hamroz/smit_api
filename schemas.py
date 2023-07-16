from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional
from pydantic import validator
import datetime


class CargoRate(BaseModel):
    cargo_type: str = Field(alias="cargo-type")
    rate: float

    @validator("rate")
    def validate_rate(cls, rate):
        if rate < 0:
            raise ValueError("Rate must be a positive number.")
        return rate


class TariffIn(BaseModel):
    tariffs: Dict[str, List[CargoRate]]


class TariffUpdate(BaseModel):
    date: Optional[str]
    cargo_type: Optional[str]
    rate: Optional[float]

    @validator("date")
    def validate_date(cls, date):
        if date is not None:
            try:
                datetime.datetime.strptime(date, "%Y-%m-%d").date()
                return date
            except ValueError:
                raise ValueError("Invalid date format. It should be YYYY-MM-DD.")


class InsuranceIn(BaseModel):
    declared_value: float
