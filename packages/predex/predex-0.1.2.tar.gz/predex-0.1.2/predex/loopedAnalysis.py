
import pandas as pd
import itertools


# Load input and call functions
def main():
    designPath = ""
    compare = "Groups"

    designFile = pd.read_csv(designPath, index_col=1)
    unique = list(set(designFile[compare]))

    with open("designs.R", "w") as myfile:
        myfile.write("designs <- list(\n")

    for item in range(len(unique)-1):
        unique = combinations(unique, designPath)
    write_to_file()


# Make possible combinations and write temp. data to file
def combinations(unique, designPath):    
    value = unique[0]
    del unique[0]        
    matrixList = list(itertools.product([value], unique))
    for design in matrixList:
        with open("designs.R", "a") as myfile:
            myfile.write('\tlist(\n\t\tdesign = "' + designPath +
                '",\n\t\tmatrix_v1 = "' + design[0] +
                '",\n\t\tmatrix_v2 = "' + design[1] +
                '",\n\t\tname = "' + design[0] + 'vs' + design[1] + '"\n\t),\n')
    return unique


# Write final data to file
def write_to_file():    
    with open("designs.R", 'r') as myfile:
        lines = myfile.readlines()
        lines = lines[:-1]
    with open("designs.txt", "w") as myfile:
        myfile.writelines(lines)
        myfile.write("\t)\n)")


if __name__ == "__main__":
    main()
