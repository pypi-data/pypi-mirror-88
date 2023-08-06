#! /usr/bin/env python3
import sys
import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="Prints list of commands and short commands with descriptions.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )
    return parser

def main(argv=None):

    """
    :desc: Print command line arguments for uniaxially strained graphene and use with QMC software located at https://code.delmaestro.org
    """
    if argv is None:
        argv = sys.argv

    parser = create_parser()
    args = parser.parse_args(argv[1:])

    print("")
    print("Graphene Tools Commands:")
    print("    gt_roughly_square: Print command line arguments for uniaxially strained graphene and use with QMC software located at https://code.delmaestro.org")
    print("    gt_roughly_square_plot: Plot graphene lattice and C1/3 phase corresponding to printed command line arguments for uniaxially strained graphene (for use with QMC software located at https://code.delmaestro.org)")
    print("    gt_c_one_third_commensurate_command: Print command line arguments for uniaxially strained graphene and use with QMC software located at https://code.delmaestro.org")
    print("    gt_c_one_third_commensurate_command_plot: Plot graphene lattice and C1/3 phase corresponding to printed command line arguments for uniaxially strained graphene (for use with QMC software located at https://code.delmaestro.org)")
    print("")
    print("Graphene Tools Commands (short names):")
    print("    gt_rs: Short command to `gt_roughly_square`")
    print("    gt_rsp: Short command to `gt_roughly_square_plot`")
    print("    gt_cotcc: Short command to `gt_c_one_third_commensurate_command`")
    print("    gt_cotccp: Short command to `gt_c_one_third_commensurate_command_plot`")

    return 0



if __name__ == '__main__':
    sys.exit(main(sys.argv))

