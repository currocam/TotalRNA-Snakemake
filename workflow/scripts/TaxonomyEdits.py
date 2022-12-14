"Add taxonomic prefix to mapped reads to contigs."
import sys
from typing import List
import argparse
PVC_POSITION = 1

def get_taxonomy_list(x: List[str]) -> List[str]:
    """
    Get taxonomy column and split it into a list of values. 
    >>> cols = ['RandomId', '1347', '253', '339', 'Main genome;Bacteria;Bacteria (superkingdom);PVC group (Planctobacteria);Planctomycetes;Phycisphaerae;Tepidisphaerales;Tepidisphaeraceae']
    >>> get_taxonomy_list(cols)
    ['Bacteria', 'PVC group (Planctobacteria)', 'Planctomycetes', 'Phycisphaerae', 'Tepidisphaerales', 'Tepidisphaeraceae']
    """
    taxonomy= x[-1] \
    .replace(" (superkingdom)","") \
    .replace(" (superphylum)","") \
    .split(";")
    return taxonomy[2:]

def add_prefix_taxonomy(x: List[str]) -> List[str]:
    """
    Add prefix to different taxonomic categories. 
    >>> add_prefix_taxonomy([])
    ['k__', 't__', 'p__', 'c__', 'o__', 'f__', 'g__', 's__']
    >>> add_prefix_taxonomy(['Bacteria', 'PVC group (Planctobacteria)', 'Planctomycetes', 'Phycisphaerae', 'Tepidisphaerales', 'Tepidisphaeraceae'])
    ['k__Bacteria', 't__PVC group (Planctobacteria)', 'p__Planctomycetes', 'c__Phycisphaerae', 'o__Tepidisphaerales', 'f__Tepidisphaeraceae', 'g__', 's__']
    """
    y = ["k__","t__", "p__","c__","o__","f__","g__","s__"] 
    if len(x) > len(y):
        print("Warning: taxonomy column is longer than expected", file=sys.stderr)
        print(x, file=sys.stderr)
    for i, v in enumerate(x):
        y[i] += v
    return y

def edit_line(line: str) -> str:
    cols = [col.strip() for col in line.strip().split("\t")]
    taxonomy = add_prefix_taxonomy(get_taxonomy_list(cols   ))
    taxonomy.pop(PVC_POSITION)
    cols[-1] = "; ".join(taxonomy)
    return "\t".join(cols)

def create_argument_parser() -> argparse.ArgumentParser:
    argparser = argparse.ArgumentParser(description="Add taxonomic prefix to mapped reads to contigs.")
    # 'infile' is either provided as an input file name or stdin
    argparser.add_argument(
        "infile",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
    )
    # 'outfile' is either provided as a file name or we use stdout
    argparser.add_argument(
        "outfile",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )
    return argparser

def main() -> None: 
    argparser = create_argument_parser()
    args = argparser.parse_args()
    args.outfile.write(
        next(args.infile).replace("classification", "taxonomy")+'\n'
        )
    for line in args.infile:
        args.outfile.write(edit_line(line)+'\n')
    print("Everything runs smoothly", file=sys.stderr)

if __name__ == "__main__":
    main()