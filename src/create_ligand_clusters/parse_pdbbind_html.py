import json
from pathlib import Path

from bs4 import BeautifulSoup
from tqdm import tqdm

project_dir = Path(__file__).resolve().parents[2]


def get_entry_info(pdbid):
    source_path = project_dir / "data" / "sources" / f"{pdbid}.html"
    if not source_path.exists():
        print(f"{pdbid} not found")
        return

    with open(str(source_path), "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    entry_info_soup = soup.select_one(
        "body > table > tbody > tr:nth-child(6) > td > table:nth-child(1) > tbody > tr:nth-child(2) > td:nth-child(3) > fieldset:nth-child(1) > table"
    )
    rows = entry_info_soup.find_all("tr")

    entry_info = {}
    for row in rows:
        key = row.select_one("td:nth-child(1)").text
        if key == "Ligand Properties":
            continue
        value = row.select_one("td:nth-child(2)")
        if key == "PDB ID":
            entry_info[key] = value.text.strip()
            entry_info["link"] = value.find("a")["href"]
            continue
        if key == "EC.Number":
            entry_info[key] = value.text.strip()
            # entry_info["EC.Number link"] = value.find("a")["href"]
            continue
        if key == "Protein/NA Sequence":
            entry_info[f"{key} link"] = (
                "http://www.pdbbind.org.cn/" + value.find("a")["href"]
            )
            continue
        if key == "Primary Reference":
            entry_info[f"{key} name"] = value.text
            try:
                entry_info[f"{key} link"] = value.find("a")["href"]
            except:
                pass
            continue
        if key == "LOGP Value":
            continue
        if key == "Drug likeness":
            continue
        entry_info[key] = value.text.strip()

    with open(
        str(project_dir / "data" / "entry_information" / f"{pdbid}.json"), "w"
    ) as f:
        json.dump(entry_info, f, indent=4, ensure_ascii=False)


def get_pdbids():
    pdbid_list_path = project_dir / "data" / "PDBbind_v2020_pdbids.txt"
    with open(str(pdbid_list_path), "r") as f:
        pdbids = f.read().splitlines()
    return pdbids


def main():
    pdbids = get_pdbids()

    bar = tqdm(pdbids)
    for pdbid in pdbids:
        get_entry_info(pdbid)
        bar.update(1)


if __name__ == "__main__":
    main()
