"""Console script for predex."""
import sys
import argparse

import predex.designMatrix as designMatrix
import predex.annoGenerator as annoGenerator


"""Start called task"""
def main():
    check_args()


def check_args():
    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
    parser = argparse.ArgumentParser(description = "Prepare data for expression analysis with e.g. dgeAnalysis - LUMC.")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.1")

    subparser = parser.add_subparsers()

    # design argument
    a_parser = subparser.add_parser("design", help="Create design matrix template", formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
    a_parser.set_defaults(func=designMatrix.main)
    required = a_parser.add_argument_group('required arguments')
    required.add_argument("-i", "--input", help="Input files (count matrix, e.g., HTSeq)", required=True)
    required.add_argument("-o", "--output", help="Output directory", required=True)

    # annotation argument
    b_parser = subparser.add_parser("annotation", help="Create annotation file", formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
    b_parser.set_defaults(func=annoGenerator.main)
    required = b_parser.add_argument_group('required arguments')
    required.add_argument("-f", "--fasta", help="Fasta file input", required=True)
    required.add_argument("-g", "--gtf", help="GTF file input", required=True)
    required.add_argument("-o", "--output", help="Output directory", required=True)
    
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":    
    main()
