#! /usr/local/bin/python37

import sys
import warnings # Required for pybedtools: sequence()
import pybedtools
import pandas as pd


# --------------------------------------------------------------------------
# ----- Read through gtf and call required functions -----


def getGTF(reference, gtf):
    newGene = list()
    gene_seq = list()
    exon_data = list()
    allGeneData = dict()
    reference = pybedtools.BedTool(reference)

    with open(gtf, "r") as openFile:
        for line in openFile:
            line = line.strip().replace('\t', ';').split(";")
            if line[0][0] == "#":
                pass
            elif "gene" in line[2]:
                allGeneData = addNewGene(exon_data, gene_seq, newGene, allGeneData)
                newGene = get_geneInfo(line)
                gene_seq = getSequence(line, reference)
                exon_data = list()
                if len(allGeneData) % 5000 == 0:
                    print("\tProcessed", len(allGeneData), "genes")
            elif "exon" in line[2]:
                exon = [int(line[3])-newGene[3], int(line[4])-newGene[3]]
                exon_data.append(exon)
    allGeneData = addNewGene(exon_data, gene_seq, newGene, allGeneData)
    return allGeneData


# --------------------------------------------------------------------------
# ----- Call functions to gather exon data and merge all gene information -----


def addNewGene(exon_data, gene_seq, newGene, allGeneData):
    if exon_data and gene_seq != "":
        exon_data = checkExonData(exon_data)
        newGene = getExonIntron(newGene, gene_seq, exon_data)
        allGeneData[newGene[0]] = newGene
    return allGeneData


# --------------------------------------------------------------------------
# ----- Create correct exon location without any overlap -----


def checkExonData(exon_data):
    exon_data = sorted(exon_data)
    correct = [exon_data[0]]
    for location in exon_data:
        if correct[-1][0] <= location[0] <= correct[-1][1] <= location[1]:
            correct[-1][1] = location[1]
        elif location[0] >= correct[-1][0] and location[1] <= correct[-1][1]:
            pass
        else:
            correct.append(location)
    return correct


# --------------------------------------------------------------------------
# ----- Get gene data from gtf -----


def get_geneInfo(line):
    try:
        geneSymbol = str(''.join([s for s in line if "gene_name" in s]).split()[-1].strip('"'))
    except IndexError as err:
        geneSymbol = str(''.join([s for s in line if "gene_id" in s]).split()[-1].strip('"'))
        print("\t geneName unavailable for", geneSymbol + ", will use geneID instead")        
    newGene = [str(''.join([s for s in line if "gene_id" in s]).split()[-1].strip('"')),  # GeneID
               str(geneSymbol),  # GeneSymbol
               str(line[0]),  # Contig
               int(line[3]),  # StartPos
               int(line[4]),  # EndPos
               int(line[4]) - int(line[3]) + 1,  # Length
               str(line[6]),  # GeneStrand
               str(''.join([s for s in line if "gene_biotype" in s]).split()[-1].strip('"'))]  # GeneType
    return newGene


# --------------------------------------------------------------------------
# ----- Get gene sequence -----


def getSequence(line, reference):
    contig = str(line[0])
    start = line[3]
    end = line[4]
    if start != end:
        bed = pybedtools.BedTool(' '.join([contig, str(start), str(end)]), from_string=True)
        try:
            warnings.simplefilter("ignore")
            bed = bed.sequence(fi=reference)
            with open(bed.seqfn, "r") as openFile:
                bed = openFile.readlines()[1].strip()
        except IndexError:
            bed = ""
    else:
        bed = ""
    return bed


# --------------------------------------------------------------------------
# ----- Get exon/intron data and add to gene data -----


def getExonIntron(newGene, gene_seq, exon_data):
    exon_seq = ""
    intron_seq = gene_seq
    for exon in exon_data:
        exon_seq += gene_seq[exon[0]:exon[1]]
        intron_seq = intron_seq[:exon[0]] + len(intron_seq[exon[0]:exon[1]])*"0" + intron_seq[exon[1]:]
    intron_seq = intron_seq.replace("0", "")

    exonlength = len(exon_seq)
    geneGC = getGCcontent(gene_seq)
    exonGC = getGCcontent(exon_seq)
    intronGC = getGCcontent(intron_seq)
    newGene.extend([geneGC, exonGC, intronGC, exonlength])
    return newGene


# --------------------------------------------------------------------------
# ----- Calculate GC content -----


def getGCcontent(sequence):
    if len(sequence) == 0:
        gc = 0
    else:
        gc = round(sum(map(sequence.count, ["G", "C"])) / len(sequence), 6)
    return gc


# --------------------------------------------------------------------------
# ----- Set column names and save dataframe as TSV -----


def saveDataframe(df, outputDir):
    df.columns = ["feature", "geneName", "chromosome", "startPos", "endPos",
                  "geneLength", "geneStrand", "geneType", "geneGC", "exonGC",
                  "intronGC", "exonLength"]
    df = df[["feature", "geneName", "chromosome", "startPos", "endPos",
             "geneStrand", "geneLength", "exonLength", "geneGC", "exonGC",
             "intronGC", "geneType"]]
    df[["startPos", "endPos", "geneLength", "exonLength"]] = df[
        ["startPos", "endPos", "geneLength", "exonLength"]].astype('Int64')
    df = df.sort_values("feature")
    df.to_csv(outputDir + "/annotation.tsv", sep="\t", index=False)


# --------------------------------------------------------------------------
# ----- Start script and get arguments -----

def main(args):
    print("Running...")
    reference = args.fasta
    gtf = args.gtf
    outputDir = args.output

    allGeneData = getGTF(reference, gtf)
    print("Saving data...")
    df = pd.DataFrame.from_dict(allGeneData, orient="index")
    df.columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    saveDataframe(df, outputDir)

    print("Done!")


if __name__ == "__main__":
    main()
