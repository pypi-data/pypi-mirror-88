import io

import numpy as np
import pandas as pd

from mondobrain.api import solve_result, solve_start_file
from mondobrain.dd_transformer import DDTransformer
from mondobrain.utils import utilities


def solve(
    df: pd.DataFrame,
    outcome: str = None,
    target: str = None,
    encode=True,
    sample=True,
    random_state=0,
    **kwargs
):
    """Run a solve without worrying about API requests.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to use for the solve

    outcome : str, default=None
        Which column to use as the outcome for the solve (sometimes referred to as a
        target feature). If None, then the first column is selected

    target: str, default=None
        The class in the outcome column to target. For a continuous outcome this should
        either be `min` or `max`. If None, then the first class or `max` is selected.

    encode: bool, default=True
        Whether or not the data should be encoded before being sent to the MB API.
        Encoding can result in additional time on client side. Disable if your data is
        largely non-sensitive.

    sample: bool, default=True
        Whether or not the data should be sampled before being sent to the MB API.
        Not pre-sampling the data can cause size limits to be reached and excessive
        solve times

    random_state : int or np.random.RandomStateInstance, default: 0
        Pseudo-random number generator to control the sampling state.
        Use an int for reproducible results across function calls.
        See the sklearn for more details.

    kwargs: any
        Remaining kwargs are sent so solve_start_file

    Returns
    -------
    rule: dict
        The conditions that the MB API found
    """
    if outcome is None:
        outcome = df.columns[0]

    if target is None:
        if df[outcome].dtype == np.object:
            target = df.loc[0, outcome]
        else:
            target = "max"

    if encode:
        # Some utilities require original values
        df_orig = df.copy()
        outcome_orig = outcome
        target_orig = target

        encoder = DDTransformer(df)
        df = utilities.encode_dataframe(df, encoder)
        outcome = encoder.original_to_encoded_column(outcome)
        target = utilities.encode_value(df_orig, outcome_orig, target_orig, encoder)

    if sample:
        df, _ = utilities.sample_if_needed(
            df, target, outcome, random_state=random_state
        )

    data = io.BytesIO()
    df.to_parquet(data)
    data.seek(0)  # Reset the pointer as `to_parquet` leaves it at the end

    task = solve_start_file(outcome=outcome, target=target, data=data, **kwargs)
    result = solve_result(id=task["id"])

    rule = result["rule"]

    if encode:
        # We need to decode the rule if we encoded
        rule = utilities.decode_rule(rule, encoder)

    return rule
