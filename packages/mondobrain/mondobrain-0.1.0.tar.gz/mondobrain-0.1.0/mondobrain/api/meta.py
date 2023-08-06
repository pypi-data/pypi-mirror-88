from typing import List

from mondobrain.types import Data, Direction, Inverse

from .requestor import APIRequestor


def meta_class_start(
    outcome: str = None,
    target: str = None,
    timeout: int = None,
    min_size_frac: float = None,
    # case_points: dict = None, DISABLED FOR NOW
    classes: List[str] = None,
    direction: Direction = Direction.both,
    encode: List[str] = None,
    inverse: Inverse = None,
    depth: int = None,
    data: Data = None,
    **kwargs
):
    """Starts a classes meta solve
    """
    params = {
        "outcome": outcome,
        "target": target,
        "timeout": timeout,
        "min_size_frac": min_size_frac,
        "classes": classes,
        "direction": direction,
        "encode": encode,
        "inverse": inverse,
        "depth": depth,
        "data": data,
    }

    requestor = APIRequestor(**kwargs)
    requestor.request("post", "meta.class.start", params=params)


def meta_exclusion_set_start(
    outcome: str = None,
    target: str = None,
    timeout: int = None,
    min_size_frac: float = None,
    # case_points: dict = None, DISABLED FOR NOW
    min_size: int = None,
    classes: List[str] = None,
    direction: Direction = Direction.both,
    encode: List[str] = None,
    depth: int = None,
    data: Data = None,
    **kwargs
):
    """Starts an exclusion set solve
    """
    params = {
        "outcome": outcome,
        "target": target,
        "timeout": timeout,
        "min_size_frac": min_size_frac,
        "min_size": min_size,
        "classes": classes,
        "direction": direction,
        "encode": encode,
        "depth": depth,
        "data": data,
    }

    requestor = APIRequestor(**kwargs)
    return requestor.request("post", "meta.exclusionset.start", params=params)


def meta_result(id: str, **kwargs):
    """Read meta solve results (rules) from the API

    Parameters
    ----------
    id: str
        The task ID as returned from meta_classes_start or meta_exclusion_set_start
    """
    params = {"id": id}

    requestor = APIRequestor(**kwargs)

    return requestor.request("post", "meta.result", params=params)
