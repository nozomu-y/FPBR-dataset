from pathlib import Path
from time import sleep

import requests
from tqdm import tqdm

project_dir = Path(__file__).resolve().parents[2]


def get_pdbids():
    pdbid_list_path = project_dir / "data" / "PDBbind_v2020_pdbids.txt"
    with open(str(pdbid_list_path), "r") as f:
        pdbids = f.read().splitlines()
    return pdbids


def download_fasta(pdbid, download_dir):
    save_path = download_dir / f"{pdbid}.fasta"

    url = f"http://www.pdbbind.org.cn/FASTA/{pdbid}.txt"
    if pdbid == '5ab1':
        url = "https://www.rcsb.org/fasta/entry/6YHW"

    try:
        r = requests.get(url, timeout=10)
        print(r.text)
        with open(str(save_path), "w") as f:
            f.write(r.text)
    except:
        print(f"Failed to download {pdbid}.fasta")
        pass


def main():
    pdbids = get_pdbids()
    download_dir = project_dir / "data" / "fastas"
    downloaded_pdbids = [p.stem for p in download_dir.glob("*.fasta")]
    pdbids = [pdbid for pdbid in pdbids if pdbid not in downloaded_pdbids]

    bar = tqdm(pdbids, mininterval=0.1)
    for pdbid in pdbids:
        download_fasta(pdbid, download_dir)
        bar.update(1)
        sleep(60)


if __name__ == "__main__":
    main()
