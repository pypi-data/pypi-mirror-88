import argparse

import af_parser
import labeling_scheme as lab
import semantics as sem
import tasks
import z3_instance
from timer import Timer

# TODO:
#  - Flag for extensions
#  - flag to generate unsat core; this needs named assertions, see assert_and_track() in z3.py
#  - check why seemingly the same labeling still can appear multiple times for AL
#  - af_constraints in z3i overlaps with AF semantics
#  - credulous and skeptical acceptance wrt. a labeling scheme


def main():
    main_timer = Timer(output_string="Overall runtime:")

    #########################
    # set up argument parser
    #########################
    arg_parser = argparse.ArgumentParser(description="CPrAA - a Checker for Probabilistic Abstract Argumentation ",
                                         add_help=False)
    base_group = arg_parser.add_argument_group("basic parameters")
    base_group.add_argument("-f", "--file", help="the argumentation framework as .tgf file")
    base_group.add_argument("-s", "--semantics", nargs="+", default=[],
                            help="the probabilistic semantics to check against")
    base_group.add_argument("-OD", "--one_distribution", action="store_true",
                            help="compute one distribution satisfying the semantics")
    base_group.add_argument("-i", "--assume_independence", action="store_true",
                            help="treat the argument's probabilities as independent (warning: this leads to incorrect "
                                 "results for some semantics)")

    ac_group = arg_parser.add_argument_group("acceptance checking")
    ac_group.add_argument("-a", "--argument", help="the argument from the AF to be checked")
    ac_group.add_argument("-CA", "--credulous_acceptance",
                          nargs="?", metavar="THRESHOLD", type=float, const=1.0,
                          help="check credulous acceptance of given argument, "
                               "optionally taking a threshold into account")
    ac_group.add_argument("-SA", "--skeptical_acceptance",
                          nargs="?", metavar="THRESHOLD", type=float, const=1.0,
                          help="check skeptical acceptance of given argument, "
                               "optionally taking a threshold into account")
    ac_group.add_argument("-CAA", "--credulous_acceptance_all",
                          nargs="?", metavar="THRESHOLD", type=float, const=1.0,
                          help="check credulous acceptance of all arguments, "
                               "optionally taking a threshold into account")
    ac_group.add_argument("-SAA", "--skeptical_acceptance_all",
                          nargs="?", metavar="THRESHOLD", type=float, const=1.0,
                          help="check skeptical acceptance of all arguments, "
                               "optionally taking a threshold into account")

    lab_group = arg_parser.add_argument_group("generate labelings")
    lab_group.add_argument("-l", "--labeling_scheme", metavar="SCHEME", help="the labeling scheme to use")
    lab_group.add_argument("-OL", "--one_labeling", action="store_true",
                           help="compute one labeling satisfying the semantics")
    lab_group.add_argument("-AL", "--all_labelings", action="store_true",
                           help="compute all labelings satisfying the semantics")
    lab_group.add_argument("-lt", "--labeling_threshold", nargs="+", metavar="T", type=float,
                           help="the optional thresholds needed for some labeling schemes")

    info_group = arg_parser.add_argument_group('informational parameters')
    info_group.add_argument("-h", "--help", action="help", help="show this help message")
    info_group.add_argument("-ls", "--list_semantics", action="store_true",
                            help="list all available probabilistic semantics")
    info_group.add_argument("-ll", "--list_labeling_schemes", action="store_true",
                            help="list all available labeling schemes")
    info_group.add_argument("-d", "--documentation", nargs="+", default=[], metavar="NAME",
                            help="display a short documentation for the listed semantics or labeling schemes")
    info_group.add_argument("-t", "--time", action="store_true", help="time the execution")
    info_group.add_argument("-o", "--distribution_output_format", metavar="FORMAT", type=str, default="M",
                            help="how to output distributions: (M) marginal node probabilities, (F) full distribution, "
                                 "(S) support of distribution, (Z) Z3 output, (T) SMT2 format.")

    ##################
    # parse arguments
    ##################
    args = arg_parser.parse_args()

    af = None
    z3i = None
    labeling_scheme = None
    semantics = []
    argument = None

    main_timer.enable_printing = args.time
    Timer.enable_printing_default = args.time

    if args.list_semantics:
        print("Available semantics:", ", ".join(sem.all_semantics_names()))

    if args.list_labeling_schemes:
        print("Available labeling schemes:", ", ".join(lab.get_all_labeling_scheme_names()))

    if args.documentation:
        for name in args.documentation:
            semantics_class = sem.get_semantics_class_by_name(name)
            if semantics_class:
                print("Semantics '" + semantics_class.__name__ + "':")
                if semantics_class.__doc__:
                    print(semantics_class.__doc__.strip("\n"))
                else:
                    print("    No documentation available.")
            else:
                labeling_scheme_class = lab.get_labeling_scheme_class(name)
                if labeling_scheme_class:
                    print("Labeling scheme '" + labeling_scheme_class.__name__ + "':")
                    if labeling_scheme_class.__doc__:
                        print(labeling_scheme_class.__doc__.strip("\n"))
                    else:
                        print("    No documentation available.")
                else:
                    arg_parser.error("no semantics or labeling scheme called '" + name + "' exists")

    if args.file:
        af = af_parser.parse_tgf(args.file)
        af.print()
        z3i_setup_timer = Timer(output_string="z3i setup took")
        z3i = z3_instance.Z3Instance(af, args.assume_independence)
        z3i_setup_timer.stop()

    if args.semantics:
        if not af:
            arg_parser.error("an AF must be provided when checking semantics")

        semantics_constraints_timer = Timer(output_string="Generating constraints for all semantics took")
        for semantics_name in args.semantics:
            semantics_class = sem.get_semantics_class_by_name(semantics_name)
            if not semantics_class:
                arg_parser.error("No semantics called '"
                                 + semantics_name + "' exists. Use -ls to list all available semantics.")
            semantics.append(semantics_class(z3i))

        semantics_constraints_timer.stop()

    if args.labeling_scheme:
        labeling_scheme_class = lab.get_labeling_scheme_class(args.labeling_scheme)
        if not labeling_scheme_class:
            arg_parser.error("no labeling scheme called '" + args.labeling_scheme + "' exists")
        num_args_required = labeling_scheme_class.num_args
        if args.labeling_threshold:
            num_args_given = len(args.labeling_threshold)
        else:
            num_args_given = 0
        if num_args_given < num_args_required:
            error_message = "mismatch in the number of thresholds: required by labeling scheme '" \
                            + args.labeling_scheme + "': " + str(num_args_required) + ", given: " + str(num_args_given)
            arg_parser.error(error_message)
        if num_args_given > num_args_required:
            warning_message = "warning: mismatch in the number of thresholds: required by labeling scheme '" \
                              + args.labeling_scheme + "': " + str(num_args_required) + ", given: " \
                              + str(num_args_given) + " - i'm ignoring the surplus ones"
            print(warning_message)
        if num_args_required == 0:
            labeling_scheme = labeling_scheme_class()
        elif num_args_required == 1:
            labeling_scheme = labeling_scheme_class(args.labeling_threshold[0])
        elif num_args_required == 2:
            labeling_scheme = labeling_scheme_class(args.labeling_threshold[0], args.labeling_threshold[1])
        else:
            raise NotImplementedError("labeling schemes with more than 2 thresholds")

    if args.argument:
        if not af:
            arg_parser.error("an AF must be provided when checking acceptance")
        argument = af.get_node_by_name(args.argument)

    ########
    # tasks
    ########

    if args.one_distribution:
        if not af:
            arg_parser.error("an AF must be provided to compute a distribution")

        od_timer = Timer(output_string="Computing one distribution took")
        print("Computing one distribution satisfying the following semantics:",
              ", ".join(args.semantics))
        model = tasks.get_model(z3i, semantics)
        if model:
            z3i.print_formatted_distribution(model, args.distribution_output_format)
            # z3_instance.print_model(af, model)
        else:
            print("No distribution satisfying the given semantics exists.")
        od_timer.stop()

    if args.one_labeling:
        if not af:
            arg_parser.error("an AF must be provided to compute a labeling")
        if not labeling_scheme:
            arg_parser.error("no labeling provided")

        ol_timer = Timer(output_string="Computing one labeling took")
        print("Computing one", args.labeling_scheme, "labeling satisfying the following semantics:",
              ", ".join(args.semantics))
        labeling = tasks.get_satisfying_labeling(z3i, labeling_scheme, semantics)
        print(labeling)
        ol_timer.stop()

    if args.all_labelings:
        if not af:
            arg_parser.error("an AF must be provided to compute a labeling")
        if not labeling_scheme:
            arg_parser.error("no labeling provided")

        al_timer = Timer(output_string="Computing all labelings took")
        print("Computing all", args.labeling_scheme, "labelings satisfying the following semantics:",
              ", ".join(args.semantics))
        labelings = tasks.get_all_satisfying_labelings(z3i, labeling_scheme, semantics)
        print("Number of labelings:", len(labelings))
        # for ext in sorted([labeling.labeled_in for labeling in labelings]):
        #     print(ext)
        # for labeling in labelings:
        #     print(labeling)
        #     # print(labeling.model)
        #     # z3i.print_distribution(labeling.model, only_positive=True)
        #     # z3_instance.print_model(af, labeling.model)
        for labeling in sorted(list(set(map(repr, labelings)))):
            print(labeling)
        al_timer.stop()

    if args.credulous_acceptance is not None:
        if not af:
            arg_parser.error("an AF must be provided to check acceptance")
        if not argument:
            arg_parser.error("argument to be checked is missing")

        threshold = args.credulous_acceptance

        ca_timer = Timer(output_string="Checking credulous acceptance took")
        print("Checking credulous acceptance of argument", args.argument, "with threshold", threshold,
              "under the following semantics:", ", ".join(args.semantics))
        (acceptable, model) = tasks.check_credulous_threshold_acceptance(z3i, semantics, threshold, argument)
        if acceptable:
            print(args.argument, "is credulously accepted.")
            print("Satisfying distribution:")
            z3i.print_formatted_distribution(model, args.distribution_output_format)
            # z3i.print_distribution(model, only_positive=True)
            # z3_instance.print_model(af, model)
        else:
            print(args.argument, "is not credulously accepted.")
        ca_timer.stop()

    if args.skeptical_acceptance is not None:
        if not af:
            arg_parser.error("an AF must be provided to check acceptance")
        if not argument:
            arg_parser.error("argument to be checked is missing")

        threshold = args.skeptical_acceptance

        sa_timer = Timer(output_string="Checking skeptical acceptance took")
        print("Checking skeptical acceptance of argument", args.argument, "with threshold", threshold,
              "under the following semantics:", ", ".join(args.semantics))
        (acceptable, counterexample) = tasks.check_skeptical_threshold_acceptance(z3i, semantics, threshold, argument)
        if acceptable:
            print(args.argument, "is skeptically accepted.")
        else:
            print(args.argument, "is not skeptically accepted.")
            print("Counterexample:")
            z3i.print_formatted_distribution(counterexample, args.distribution_output_format)
            # z3i.print_distribution(counterexample, only_positive=True)
            # z3_instance.print_model(af, counterexample)
        sa_timer.stop()

    if args.credulous_acceptance_all is not None:
        if not af:
            arg_parser.error("an AF must be provided to check acceptance")

        threshold = args.credulous_acceptance_all

        ca_timer = Timer(output_string="Checking credulous acceptance for all arguments took")
        print("Checking credulous acceptance of all arguments with threshold", threshold,
              "under the following semantics:", ", ".join(args.semantics))
        accepted_args = []
        not_accepted_args = []
        for argument in af.get_nodes():
            (acceptable, model) = tasks.check_credulous_threshold_acceptance(z3i, semantics, threshold, argument)
            if acceptable:
                accepted_args.append(argument)
                # print(argument.name, "is credulously accepted.")
                # print("Satisfying distribution:")
                # z3i.print_distribution(model, only_positive=True)
                # z3_instance.print_model(af, model)
            else:
                not_accepted_args.append(argument)
                # print(argument.name, "is not credulously accepted.")
        print("Credulously accepted:", accepted_args)
        print("Not credulously accepted:", not_accepted_args)
        ca_timer.stop()

    if args.skeptical_acceptance_all is not None:
        if not af:
            arg_parser.error("an AF must be provided to check acceptance")

        threshold = args.skeptical_acceptance_all

        ca_timer = Timer(output_string="Checking skeptical acceptance for all arguments took")
        print("Checking skeptical acceptance of all arguments with threshold", threshold,
              "under the following semantics:", ", ".join(args.semantics))
        accepted_args = []
        not_accepted_args = []
        for argument in af.get_nodes():
            acceptable, counterexample = tasks.check_skeptical_threshold_acceptance(z3i, semantics, threshold, argument)
            if acceptable:
                accepted_args.append(argument)
                # print(argument.name, "is skeptically accepted.")
            else:
                not_accepted_args.append(argument)
                # print(argument.name, "is not skeptically accepted.")
                # print("Counterexample:", counterexample)
                # z3i.print_distribution(counterexample, only_positive=True)
                # z3_instance.print_model(af, counterexample)
        print("Skeptically accepted:", accepted_args)
        print("Not skeptically accepted:", not_accepted_args)
        ca_timer.stop()

    main_timer.stop()

    # CSV friendly print of timing results
    # semantics_names = ",".join([semantics_obj.__class__.__name__ for semantics_obj in semantics])
    # timings = ";".join([str(timer.last_timing) for timer in Timer.all_timers])
    # # print(semantics_names + ";" + timings)
    # print(af.name + ";" + timings)


main()


# ---------------------------------------------------------

def test_all_semantics():
    # path = "AFs/af01.tgf"
    path = "AFs/af_references_noisy.tgf"
    af = af_parser.parse_tgf(path)
    z3i = z3_instance.Z3Instance(af)

    for semantics_class in tasks.Semantics.__subclasses__():
        try:
            semantics = semantics_class(z3i)
            print(semantics_class.__name__, semantics.constraints)
        except NotImplementedError:
            print(semantics_class.__name__, "(not implemented)")


# test_all_semantics()
