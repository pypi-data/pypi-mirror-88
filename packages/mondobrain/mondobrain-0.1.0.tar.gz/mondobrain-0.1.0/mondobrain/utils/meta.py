from typing import Dict, List

import pandas as pd

from mondobrain.core.frame import MondoDataFrame
from mondobrain.dd_transformer import DDTransformer
from mondobrain.types import ContinuousFilter, Meta, MetaRule
from mondobrain.utils import utilities

from .constants import RULE_PREFIX


def get_meta_name(meta: Meta, with_stats: bool = False) -> str:
    class_lbl = "[{0}]".format(meta.class_)
    dir_lbl = "[dir={0}]".format(meta.direction) if meta.direction else ""
    inv_lbl = "[inv={0}]".format(meta.inverse) if meta.inverse else ""
    depth_lbl = "[d={0}]".format(meta.depth) if meta.depth else ""
    iter_lbl = "[i={0}]".format(meta.iteration) if meta.iteration else ""
    score_lbl = "[z={:.3f}]".format(float(meta.score)) if with_stats else ""
    size_lbl = "[n={:.0f}]".format(float(meta.size)) if with_stats else ""

    return "{0}{1}{2}{3}{4}{5}{6}{7}".format(
        RULE_PREFIX,
        class_lbl,
        dir_lbl,
        iter_lbl,
        inv_lbl,
        depth_lbl,
        score_lbl,
        size_lbl,
    )


def update_meta(rule: MetaRule, meta: Meta = None):
    if not rule.meta:
        rule.meta = Meta()

    if meta:
        if meta.iteration:
            rule.meta.iteration = meta.iteration
        if meta.depth:
            rule.meta.depth = meta.depth
        if meta.class_:
            rule.meta.class_ = meta.class_
        if meta.direction:
            rule.meta.direction = meta.direction
        if meta.inverse:
            rule.meta.inverse = meta.inverse
        if meta.score:
            rule.meta.score = meta.score
        if meta.size:
            rule.meta.size = meta.size

    rule.meta.name = get_meta_name(rule.meta)


def decode_meta_rules(
    rules: List[MetaRule], mdf: MondoDataFrame, outcome: str, encoder: DDTransformer,
) -> List[MetaRule]:
    decoded_rules = []
    meta_rule_name_map = {}

    if mdf[outcome].var_type == "discrete":
        for meta_rule in rules:
            old_name = meta_rule.meta.name

            meta_decoded = Meta(
                class_=utilities.decode_value(
                    mdf[outcome], meta_rule.meta.class_, encoder
                )
            )
            update_meta(meta_rule, meta_decoded)

            new_name = meta_rule.meta.name
            meta_rule_name_map[old_name] = new_name

        for meta_rule in rules:
            meta_rule_dict = meta_rule.dict()
            rule_decoded = utilities.decode_rule(meta_rule_dict["rule"], encoder)

            old_keys = [
                key for key, cond in rule_decoded.items() if key.startswith(RULE_PREFIX)
            ]
            for key in old_keys:
                new_key = meta_rule_name_map[key]
                rule_decoded[new_key] = rule_decoded.pop(key)

            meta_rule_decoded = {
                "rule": rule_decoded,
                "meta": meta_rule_dict["meta"],
            }

            decoded_rules.append(MetaRule(**meta_rule_decoded))
    else:
        for meta_rule in rules:
            meta_rule_dict = meta_rule.dict()
            rule_decoded = utilities.decode_rule(meta_rule_dict["rule"], encoder)
            meta_rule_decoded = {
                "rule": rule_decoded,
                "meta": meta_rule_dict["meta"],
            }

            decoded_rules.append(MetaRule(**meta_rule_decoded))

    return decoded_rules


def print_rule_trees(rules: List[MetaRule], class_: str = None, depth: int = None):
    rule_map = __get_rule_map(rules)

    filt_rules = rules
    if class_:
        filt_rules = [x for x in filt_rules if class_ == x.meta.class_]
    if depth:
        filt_rules = [x for x in filt_rules if depth == x.meta.depth]

    for rule in filt_rules:
        __print_rule_tree_helper(rule, rule_map, is_root=True)


def apply_meta_rules_to_df(rules: List[MetaRule], df: pd.DataFrame):
    filt_rules = []

    for rule in rules:
        if rule.meta.name not in df.columns:
            for key, cond in rule.rule.items():
                if type(cond) is ContinuousFilter:
                    rule.rule[key] = cond.dict()

            filt_rules.append(rule)

    rule_map = __get_rule_map(filt_rules)
    curr_df = df.copy()

    feat_rule_map = {}

    for rule in filt_rules:
        feat_rule_map[rule.meta.name] = []

        for key, cond in rule.rule.items():
            if key.startswith(RULE_PREFIX):
                feat_rule_map[rule.meta.name].append(key)

    while feat_rule_map:
        applied_rules = []

        for name, feat_rules in feat_rule_map.items():
            if len(feat_rules) == 0:
                rule = rule_map[name]
                df_rule = utilities.apply_rule_to_df(curr_df, rule.rule)

                curr_df[name] = curr_df.index.isin(df_rule.index).astype(int)
                applied_rules.append(name)

        if len(applied_rules) == 0:
            break

        for name in applied_rules:
            del feat_rule_map[name]

        for name, feat_rules in feat_rule_map.items():
            feat_rule_map[name] = [x for x in feat_rules if x not in applied_rules]

    return curr_df


def __get_rule_map(rules: List[MetaRule]) -> Dict[str, MetaRule]:
    return {x.meta.name: x for x in rules}


def __print_rule_tree_helper(
    rule: MetaRule,
    rule_map: Dict[str, MetaRule],
    prefix: str = "",
    is_root: bool = False,
):

    TREE_SPACE, TREE_BRANCH, TREE_TEE, TREE_END = "    ", "│   ", "├── ", "└── "

    filters = rule.rule

    if is_root:
        print(get_meta_name(rule.meta, with_stats=True))

    pointers = [TREE_TEE] * (len(filters) - 1) + [TREE_END]

    for pointer, col in zip(pointers, filters):
        filt = filters[col]
        col_lbl = prefix + pointer + col + ":"

        if type(filt) is str:
            print(col_lbl, filt)
        else:
            if filt.lo == filt.hi:
                print(col_lbl, filt.lo)
            else:
                print(col_lbl, "[{0}, {1}]".format(filt.lo, filt.hi))

        if col.startswith(RULE_PREFIX):
            extension = TREE_BRANCH if pointer == TREE_TEE else TREE_SPACE

            __print_rule_tree_helper(rule_map[col], rule_map, prefix=prefix + extension)

    if is_root:
        print()
