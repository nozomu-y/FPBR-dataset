import json
import pickle
from functools import cache
from pathlib import Path

import numpy as np
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
from tqdm import tqdm

project_dir = Path(__file__).resolve().parents[2]


def get_pdbids():
    pdbid_list_path = project_dir / "data" / "PDBbind_v2020_pdbids.txt"
    with open(str(pdbid_list_path), "r") as f:
        pdbids = f.read().splitlines()
    return pdbids


def get_smiles(pdbid):
    entry_info_path = project_dir / "data" / "entry_information" / f"{pdbid}.json"
    with open(str(entry_info_path), "r") as f:
        entry_info = json.load(f)
    return entry_info["Canonical SMILES"]


@cache
def calculate_fingerprints(smiles):
    mol = Chem.MolFromSmiles(smiles)
    try:
        morgan_fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
    except:
        morgan_fp = None
    return morgan_fp


def main():
    pdbids = get_pdbids()

    fingerprints = []
    fingerprint_pdbids = []
    bar = tqdm(pdbids)
    for pdbid in pdbids:
        fp = calculate_fingerprints(get_smiles(pdbid))
        if fp is None:
            continue
        fingerprints.append(fp)
        fingerprint_pdbids.append(pdbid)
        bar.update(1)

    dist_matrix = []
    bar = tqdm(fingerprints)
    for fp in fingerprints:
        dist_matrix.append(DataStructs.BulkTanimotoSimilarity(fp, fingerprints))
        bar.update(1)

    dist_matrix = np.array(dist_matrix)
    dist_matrix = 1 - dist_matrix
    print(dist_matrix)
    with open(project_dir / "data" / "distance_matrix.pkl", "wb") as f:
        pickle.dump((fingerprint_pdbids, dist_matrix), f)


if __name__ == "__main__":
    main()
