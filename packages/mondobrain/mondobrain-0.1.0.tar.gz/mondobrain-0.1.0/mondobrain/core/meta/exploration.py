import mondobrain as mb
from mondobrain.types import (
    ClassStartOptions,
    Direction,
    ExclusionSetStartOptions,
    MetaResult,
)


class BaseExploration:
    def explore(self, options: dict) -> MetaResult:
        raise NotImplementedError(".explore() must be overridden")


class ClassExploration(BaseExploration):
    """
    Class exploration strategy for MetaMondo

    Gathers feature rules by learning on multiple classes in multiple directions.

    Parameters
    ----------
    classes: array of string or None (optional), default=None
        A list of classes to explore.  If None, explore all classes.

    direction: 'in', 'out', 'both', or None (optional), default='both'
        Direction to explore each outcome class.  Only applicable for discrete
        outcomes.
        - 'in': find feature rules inside of the outcome class
        - 'out': find feature rules outside of the outcome class
        - 'both': do both in and out
        - None: do not explore directions (for continuous outcome variables)

    inverse: 'in_rule' or None (optional), default=None
        Strategy for finding "inverse" rules when a feature rule is found
        - 'in_rule': find an inverse rule for the same class, opposite direction
            inside the feature rule
        - None: do not add inverse rules

    depth: int (optional), default=1
        The number of exploration cycles.

    parallel: bool (optional), default=False
        Explore each outcome class independently and in parallel.

    """

    def __init__(
        self,
        classes=None,
        direction=Direction.both,
        inverse=None,
        depth=1,
        parallel=False,
    ):
        super(ClassExploration, self).__init__()
        self.classes = classes
        self.direction = direction
        self.inverse = inverse
        self.depth = depth
        self.parallel = parallel

    def explore(self, options: dict) -> MetaResult:
        options = ClassStartOptions(**options)
        options.classes = self.classes
        options.direction = self.direction
        options.inverse = self.inverse
        options.depth = self.depth
        options.parallel = self.parallel

        task = mb.api.meta_class_start(**options.dict())
        result = mb.api.meta_result(id=task["id"])

        return MetaResult(**result)


class ExclusionSetExploration(BaseExploration):
    """
    Exclusion set exploration strategy for MetaMondo

    Gathers feature rules by learning a rule, then learning another rule on the
    exclusion set, repeating until the exclusion set reaches a minimum size.

    Parameters
    ----------
    min_size: int (optional), default=10
        The minimum size of the exclusion set.  Stops exploration when the
        exclusion set is below this size.

    classes: array of string or None (optional), default=None
        A list of classes to explore.  If None, explore all classes.

    direction: 'in', 'out', 'both', or None (optional), default='both'
        Direction to explore each outcome class.  Only applicable for discrete
        outcomes.
        - 'in': find feature rules inside of the outcome class
        - 'out': find feature rules outside of the outcome class
        - 'both': do both in and out
        - None: do not explore directions (for continuous outcome variables)

    depth: int (optional), default=1
        The number of exploration cycles.

    parallel: bool (optional), default=False
        Explore each outcome class independently and in parallel.

    """

    def __init__(
        self,
        min_size=10,
        classes=None,
        direction=Direction.both,
        depth=1,
        parallel=False,
    ):
        super(ExclusionSetExploration, self).__init__()
        self.min_size = min_size
        self.classes = classes
        self.direction = direction
        self.depth = depth
        self.parallel = parallel

    def explore(self, options: dict) -> MetaResult:
        options = ExclusionSetStartOptions(**options)
        options.min_size = self.min_size
        options.classes = self.classes
        options.direction = self.direction
        options.depth = self.depth
        options.parallel = self.parallel

        task = mb.api.meta_exclusion_set_start(**options.dict())
        result = mb.api.meta_result(id=task["id"])

        return MetaResult(**result)
