from typing import List, Set

import z3

import DPGM as AF
from labeling import Labeling
from labeling_scheme import LabelingScheme
from semantics import Semantics
from z3_instance import Z3Instance


def get_model(z3i: Z3Instance, semantics: List[Semantics], constraints=None):
    """
    Check if a distribution satisfying the constraints of all semantics plus potential additional constraints exists.
    If so, return it as a model.

    :param z3i: the underlying z3 instance with the AF
    :param semantics: a list of semantics
    :param constraints: optional list of additional constraints
    :return: A model if one exists, None otherwise
    """
    if not constraints:
        constraints = []

    for sem in semantics:
        # print(sem.__class__.__name__, sem.get_constraints())
        constraints.extend(sem.get_constraints())

    result = z3i.run(constraints)
    if result == z3.sat:
        return z3i.solver.model()
    else:
        return None


def get_satisfying_labeling(z3i: Z3Instance, lab: LabelingScheme, semantics: List[Semantics]) -> Labeling:
    """
    Get a labeling satisfying the given semantics under the given labeling scheme. Returns None if no such labeling
    exists.

    :param z3i: the underlying z3 instance with the AF
    :param lab: a labeling scheme
    :param semantics: a list of semantics
    :return: A labeling or None
    """
    model = get_model(z3i, semantics)
    if model:
        return Labeling(lab, z3i, model)


def get_all_satisfying_labelings(z3i: Z3Instance, lab: LabelingScheme, semantics: List[Semantics]) -> Set[Labeling]:
    """
    Compute all labelings under the given labeling scheme that satisfy the given semantics.

    :param z3i: the underlying z3 instance with the AF
    :param lab: a labeling scheme
    :param semantics: a list of semantics
    :return: a list of labelings
    """
    for sem in semantics:
        # print(sem.__class__.__name__, sem.get_constraints())
        z3i.add_constraints(sem.get_constraints())
    # print("z3i.constraints: ", z3i.constraints)
    # test overall satisfiability
    result = z3i.run([])
    print("Overall satisfiability:", result)
    if result != z3.sat:
        return set()

    candidate_constraints = [[]]
    labelings = set()
    num_of_checks = 1

    # num_nodes = len(z3i.af.get_nodes())
    for node in z3i.af.get_nodes():
        print(node.name)
        next_candidate_constraints = []
        for candidate_constraint in candidate_constraints:
            for const in lab.get_constraints(node, z3i):
                new_candidate_constraint = candidate_constraint.copy()
                new_candidate_constraint.append(const)
                # add candidate constraints to solver
                z3i.solver.push()  # this adds an backtracking point
                # print(z3i.solver)
                z3i.solver.add(new_candidate_constraint)
                # print(z3i.solver)
                result = z3i.solver.check()
                num_of_checks += 1
                if result == z3.sat:
                    # print("new_candidate_constraint", new_candidate_constraint)
                    next_candidate_constraints.append(new_candidate_constraint)
                    model = z3i.solver.model()
                    labeling = Labeling(lab, z3i, model)
                    labelings.add(labeling)
                    # print("model", model)
                    # print("labeling:", labeling)
                #  remove candidate constraints from solver
                z3i.solver.pop()  # go back to the backtracking point
        candidate_constraints = next_candidate_constraints

    print("Finished. Performed", num_of_checks, "checks.")
    return labelings


def check_credulous_threshold_acceptance(z3i: Z3Instance, semantics: List[Semantics], threshold: float,
                                         argument: AF.Node):
    """
    Under a given threshold, check if the given argument is credulously accepted, i.e. there exists at least one
    distribution satisfying all given semantics that assigns the argument a probability greater or equal to the
    threshold.

    :param z3i: the underlying z3 instance with the AF
    :param semantics: a list of semantics
    :param threshold: a float from the interval [0,1]
    :param argument: an argument from the AF
    :return: True + a model if one exists, False otherwise
    """
    argument_prob = z3i.get_node_prob_var(argument)
    constraints = [argument_prob >= threshold]
    model = get_model(z3i, semantics, constraints)
    if model:
        return True, model
    else:
        return False, None


def check_credulous_acceptance(z3i: Z3Instance, semantics: List[Semantics], argument: AF.Node):
    """
    Check if the given argument is credulously accepted, i.e. there exists at least one distribution satisfying all
    given semantics that assigns the argument probability one.

    :param z3i: the underlying z3 instance with the AF
    :param semantics: a list of semantics
    :param argument: an argument from the AF
    :return: True + a model if one exists, False otherwise
    """
    threshold = 1
    return check_credulous_threshold_acceptance(z3i, semantics, threshold, argument)


def check_skeptical_threshold_acceptance(z3i: Z3Instance, semantics: List[Semantics], threshold: float,
                                         argument: AF.Node):
    """
    Under a given threshold, check if the given argument is skeptically accepted, i.e. all distributions that satisfy
    all given semantics assign the argument a probability greater or equal to the threshold.

    :param z3i: the underlying z3 instance with the AF
    :param semantics: a list of semantics
    :param threshold: a float from the interval [0,1]
    :param argument: an argument from the AF
    :return: True or False + counter example
    """
    # "check if for all satisfying distributions, P(A) >= t holds"
    # <=> not "check if for one satisfying distribution, P(A) < t holds"
    argument_prob = z3i.get_node_prob_var(argument)
    constraints = [argument_prob < threshold]
    model = get_model(z3i, semantics, constraints)
    if model:
        return False, model
    else:
        return True, None


def check_skeptical_acceptance(z3i: Z3Instance, semantics: List[Semantics], argument: AF.Node):
    """
    Check if the given argument is skeptically accepted, i.e. all distributions that satisfy all given semantics assign
    the argument probability one.

    :param z3i: the underlying z3 instance with the AF
    :param semantics: a list of semantics
    :param argument: an argument from the AF
    :return: True or False + counter example
    """
    threshold = 1
    return check_skeptical_threshold_acceptance(z3i, semantics, threshold, argument)
