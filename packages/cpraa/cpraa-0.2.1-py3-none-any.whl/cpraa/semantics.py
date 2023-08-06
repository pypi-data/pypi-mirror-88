from typing import List, Type

import z3

import assignments
import classical_semantics as classical
import DPGM as AF
import z3_instance as zi


class Semantics:
    def __init__(self, z3_instance: zi.Z3Instance):
        self.context = z3_instance.context
        self.af = z3_instance.af
        self.z3i = z3_instance
        self.constraints: List[z3.BoolRef] = []

        self.generate_constraints()

    def generate_constraints(self):
        # implemented by subclasses
        pass

    def get_constraints(self):
        return self.constraints


####################
# trivial semantics
####################

class Min(Semantics):
    """
    Minimality semantics: All nodes must hold with probability 0.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            self.constraints.append(node_prob == 0)


class Neu(Semantics):
    """
    Neutrality semantics: All nodes must hold with probability 0.5.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            self.constraints.append(node_prob == 0.5)


class Max(Semantics):
    """
    Maximality semantics: All nodes must hold with probability 1.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            self.constraints.append(node_prob == 1)


class Dirac(Semantics):
    """
    Dirac semantics: All nodes must hold with either probability 0 or 1.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            self.constraints.append(z3.Or(node_prob == 0, node_prob == 1))


class Ter(Semantics):
    """
    Ternary semantics: All nodes must hold with either probability 0, 0.5 or 1.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            self.constraints.append(z3.Or(node_prob == 0, node_prob == 0.5, node_prob == 1))


################################
# semantics by Hunter and Thimm
################################

class Fou(Semantics):
    """
    Foundedness semantics: Initial nodes must hold with probability 1.
    """
    def generate_constraints(self):
        for node in self.af.get_initial_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            self.constraints.append(node_prob == 1)


class SFou(Semantics):
    """
    Semi-Foundedness semantics: Initial nodes must hold with probability >= 0.5.
    """
    def generate_constraints(self):
        for node in self.af.get_initial_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            self.constraints.append(node_prob >= 0.5)


class Inv(Semantics):
    """
    Involution semantics: p_A = 1 - p_B for all attacks A -> B.
    """
    def generate_constraints(self):
        for edge in self.af.get_edges():
            prob_node_from = self.z3i.get_node_prob_var(edge.node_from)
            prob_node_to = self.z3i.get_node_prob_var(edge.node_to)
            self.constraints.append(prob_node_from == 1 - prob_node_to)


class Rat(Semantics):
    """
    Rationality semantics: p_A > 0.5 implies p_B <= 0.5 for all attacks A -> B.
    """
    def generate_constraints(self):
        for edge in self.af.get_edges():
            prob_node_from = self.z3i.get_node_prob_var(edge.node_from)
            prob_node_to = self.z3i.get_node_prob_var(edge.node_to)
            self.constraints.append(z3.Implies(prob_node_from > 0.5, prob_node_to <= 0.5, ctx=self.context))


class Coh(Semantics):
    """
    Coherency semantics: p_A <= 1 - p_B for all attacks A -> B.
    """
    def generate_constraints(self):
        for edge in self.af.get_edges():
            prob_node_from = self.z3i.get_node_prob_var(edge.node_from)
            prob_node_to = self.z3i.get_node_prob_var(edge.node_to)
            self.constraints.append(prob_node_from <= 1 - prob_node_to)


class Opt(Semantics):
    """
    Optimism semantics: p_A >= 1 - Sum p_B for all attackers B of A.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            if node.is_initial():
                self.constraints.append(node_prob == 1)
                continue
            summation = z3.Sum([self.z3i.get_node_prob_var(attacker) for attacker in node.get_parents()])
            self.constraints.append(node_prob >= 1 - summation)


class SOpt(Semantics):
    """
    Semi-optimism semantics: p_A >= 1 - Sum p_B for all attackers B of A iff A has at least one attacker.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            if node.is_initial():
                continue
            node_prob = self.z3i.get_node_prob_var(node)
            summation = z3.Sum([self.z3i.get_node_prob_var(attacker) for attacker in node.get_parents()])
            self.constraints.append(node_prob >= 1 - summation)


class Jus(Semantics):
    """
    Justifiability semantics: Coherency and optimism constraints hold.
    """
    def generate_constraints(self):
        opt = Opt(self.z3i)
        coh = Coh(self.z3i)
        self.constraints.extend(opt.get_constraints() + coh.get_constraints())


######################
# semantics by Baier
######################

class CF(Semantics):
    """
    Conflict-freeness semantics: p_A_B = 0 for all attacks A -> B.
    """
    def generate_constraints(self):
        for edge in self.af.get_edges():
            assignment = [(edge.node_from, True), (edge.node_to, True)]
            prob_var = self.z3i.get_prob_var(assignment)
            self.constraints.append(prob_var == 0)


# Admissibility

def almost_sure_defense_constraint(z3i: zi.Z3Instance, node: AF.Node):
    """
    Generate a constraint for an argument A to be almost-surely defended.
    This means for all attackers B->A, the probability that B is in turn attacked (and thus A is defended) is 1.
    That is, P(C1 or C2 or ... or Cn) = 1 for attackers C1...Cn of B, or, equivalently, P(nC1, nC2, ..., nCn) = 0.
    If an attacker B of A has no attackers, then A cannot be almost-surely defended, thus the impossible constraint
    'False' is added.
    """
    parents = list(node.get_parents())
    if len(parents) == 0:
        # unattacked nodes are necessarily defended
        return z3.BoolVal(True, ctx=z3i.context)

    # special treatment for the first attacker as starting point for nested Ands
    first_attacker = parents[0]
    first_attacker_parents = first_attacker.get_parents()
    if first_attacker_parents:
        assignment = []
        for defender in first_attacker_parents:
            assignment.append((defender, False))
        prob_var = z3i.get_prob_var(assignment)
        constraint = prob_var == 0
    else:
        return z3.BoolVal(False, ctx=z3i.context)

    for attacker in parents[1:]:
        attacker_parents = attacker.get_parents()
        if attacker_parents:
            assignment = []
            for defender in attacker_parents:
                assignment.append((defender, False))
            prob_var = z3i.get_prob_var(assignment)
            constraint = z3.And(constraint, prob_var == 0)
        else:
            return z3.BoolVal(False, ctx=z3i.context)
    return constraint


class WAdm(Semantics):
    """
    Weak admissibility semantics: CF and p_A = 1 implies A is almost-surely defended.
    """
    def generate_constraints(self):
        sCF = CF(self.z3i)
        self.constraints.extend(sCF.constraints)
        for node in self.af.get_nodes():
            if node.is_initial():
                # initial nodes are always almost-surely defended, thus the constraint would become 'p_A == 1 -> True'
                continue
            node_prob = self.z3i.get_node_prob_var(node)
            as_defense_constraint = almost_sure_defense_constraint(self.z3i, node)
            self.constraints.append(z3.Implies(node_prob == 1, as_defense_constraint, ctx=self.context))


class LabAdm(Semantics):
    def generate_constraints(self):
        sCF = CF(self.z3i)
        self.constraints.extend(sCF.constraints)
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            or_list = []
            for parent_node in node.get_parents():
                parent_node_prob = self.z3i.get_node_prob_var(parent_node)
                or_list.append(parent_node_prob == 1)
            self.constraints.append(z3.Implies(node_prob == 0, z3.Or(or_list, self.context), self.context))


class SLabAdm(Semantics):
    def generate_constraints(self):
        sCF = CF(self.z3i)
        self.constraints.extend(sCF.constraints)
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            if node.is_initial():
                continue
            or_list = []
            for parent_node in node.get_parents():
                parent_node_prob = self.z3i.get_node_prob_var(parent_node)
                or_list.append(parent_node_prob == 1)
            self.constraints.append(z3.Implies(node_prob == 0, z3.Or(or_list, self.context), self.context))


def open_interval_constraint(prob_var, context, low=0, high=1):
    return z3.And(prob_var > low, prob_var < high, context)


class LabCmp(Semantics):
    def generate_constraints(self):
        labAdm = LabAdm(self.z3i)
        self.constraints.extend(labAdm.constraints)
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            node_undec = open_interval_constraint(node_prob, self.context)
            or_list = []
            for parent_node in node.get_parents():
                parent_node_prob = self.z3i.get_node_prob_var(parent_node)
                self.constraints.append(z3.Implies(node_undec, parent_node_prob < 1, self.context))
                parent_undec = open_interval_constraint(parent_node_prob, self.context)
                or_list.append(parent_undec)
            self.constraints.append(z3.Implies(node_undec, z3.Or(or_list, self.context), self.context))


class SLabCmp(Semantics):
    def generate_constraints(self):
        sLabAdm = SLabAdm(self.z3i)
        self.constraints.extend(sLabAdm.constraints)
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            if node.is_initial():
                continue
            node_undec = open_interval_constraint(node_prob, self.context)
            or_list = []
            for parent_node in node.get_parents():
                parent_node_prob = self.z3i.get_node_prob_var(parent_node)
                self.constraints.append(z3.Implies(node_undec, parent_node_prob < 1, self.context))
                parent_undec = open_interval_constraint(parent_node_prob, self.context)
                or_list.append(parent_undec)
            self.constraints.append(z3.Implies(node_undec, z3.Or(or_list, self.context), self.context))


class PrAdm(Semantics):
    """
    Probabilistic admissibility semantics: CF and for all arguments B with attackers A1...An and attackees C1...Cm,
    P(C1 or ... or Cm) <= P(A1 or ... or An) holds. Equivalently, by negating each side and simplifying, we get
    P(nC1, ..., nCm) >= P(nA1, ..., nAn).
    """
    def generate_constraints(self):
        sCF = CF(self.z3i)
        self.constraints.extend(sCF.constraints)
        for node in self.af.get_nodes():
            node_parents = node.get_parents()
            if node_parents:
                attacker_assignment = [(attacker, False) for attacker in node_parents]
                attacker_prob_var = self.z3i.get_prob_var(attacker_assignment)
            else:
                # there are no attackers, so the prob of any attacker holding is 0
                # thus, in the negated view, the prob is 1
                attacker_prob_var = 1
            node_children = node.get_children()
            if node_children:
                attackee_assignment = [(attackee, False) for attackee in node_children]
                attackee_prob_var = self.z3i.get_prob_var(attackee_assignment)
            else:
                # there are no attackees, so the prob of any attackee holding is 0
                # thus, in the negated view, the prob is 1
                attackee_prob_var = 1
            if node_parents or node_children:
                self.constraints.append(attackee_prob_var >= attacker_prob_var)


class MinAdm(Semantics):
    """
    Min-admissibility semantics: CF and for every argument C, P(C) <= min_{B in Pre(C)} P(OR Pre(B)) holds.
    Equivalently, for all B in Pre(C) with Pre(B) = {A1, ..., An}, it holds P(C) <= 1 - P(nA1, ..., nAn).
    """
    def generate_constraints(self):
        sCF = CF(self.z3i)
        self.constraints.extend(sCF.constraints)
        for node in self.af.get_nodes():
            node_parents = node.get_parents()
            if node_parents:
                node_prob = self.z3i.get_node_prob_var(node)
                for attacker in node_parents:
                    attacker_parents = attacker.get_parents()
                    if attacker_parents:
                        assignment = [(defender, False) for defender in attacker_parents]
                        prob_var = self.z3i.get_prob_var(assignment)
                        self.constraints.append(node_prob <= 1 - prob_var)
                    else:
                        self.constraints.append(node_prob == 0)
            else:
                pass  # minAdm enforces no constraint for initial arguments


class JntAdm(Semantics):
    """
    Joint-admissibility semantics: CF and for every argument C, P(C) <= P(AND_{B in Pre(C)} (OR Pre(B))) holds.
    """
    def generate_constraints(self):
        sCF = CF(self.z3i)
        self.constraints.extend(sCF.constraints)
        for node in self.af.get_nodes():
            if node.is_initial():
                # for nodes without attackers, the constraint becomes P(C) <= 1, so we skip it
                continue
            node_prob = self.z3i.get_node_prob_var(node)
            # the positive cnf corresponding to AND_{B in Pre(C)} (OR Pre(B))
            cnf = [list(attacker.get_parents()) for attacker in node.get_parents()]
            if [] in cnf:
                # there is an attacker B which is not in turn attacked, thus P(AND_{B in Pre(C)} (OR Pre(B))) = 0
                self.constraints.append(node_prob == 0)
                continue

            prob_vars = self.z3i.positive_cnf_probvars(cnf)
            # self.constraints.append(node_prob <= z3.Sum(prob_vars))
            self.constraints.append(node_prob.__le__(z3.Sum(prob_vars)))


class ElmAdm(Semantics):
    """
    Element-wise admissibility semantics: If a probabilistic variable from the full joint distribution has positive
    probability, it needs to correspond to an admissible extension in the classical sense. That is, all prob vars
    corresponding to non-admissible extensions need to have probability zero.
    """
    def generate_constraints(self):
        sAdm = classical.Admissible(self.af)
        adm_extensions = sAdm.get_extensions()
        for assignment in self.z3i.full_joint_assignments:
            assignment_ext = set([node for (node, b) in assignment if b])
            if assignment_ext not in adm_extensions:
                prob_var = self.z3i.get_prob_var(assignment)
                self.constraints.append(prob_var == 0)


# Completeness

class WCmp(Semantics):
    """
    Weak completeness semantics: CF and p_A = 1 if and only if A is almost-surely defended.
    """
    def generate_constraints(self):
        sCF = CF(self.z3i)
        self.constraints.extend(sCF.constraints)
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            if node.is_initial():
                # every initial node is almost-surely defended
                self.constraints.append(node_prob == 1)
                continue
            as_defense_constraint = almost_sure_defense_constraint(self.z3i, node)
            self.constraints.append(z3.Implies(node_prob == 1, as_defense_constraint, ctx=self.context))
            self.constraints.append(z3.Implies(as_defense_constraint, node_prob == 1, ctx=self.context))


def prCmp_constraint(nodes: List[AF.Node], z3i: zi.Z3Instance) -> List[z3.BoolRef]:
    """
    Given a list of arguments, returns the constraints P(C) >= P(AND_{B in Pre(C)} (OR Pre(B))) for every argument C.
    """
    constraints = []
    for node in nodes:
        node_prob = z3i.get_node_prob_var(node)
        if node.is_initial():
            # for nodes without attackers, the constraint becomes P(C) >= 1
            constraints.append(node_prob == 1)
            continue
        # the positive cnf corresponding to AND_{B in Pre(C)} (OR Pre(B))
        cnf = [list(attacker.get_parents()) for attacker in node.get_parents()]
        if [] in cnf:
            # there is an attacker B which is not in turn attacked, thus P(AND_{B in Pre(C)} (OR Pre(B))) = 0
            # the constraint would be P(C) >= 0, so we skip it
            continue

        prob_vars = z3i.positive_cnf_probvars(cnf)
        constraints.append(node_prob >= z3.Sum(prob_vars))
    return constraints


class PrCmp(Semantics):
    """
    Probabilistic completeness semantics: Prob. admissible and P(C) >= P(AND_{B in Pre(C)} (OR Pre(B))) holds for all
    arguments C.
    """
    def generate_constraints(self):
        prAdm = PrAdm(self.z3i)
        self.constraints.extend(prAdm.constraints)
        self.constraints.extend(prCmp_constraint(self.af.get_nodes(), self.z3i))


class MinCmp(Semantics):
    """
    Min-complete semantics: Min-admissible and P(C) >= P(AND_{B in Pre(C)} (OR Pre(B))) holds for all arguments C.
    """
    def generate_constraints(self):
        minAdm = MinAdm(self.z3i)
        self.constraints.extend(minAdm.constraints)
        self.constraints.extend(prCmp_constraint(self.af.get_nodes(), self.z3i))


class JntCmp(Semantics):
    """
    Joint-complete semantics: CF and P(C) = P(AND_{B in Pre(C)} (OR Pre(B))) holds for all arguments C.
    """
    def generate_constraints(self):
        sCF = CF(self.z3i)
        self.constraints.extend(sCF.constraints)
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            if node.is_initial():
                # for nodes without attackers, the constraint becomes P(C) == 1
                self.constraints.append(node_prob == 1)
                continue
            # the positive cnf corresponding to AND_{B in Pre(C)} (OR Pre(B))
            cnf = [list(attacker.get_parents()) for attacker in node.get_parents()]
            if [] in cnf:
                # there is an attacker B which is not in turn attacked, thus P(AND_{B in Pre(C)} (OR Pre(B))) = 0
                self.constraints.append(node_prob == 0)
                continue
            prob_vars = self.z3i.positive_cnf_probvars(cnf)
            # self.constraints.append(node_prob == z3.Sum(prob_vars))
            self.constraints.append(node_prob.__eq__(z3.Sum(prob_vars)))


class ElmCmp(Semantics):
    """
    Element-wise completeness semantics: If a probabilistic variable from the full joint distribution has positive
    probability, it needs to correspond to a complete extension in the classical sense. That is, all prob vars
    corresponding to non-complete extensions need to have probability zero.
    """
    def generate_constraints(self):
        sCmp = classical.Complete(self.af)
        cmp_extensions = sCmp.get_extensions()
        for assignment in self.z3i.full_joint_assignments:
            assignment_ext = set([node for (node, b) in assignment if b])
            if assignment_ext not in cmp_extensions:
                prob_var = self.z3i.get_prob_var(assignment)
                self.constraints.append(prob_var == 0)


#####################
# semantics by Käfer
#####################

class WNorS(Semantics):
    """
    Weak not-or semantics without CF: Generates constraints p_A <= p_nB1_nB2_..._nBi for every non-initial argument A
    with attackers B1, ..., Bi for some i > 0.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            if node.is_initial():
                continue  # for initial nodes, the constraint would be 'p_A <= 1' which already exists
            node_prob = self.z3i.get_node_prob_var(node)
            assignment = [(attacker, False) for attacker in node.get_parents()]
            attackers_prob = self.z3i.get_prob_var(assignment)
            # self.constraints.append(node_prob <= attackers_prob)
            self.constraints.append(node_prob.__le__(attackers_prob))


class NorS(Semantics):
    """
    Not-or semantics without CF: Generates constraints p_A = p_nB1_nB2_..._nBi for every non-initial argument A with
    attackers B1, ..., Bi for some i > 0.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            if node.is_initial():
                continue
            node_prob = self.z3i.get_node_prob_var(node)
            assignment = [(attacker, False) for attacker in node.get_parents()]
            attackers_prob = self.z3i.get_prob_var(assignment)
            # self.constraints.append(node_prob == attackers_prob)
            self.constraints.append(node_prob.__eq__(attackers_prob))


class SNorS(Semantics):
    """
    Strong not-or semantics without CF. Generates constraints p_A = 1 for initial arguments and p_A = p_nB1_nB2_..._nBi
    for every non-initial argument A with attackers B1, ..., Bi for some i>0.
    Also the intersection of Nor and Fou.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            if node.is_initial():
                self.constraints.append(node_prob == 1)
            else:
                assignment = [(attacker, False) for attacker in node.get_parents()]
                attackers_prob = self.z3i.get_prob_var(assignment)
                # self.constraints.append(node_prob == attackers_prob)
                self.constraints.append(node_prob.__eq__(attackers_prob))


class WNor(Semantics):
    """
    Weak not-or semantics: Generates constraints for conflict-freeness and p_A <= p_nB1_nB2_..._nBi for every
    non-initial argument A with attackers B1, ..., Bi for some i > 0.
    """
    def generate_constraints(self):
        sCF = CF(self.z3i)
        self.constraints.extend(sCF.constraints)
        for node in self.af.get_nodes():
            if node.is_initial():
                continue  # for initial nodes, the constraint would be 'p_A <= 1' which already exists
            node_prob = self.z3i.get_node_prob_var(node)
            assignment = [(attacker, False) for attacker in node.get_parents()]
            attackers_prob = self.z3i.get_prob_var(assignment)
            # self.constraints.append(node_prob <= attackers_prob)
            self.constraints.append(node_prob.__le__(attackers_prob))


class Nor(Semantics):
    """
    Not-or semantics: Generates constraints for conflict-freeness and p_A = p_nB1_nB2_..._nBi for every non-initial
    argument A with attackers B1, ..., Bi for some i > 0.
    """
    def generate_constraints(self):
        sCF = CF(self.z3i)
        self.constraints.extend(sCF.constraints)
        for node in self.af.get_nodes():
            if node.is_initial():
                continue
            node_prob = self.z3i.get_node_prob_var(node)
            assignment = [(attacker, False) for attacker in node.get_parents()]
            attackers_prob = self.z3i.get_prob_var(assignment)
            # self.constraints.append(node_prob == attackers_prob)
            self.constraints.append(node_prob.__eq__(attackers_prob))


class SNor(Semantics):
    """
    Strong not-or semantics: Generates constraints for conflict-freeness, p_A = 1 for initial arguments and
    p_A = p_nB1_nB2_..._nBi for every non-initial argument A with attackers B1, ..., Bi for some i>0.
    Also the intersection of Nor and Fou and CF.
    """
    def generate_constraints(self):
        sCF = CF(self.z3i)
        self.constraints.extend(sCF.constraints)
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            if node.is_initial():
                self.constraints.append(node_prob == 1)
            else:
                assignment = [(attacker, False) for attacker in node.get_parents()]
                attackers_prob = self.z3i.get_prob_var(assignment)
                # self.constraints.append(node_prob == attackers_prob)
                self.constraints.append(node_prob.__eq__(attackers_prob))


class AF(Semantics):
    """
    Special semantics to add constraints for probability values or intervals specified in the AF input file.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            node_prob = self.z3i.get_node_prob_var(node)
            if node.value is not None:
                assert node.interval is None, "node with both value and interval set"
                # self.constraints.append(node_prob == node.value)
                self.constraints.append(node_prob.__eq__(node.value))
            elif node.interval is not None:
                low, high = node.interval
                # self.constraints.append(node_prob >= low)
                # self.constraints.append(node_prob <= high)
                self.constraints.append(node_prob.__ge__(low))
                self.constraints.append(node_prob.__le__(high))


class NNor(Semantics):
    """
    Noisy not-or semantics:  TODO
    per default without prior probabilities
    p_A_nB_nC = 1 * p_nB_nC
    p_A_nB_C  = (1 - t) * p_nB_C
    p_A_B_nC  = (1 - s) * p_B_nC
    p_A_B_C   = (1 - s ) * (1 - t) * p_B_C
    """
    def __init__(self, z3i: zi.Z3Instance, use_prior_probs=False):
        self.use_prior_probs = use_prior_probs
        super().__init__(z3i)

    def generate_constraints(self):
        # we use attack strength, so a prob_var should be created for each edge
        self.z3i.generate_edge_vars()

        for node in self.af.get_nodes():

            node_prior_prob_var = self.z3i.create_real_var("pr_" + node.name)  # e.g. pr_A
            if self.use_prior_probs:
                if node.value is not None:
                    # self.constraints.append(node_prior_prob_var == node.value)
                    self.constraints.append(node_prior_prob_var.__eq__(node.value))
                elif node.interval is not None:
                    i_min, i_max = node.interval
                    self.constraints.append(z3.And(node_prior_prob_var >= i_min, node_prior_prob_var <= i_max))
                else:
                    self.constraints.append(z3.And(node_prior_prob_var >= 0, node_prior_prob_var <= 1))
            else:
                self.constraints.append(node_prior_prob_var == 1)

            if node.is_initial():
                node_prob = self.z3i.get_node_prob_var(node)
                # self.constraints.append(node_prob == node_prior_prob_var)
                self.constraints.append(node_prob.__eq__(node_prior_prob_var))
                continue

            for parent_assignment in assignments.generate(node.get_parents()):
                parent_prob_var = self.z3i.get_prob_var(parent_assignment)  # e.g. p_nB_C
                prob_var = self.z3i.get_prob_var(parent_assignment + [(node, True)])  # e.g. p_A_nB_C

                product = node_prior_prob_var * parent_prob_var
                for (parent, status) in parent_assignment:
                    if status:
                        edge = node.get_parent_edge(parent)
                        edge_var = self.z3i.get_edge_var(edge)
                        product *= (1 - edge_var)
                # self.constraints.append(prob_var == product)
                self.constraints.append(prob_var.__eq__(product))


class NNorAF(NNor):
    """
    Noisy not-or semantics:  TODO
    with prior probabilities
    p_A_nB_nC = prA * p_nB_nC
    p_A_nB_C  = prA * (1 - t) * p_nB_C
    p_A_B_nC  = prA * (1 - s) * p_B_nC
    p_A_B_C   = prA * (1 - s ) * (1 - t) * p_B_C
    """
    def __init__(self, z3i: zi.Z3Instance):
        super().__init__(z3i, use_prior_probs=True)


class CFs(Semantics):
    """
    Conflict-freeness semantics with attack strengths: p_A_B <= 1-s for all attacks A -s-> B.
    """
    def generate_constraints(self):
        # we use attack strength, so a prob_var should be created for each edge
        self.z3i.generate_edge_vars()

        for edge in self.af.get_edges():
            edge_var = self.z3i.get_edge_var(edge)
            assignment = [(edge.node_from, True), (edge.node_to, True)]
            prob_var = self.z3i.get_prob_var(assignment)
            self.constraints.append(prob_var <= 1 - edge_var)


class StrengthCF(Semantics):
    """
    Alternative conflict-freeness semantics with attack strengths: "P(A,B) <= (1-s)P(A)" for all attacks A -s-> B.
    """
    def generate_constraints(self):
        # we use attack strength, so a prob_var should be created for each edge
        self.z3i.generate_edge_vars()

        for edge in self.af.get_edges():
            edge_var = self.z3i.get_edge_var(edge)
            assignment = [(edge.node_from, True), (edge.node_to, True)]
            prob_var = self.z3i.get_prob_var(assignment)
            node_to_prob = self.z3i.get_node_prob_var(edge.node_to)
            self.constraints.append(prob_var <= (1 - edge_var) * node_to_prob)


########################################
# Strength and Support
########################################

class StrengthSupportCF(Semantics):
    """
    Treats arrows as support with strengths: "P(A,B) >= s * P(A)" for all supports A -s-> B.
    """
    def generate_constraints(self):
        # we use attack strength, so a prob_var should be created for each edge
        self.z3i.generate_edge_vars()

        for edge in self.af.get_edges():
            edge_var = self.z3i.get_edge_var(edge)
            assignment = [(edge.node_from, True), (edge.node_to, True)]
            prob_var = self.z3i.get_prob_var(assignment)
            node_to_prob = self.z3i.get_node_prob_var(edge.node_to)
            # self.constraints.append(prob_var >= edge_var * node_to_prob)
            self.constraints.append(prob_var.__ge__(edge_var * node_to_prob))


########################################
# Dirac versions of classical semantics
########################################

class DiracClassicalSemantics(Semantics):
    """
    Lifts classical semantics into probabilistic semantics by admitting the Dirac-distributions corresponding to the
    classical semantics' extensions.
    E.g., a distribution P is Dirac-admissible if it is a Dirac distribution and P(beta) = 1 for some assignment beta
    implies that the set of arguments holding in beta is an admissible set.

    This is implemented by adding a constraint "P(beta_1) = 1 OR P(beta_2) = 1 OR ... OR P(beta_n) = 1" where beta_i are
    the assignments corresponding to the respective semantics' extensions. Note that this constraint also ensures that
    distributions satisfying it are Dirac distributions, so no additional Dirac constraints are added.
    """
    def __init__(self, classical_semantics: Type[classical.ClassicalSemantics], z3i: zi.Z3Instance):
        self.classical_semantics = classical_semantics
        super().__init__(z3i)

    def generate_constraints(self):
        cs = self.classical_semantics(self.af)
        or_list = []
        for extension in cs.get_extensions():
            assignment = [(node, node in extension) for node in self.af.get_nodes()]
            prob_var = self.z3i.get_prob_var(assignment)
            or_list.append(prob_var == 1)
        self.constraints.append(z3.Or(or_list))


class DiracCF(DiracClassicalSemantics):
    """
    Dirac-conflict-free semantics: Only allows Dirac-distributions corresponding to conflict-free extensions.
    """
    def __init__(self, z3i: zi.Z3Instance):
        super().__init__(classical.CF, z3i)


class DiracAdm(DiracClassicalSemantics):
    """
    Dirac-admissible semantics: Only allows Dirac-distributions corresponding to admissible extensions.
    """
    def __init__(self, z3i: zi.Z3Instance):
        super().__init__(classical.Admissible, z3i)


class DiracCmp(DiracClassicalSemantics):
    """
    Dirac-complete semantics: Only allows Dirac-distributions corresponding to complete extensions.
    """
    def __init__(self, z3i: zi.Z3Instance):
        super().__init__(classical.Complete, z3i)


class DiracGrn(DiracClassicalSemantics):
    """
    Dirac-grounded semantics: Only allows Dirac-distributions corresponding to grounded extensions.
    """
    def __init__(self, z3i: zi.Z3Instance):
        super().__init__(classical.Grounded, z3i)


class DiracPrf(DiracClassicalSemantics):
    """
    Dirac-preferred semantics: Only allows Dirac-distributions corresponding to preferred extensions.
    """
    def __init__(self, z3i: zi.Z3Instance):
        super().__init__(classical.Preferred, z3i)


class DiracSStl(DiracClassicalSemantics):
    """
    Dirac-semi-stable semantics: Only allows Dirac-distributions corresponding to semi-stable extensions.
    """
    def __init__(self, z3i: zi.Z3Instance):
        super().__init__(classical.SemiStable, z3i)


class DiracStl(DiracClassicalSemantics):
    """
    Dirac-stable semantics: Only allows Dirac-distributions corresponding to stable extensions.
    """
    def __init__(self, z3i: zi.Z3Instance):
        super().__init__(classical.Stable, z3i)


###################
# Helper functions
###################

def get_semantics_class_by_name(name: str):
    """
    By dark magic, get the semantics class given its name as string, e.g. "wNor" to yield the class WNor.

    :param name: the name of the semantics (case insensitive)
    :return: The semantics class corresponding to the name
    """
    queue = Semantics.__subclasses__().copy()
    while queue:
        semantics_class = queue.pop()
        if name.lower() == semantics_class.__name__.lower():
            return semantics_class
        queue.extend(semantics_class.__subclasses__())
    return None


def all_semantics_names():
    """
    :return: A list of the names of all semantics declared in this file
    """
    names = []
    # use a queue to recursively also get the names of subclasses
    queue = Semantics.__subclasses__().copy()
    while queue:
        semantics_class = queue.pop()
        queue.extend(semantics_class.__subclasses__())
        names.append(semantics_class.__name__)
    return names
