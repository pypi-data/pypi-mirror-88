from typing import Dict, Union

from pydantic import BaseModel


class ContinuousFilter(BaseModel):
    lo: float
    hi: float


DiscreteFilter = str

Rule = Dict[str, Union[ContinuousFilter, DiscreteFilter]]
