from typing import Dict, List, Union

from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr

Data = List[Dict[str, Union[None, StrictStr, StrictInt, StrictFloat]]]


class SolveOptions(BaseModel):
    outcome: str
    target: str

    timeout: int = Field(600, gt=0, le=600)
    min_size_frac: float = Field(0.2, gt=0, lt=1)
    case_points: Dict[str, Union[StrictFloat, StrictInt]] = {}
