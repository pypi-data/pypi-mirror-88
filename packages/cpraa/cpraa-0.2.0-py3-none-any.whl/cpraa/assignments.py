from typing import List, Tuple, Any

Assignment = List[Tuple[Any, Any]]  # type alias

DEFAULT_PRECISION = 5


def generate(ar: list, br: list = (False, True)) -> List[Assignment]:
    """
    Generates all possible assignments of the elements in list 'ar' to elements of list 'br'.
    E.g. ar = [x,y], br = [0,1] -> [[(x,0),(y,0)], [(x,0),(y,1)], [(x,1),(y,0)], [(x,1),(y,1)]]
    """
    combinations = [[]]

    for a in ar:
        next_combinations = []
        for c in combinations:
            for b in br:
                new_c = c.copy()
                new_c.append((a, b))
                next_combinations.append(new_c)
        combinations = next_combinations
    return combinations


def repr_assignment(a: Assignment) -> str:
    strings = []
    for (node, b) in a:
        strings.append((" " if b else "-") + str(node))
    return ",".join(strings)


def repr_assignment_prob(a: Assignment, prob: float, given: Assignment = None, precision=DEFAULT_PRECISION):
    cond = "P(" + repr_assignment(a) + ("|" + repr_assignment(given) if given else "") + ")"
    return cond + " = " + "{:0.{p}g}".format(prob, p=precision)


def print_assignment_prob(a: Assignment, prob: float, precision=DEFAULT_PRECISION):
    print(repr_assignment_prob(a, prob, [], precision))
