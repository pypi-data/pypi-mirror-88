from svpy.cfa import *
from svpy.cpa.value import *
from svpy.cpa.unreachablecall import *
from svpy.cpa.algorithm import CPAAlgorithm
from svpy.cpa.arg import *
from svpy.cpa.composite import *
from svpy.cpa.location import *
from svpy.visualization import *

import argparse
import astpretty
import os

parser = argparse.ArgumentParser(description="svpy, software verification in python.")
parser.add_argument(
    "--program", metavar="PROG", type=str, help="the program to be verified"
)
args = parser.parse_args()


def main(program):
    # parsing program into an AST:
    tree = ast.parse(program)
    with open("output/ast.txt", "w") as f:
        f.write(astpretty.pformat(tree, show_offsets=False))

    # creating a CFA from the AST:
    cfaCreator = CFACreator()
    cfaCreator.visit(tree)
    cfaRoot = cfaCreator.root
    dot = graphableToDot(GraphableCFANode(cfaRoot))
    dot.save(filename="output/cfa.dot")

    # creating a CPA and executing the CPA algorithm:
    cpa = ARGCPA(
        CompositeCPA(
            [
                LocationCPA(cfaRoot),
                ValueAnalysisCPA(),
                UnreachableCallCPA("reach_error"),
            ]
        )
    )
    waitlist = set()
    reached = set()
    init = cpa.get_initial_state()
    waitlist.add(init)
    reached.add(init)
    algo = CPAAlgorithm(cpa)
    algo.run(reached, waitlist)

    if any([hasattr(state, "is_target") and state.is_target() for state in reached]):
        print("TARGET REACHED")

    # save ARG visualization:
    dot = graphableToDot(
        GraphableARGState(init),
        nodeattrs={"style": "filled", "shape": "box", "color": "white"},
    )
    dot.save(filename="output/arg.dot")


if args.program is None and os.path.isfile(
    os.path.dirname(os.path.realpath(__file__)) + "/testprograms/source.py"
):
    args.program = (
        os.path.dirname(os.path.realpath(__file__)) + "/testprograms/source.py"
    )
if args.program is None:
    print("No program provided!")
main(open(args.program, "r").read())
