"""Console script for predex."""
import sys
import getopt

import predex.designMatrix as designMatrix
import predex.annoGenerator as annoGenerator


"""Start called task"""
def main():
    input_arg = sys.argv[1:]
    get_arguments = read_arguments(input_arg)
    
    if (input_arg[0] == "design"):
        if ("".join(sorted(get_arguments.keys())) == "io"):
            designMatrix.main(get_arguments)
        else:
            print("Error: using wrong/missing arguments")
    elif (input_arg[0] == "annotation"):
        if ("".join(sorted(get_arguments.keys())) == "gor"):
            annoGenerator.main(get_arguments)
        else:
            print("Error: using wrong/missing arguments")
    else:
        print("Error: Unkown call:", input_arg[0])
        print(get_arguments)


"""Retrieve all arguments from commandline."""
def read_arguments(input_arg):
    unixOptions = "i:r:g:o:"
    gnuOptions = ["reference=", "gtf=", "input=", "output="]
    dict_args = dict()

    try:
        arguments, values = getopt.getopt(input_arg[1:], unixOptions, gnuOptions)
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
        sys.exit(2)
        
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-i", "--input"):
            dict_args["i"] = currentValue
        elif currentArgument in ("-r", "--reference"):
            dict_args["r"] = currentValue
        elif currentArgument in ("-g", "--gtf"):
            dict_args["g"] = currentValue
        elif currentArgument in ("-o", "--output"):
            dict_args["o"] = currentValue
    return dict_args


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
