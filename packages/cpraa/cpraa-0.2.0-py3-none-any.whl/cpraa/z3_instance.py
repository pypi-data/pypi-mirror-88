from typing import Dict, List, Tuple
# import os

import z3

import assignments
import DPGM as AF


class Z3Instance:
    """Class to bundle the declared probabilistic variables, the underlying full joint distribution."""

    def __init__(self, af: AF.DPGM, assume_independence=False):
        self.af = af
        self.assume_independence = assume_independence  # when this flag is True, no full joint probability is built

        self.full_joint_prob_vars: Dict[str, z3.ArithRef] = dict()
        self.full_joint_assignments: List[List[Tuple[AF.Node, bool]]] = []
        self.other_prob_vars: Dict[str, z3.ArithRef] = dict()
        self.real_vars: Dict[str, z3.ArithRef] = dict()
        self.constraints = set()

        self.edge_prob_vars: Dict[AF.Edge, z3.ArithRef] = dict()
        self.edge_constraints = set()
        self.edge_prob_vars_generated = False

        # create a z3 solver
        self.context = z3.Context()
        self.solver = z3.Solver(ctx=self.context)

        if not self.assume_independence:
            self._generate_full_prob_vars()
            # # serialize the constraints for the full joint distribution
            # path = os.path.splitext(self.af.path)[0]  # strip the .tgf extension
            # path1 = path + "_full-joint-probvars.py"
            # with open(path1, "w") as f:
            #     f.write(repr(self.full_joint_prob_vars))
            # print("Written to", path1)
            # path2 = path + "_constraints.py"
            # with open(path2, "w") as f:
            #     f.write(repr(self.constraints))

    def generate_edge_vars(self):
        """
        Generates a probabilistic variable for each edge. If an edge has a value or interval given, those are added as
        constraints.
        """
        if self.edge_prob_vars_generated:
            # There might be several calls to generate_edge_vars, but we want to add the constraints only once.
            return
        for edge in self.af.get_edges():
            self.edge_prob_vars[edge] = z3.Real(edge.label, self.context)
            edge_prob_var = self.edge_prob_vars[edge]
            if edge.value is not None:
                self.edge_constraints.add(edge_prob_var == edge.value)
                assert edge.interval is None, "both edge.value and edge.interval where given"
            elif edge.interval is not None:
                (val_min, val_max) = edge.interval
                self.edge_constraints.add(z3.And(edge_prob_var >= val_min, edge_prob_var <= val_max, self.context))
            else:
                self.edge_constraints.add(edge_prob_var >= 0)
                self.edge_constraints.add(edge_prob_var <= 1)
        self.edge_prob_vars_generated = True

    def get_edge_var(self, edge: AF.Edge):
        if not self.edge_prob_vars_generated:
            self.generate_edge_vars()
        return self.edge_prob_vars[edge]

    def _generate_full_prob_vars(self):
        """Adds variables for the full joint distribution to the context. Adds the constraint that they sum to one."""
        constraint = 0
        if not self.full_joint_assignments:
            self.full_joint_assignments = assignments.generate(self.af.get_nodes())
        for assignment in self.full_joint_assignments:
            assignment_prob_name = prob_name(assignment)

            prob_var = z3.Real(assignment_prob_name, self.context)
            self.full_joint_prob_vars[assignment_prob_name] = prob_var
            self.constraints.add(prob_var >= 0)
            self.constraints.add(prob_var <= 1)
            constraint += prob_var

        constraint = 1 == constraint
        self.constraints.add(constraint)

    def get_node_prob_var(self, node: AF.Node):
        return self.get_prob_var([(node, True)])

    def get_prob_var(self, assignment: List[AF.Tuple[AF.Node, bool]]):
        """
        Get the probabilistic variable corresponding to a full or partial assignment.
        If it does not exist yet, it is created along with the constraints 'new_var >= 0', 'new_var <= 1' and the
        representation of new_var as sum of the full joint variables.
        """
        assert assignment, "empty assignment given"

        prob_var_name = prob_name(assignment)
        if prob_var_name in self.other_prob_vars:
            return self.other_prob_vars[prob_var_name]
        if prob_var_name in self.full_joint_prob_vars:
            return self.full_joint_prob_vars[prob_var_name]

        prob_var = z3.Real(prob_var_name, self.context)
        self.other_prob_vars[prob_var_name] = prob_var
        self.constraints.add(prob_var >= 0)
        self.constraints.add(prob_var <= 1)
        if not self.assume_independence:
            self.constraints.add(self.sum_out(assignment, prob_var))
        return prob_var

    def get_node_value(self, node: AF.Node, model: z3.ModelRef):
        """
        Get the value assigned to a node's probabilistic variable by the given model.
        :return: The value as float
        """
        return get_prob_var_value(self.get_node_prob_var(node), model)

    def create_real_var(self, name: str):
        """
        Creates and returns an auxiliary z3 real variable.
        """
        if name in self.real_vars:
            raise ValueError("A real var with name '" + name + "' already exists.")
        real_var = z3.Real(name, self.context)
        self.real_vars[name] = real_var
        return real_var

    def positive_cnf_probvars(self, clauses: List[List[AF.Node]]) -> List[z3.ArithRef]:
        """
        Given a positive CNF (i.e. without any negation in front of literals), return all prob vars of the full joint
        distribution which satisfy the CNF.
        E.g. for  (A OR B) AND (B OR C), given as [[A, B], [B, C]], return p_A_B_C, p_A_B_nC, p_nA_B_C, p_nA_B_nC and
        p_A_nB_C.
        :param clauses: A list of the conjunctive clauses of the positive CNF
        :return: A list of all prob vars from the full joint distribution which satisfy the CNF
        """
        candidates = [set()]
        given_arguments = set()
        for clause in clauses:
            given_arguments.update(clause)
            clause_assignments = assignments.generate(clause, [False, True])
            # Clauses contain disjunctive literals, so a true assignment is any assignment which assigns true at least
            # once. Filter out the first result from 'assignments' function because this assigns False to all literals.
            true_clause_assignments = clause_assignments[1:]

            new_candidates = []
            for candidate in candidates:
                # e.g. candidate = [(A, True), (B, False)]
                for true_clause_assignment in true_clause_assignments:
                    # e.g. true_clause_assignment = [(B, False), (C, True)]
                    # check whether the arguments appearing in both assignments are assigned the same value
                    skip = False
                    for (node, b) in true_clause_assignment:
                        if (node, not b) in candidate:
                            skip = True
                            break
                    # if so, add the new arguments to the candidate
                    if not skip:
                        new_candidate = candidate.copy()
                        new_candidate.update(true_clause_assignment)
                        new_candidates.append(new_candidate)
            candidates = new_candidates

        # arguments not present in the cnf can take on any value, so each previous candidate is extended by all possible
        # assignments of the remaining arguments
        remaining_arguments = set(self.af.get_nodes()).difference(given_arguments)
        remaining_assignments = assignments.generate(list(remaining_arguments))
        final_candidates = []
        for candidate in candidates:
            for remaining_assignment in remaining_assignments:
                final_candidate = candidate.copy()
                final_candidate.update(remaining_assignment)
                final_candidates.append(final_candidate)

        prob_vars = [self.get_prob_var(list(candidate)) for candidate in final_candidates]
        return prob_vars

    def sum_out(self, part_assignment: List[Tuple[AF.Node, bool]], part_assignment_prob_var):
        """[(A,True),(B,False)], [A,B,C] -> p_A_nB = p_A_nB_C + p_A_nB_nC"""
        part_assignment_args = [arg for (arg, _) in part_assignment]
        remaining_args = [arg for arg in self.af.get_nodes() if arg not in part_assignment_args]
        sum_list = []
        for assignment in assignments.generate(remaining_args):
            full_assignment = part_assignment + assignment
            full_assignment_name = prob_name(full_assignment)
            prob_var = self.full_joint_prob_vars[full_assignment_name]
            sum_list.append(prob_var)
        constraint = part_assignment_prob_var == z3.Sum(sum_list)
        return constraint
    
    def add_constraints(self, constraints):
        for cons in constraints:
            self.constraints.add(cons)

    def run(self, prob_constraints):
        """
        Add all constraints to the solver and check for a satisfying assignment.
        :param prob_constraints: a list of constraints
        :return: A z3 CheckSatResult, i.e. sat, unsat or unknown
        """
        self.solver.reset()
        self.solver.add(self.constraints)
        # print("self.constraints:", self.constraints)
        self.solver.add(self.edge_constraints)
        # print("self.af_constraints", self.af_constraints)
        self.solver.add(prob_constraints)
        # print("prob_constraints", prob_constraints)

        result = self.solver.check()
        # print(self.solver.to_smt2())
        # print(result)
        # if result == z3.sat:
        #     model = self.solver.model()
        #     self.print_distribution(model)
        #     # for node in self.af.get_nodes():
        #     #     prob = model.eval(self.get_node_prob_var(node))
        #     #     print(node.name, prob)
        return result

    def print_distribution(self, model: z3.ModelRef, nodes=None, only_positive=False):
        """
        Print distribution given by the model over the assignments of the given nodes.
        If no list of nodes is given, the distributions over all nodes in the AF is given.
        """
        if not nodes:
            nodes = self.af.get_nodes()
        node_assignments = assignments.generate(nodes)
        for assignment in node_assignments:
            prob_var = self.get_prob_var(assignment)
            value = get_prob_var_value(prob_var, model)
            if not only_positive or value > 0:
                assignments.print_assignment_prob(assignment, value)
                # print(prob_var, "=", value)

    def print_formatted_distribution(self, model: z3.ModelRef, format_string: str = ""):
        """
        Print distribution given by the model in the formats given by the format string: (M) marginal node
        probabilities, (F) full distribution, (S) support of distribution, (Z) Z3 output, (T) SMT2 format.
        """
        for char in format_string:
            if char == "M":
                for node in self.af.get_nodes():
                    print(node.name, "=", self.get_node_value(node, model))
            elif char == "F":
                self.print_distribution(model)
            elif char == "S":
                print("Support:")
                self.print_distribution(model, only_positive=True)
            elif char == "Z":
                print(model)
            elif char == "T":
                print(model.sexpr())
            else:
                print("Unknown distribution format '" + char + "'.")

    def generate_independence_constraints(self, a: List[AF.Node], b: List[AF.Node], c: List[AF.Node]):
        """
        Generate constraints stating that the nodes in A are independent of the nodes in B given the nodes in C.
        For each assignment a_A, a_B and a_C, we have
                 P(a_A | a_BC) = P(a_A | a_C)
        <=> P(a_ABC) / P(a_BC) = P(a_A | a_C)
        <=>           P(a_ABC) = P(a_BC) * P(a_A | a_C)   (this would suffice if P(a_A | a_C) is known from a CPT)
        <=>           P(a_ABC) = P(a_BC) * P(a_AC) / P(a_C)
        <=>  P(a_C) * P(a_ABC) = P(a_BC) * P(a_AC)
        """
        all_nodes = sorted(a + b + c)
        constraints = []
        for assignment in assignments.generate(all_nodes):
            a_ABC = assignment
            p_ABC = self.get_prob_var(a_ABC)
            a_BC = [(node, v) for (node, v) in assignment if node in b or node in c]
            p_BC = self.get_prob_var(a_BC)
            a_C = [(node, v) for (node, v) in assignment if node in c]
            if a_C:
                p_C = self.get_prob_var(a_C)
                a_AC = [(node, v) for (node, v) in assignment if node in a or node in c]
                p_AC = self.get_prob_var(a_AC)
                constraints.append(p_C * p_ABC == p_BC * p_AC)
            else:
                # a_C is empty, i.e., the constraint is an unconditional independence constraint
                a_A = [(node, v) for (node, v) in assignment if node in a]
                p_A = self.get_prob_var(a_A)
                constraints.append(p_ABC == p_BC * p_A)
        return constraints


def prob_name(assignment: List[AF.Tuple[AF.Node, bool]]) -> str:
    """
    Generates a fixed name for any assignment.
    Expects a list of tuples of nodes matched to True or False, i.e. [(node_B, False), (node_C, True)].
    Generates a name for the probability of the conjunction of the nodes, i.e. 'p_nB_C'.
    The order is determined by node IDs.
    """
    name = "p"
    assignment.sort()
    for (arg, b) in assignment:
        name += "_"
        if not b:
            name += "n"
        name += arg.name
    return name


def get_prob_var_value(prob_var, model: z3.ModelRef):
    """
    Get the value assigned to a probabilistic variable by the given model.
    :return: The value as float
    """
    # Based on https://stackoverflow.com/a/12600208/6620204
    value = model.eval(prob_var)
    if z3.is_int_value(value):
        return value.as_long()
    elif z3.is_rational_value(value):
        return float(value.numerator_as_long())/float(value.denominator_as_long())
    elif z3.is_algebraic_value(value):
        approx_value = value.approx(20)
        return float(approx_value.numerator_as_long())/float(approx_value.denominator_as_long())
    else:
        raise ValueError("Unable to convert to float: " + str(value))
