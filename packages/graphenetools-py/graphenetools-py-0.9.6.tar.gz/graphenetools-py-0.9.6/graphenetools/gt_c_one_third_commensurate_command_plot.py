#! /usr/bin/env python3
import sys
import argparse
from graphenetools import gt

def create_parser():
    parser = argparse.ArgumentParser(description="Plot graphene lattice and C1/3 phase corresponding to printed command line arguments for uniaxially strained graphene (for use with QMC software located at https://code.delmaestro.org)",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )
    parser.add_argument("m", type=int,
                        help="Simulation cell parameter to generate `2*m*n` C1/3 adsorption sites")
    parser.add_argument("n", type=int,
                        help="Simulation cell parameter to generate `2*m*n` C1/3 adsorption sites")
    parser.add_argument("--strain", type=float, default=0.0,
                        help="Value of strain in armchair direction")
    parser.add_argument("--carbon_carbon_distance", type=float, default=1.42,
                        help="Distance in angstrom between adjacent carbon atoms in isotropic graphene")
    parser.add_argument("--poisson_ratio", type=float, default=0.165,
                        help="Poisson's ratio, (the ratio of transverse contraction strain to longitudinal extension strain in the direction of the stretching force) for graphene")
    parser.add_argument('--mplstylefile', type=str, default="default",
                        help='Location of stylefile to use with plotting')
    parser.add_argument("--dpi", type=float, default=None,
                        help="DPI of saved plot. Defaults to `rcParams[\"savefig.dpi\"]`")
    parser.add_argument("--savefig", type=str, default="",
                        help="Location to save plot. Image type based on extension. Will not save if empty.")
    return parser

def main(argv=None):

    """
    :desc: Print command line arguments for uniaxially strained graphene and use with QMC software located at https://code.delmaestro.org
    """
    if argv is None:
        argv = sys.argv

    parser = create_parser()
    args = parser.parse_args(argv[1:])

    gt.c_one_third_commensurate_command(args.m,args.n,args.strain,carbon_carbon_distance=args.carbon_carbon_distance, poisson_ratio=args.poisson_ratio)
    fig,ax = gt.c_one_third_commensurate_command_plot(args.m,args.n,args.strain,carbon_carbon_distance=args.carbon_carbon_distance, poisson_ratio=args.poisson_ratio)
    if args.savefig:
        with gt.plt.style.context(args.mplstylefile):
            fig.savefig(args.savefig,dpi=args.dpi)
    fig.show()

    return 0



if __name__ == '__main__':
    sys.exit(main(sys.argv))

