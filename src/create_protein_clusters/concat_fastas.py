import warnings
from pathlib import Path

from Bio import BiopythonWarning
from tqdm import tqdm

warnings.simplefilter("ignore", BiopythonWarning)

project_dir = Path(__file__).resolve().parents[2]
refined_pdbids = []
other_pdbids = []
refined_dir = Path(project_dir) / "../ba_pred/data/raw/refined-set"
other_dir = Path(project_dir) / "../ba_pred/data/raw/v2020-other-PL"


def get_pdbids():
    pdbid_list_path = project_dir / "data" / "PDBbind_v2020_pdbids.txt"
    with open(str(pdbid_list_path), "r") as f:
        pdbids = f.read().splitlines()
    return pdbids


def get_pocket_fasta(pdbid):
    with open(project_dir / "data" / "fastas" / f"{pdbid}.fasta", "r") as f:
        fasta_txt = f.read()
    fasta_lines = fasta_txt.splitlines()

    records = []
    for i in range(0, len(fasta_lines), 2):
        record = {}
        record["name"] = fasta_lines[i][1:]
        record["sequence"] = fasta_lines[i + 1]
        records.append(record)

    output = f">{pdbid}\n"
    for record in records:
        output += record["sequence"]
    output += "\n"
    return output


def main():
    global refined_pdbids, other_pdbids
    pdbids = get_pdbids()

    refined_pdbids = refined_dir.glob("*")
    refined_pdbids = [p.stem for p in refined_pdbids if len(p.stem) == 4]
    other_pdbids = other_dir.glob("*")
    other_pdbids = [p.stem for p in other_pdbids if len(p.stem) == 4]

    fastas = ""
    bar = tqdm(pdbids)
    for pdbid in pdbids:
        fasta = get_pocket_fasta(pdbid)
        fastas += fasta
        bar.update(1)

    with open(project_dir / "data" / "all.fasta", "w") as f:
        f.write(fastas)


if __name__ == "__main__":
    main()
