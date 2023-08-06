from enum import Enum
from typing import List

from pydantic import BaseModel

from .rule import Rule
from .solve import Data, SolveOptions


class Direction(str, Enum):
    in_ = "in"
    out = "out"
    both = "both"


class Inverse(str, Enum):
    in_rule = "in_rule"


class ClassStartOptions(SolveOptions):
    data: Data
    target: str = None
    classes: List[str] = None
    direction: Direction = Direction.both
    inverse: Inverse = None
    depth: int = 1
    parallel: bool = False


class ExclusionSetStartOptions(SolveOptions):
    data: Data
    target: str = None
    min_size: int = 10
    classes: List[str] = None
    direction: Direction = Direction.both
    depth: int = 1
    parallel: bool = False


class Meta(BaseModel):
    name: str = None
    class_: str = None
    iteration: int = 0
    depth: int = 0
    direction: Direction = None
    inverse: Inverse = None
    score: float = 0
    size: float = 0


class MetaRule(BaseModel):
    rule: Rule
    meta: Meta


class MetaResult(BaseModel):
    rules: List[MetaRule]
