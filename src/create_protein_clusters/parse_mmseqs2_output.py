from pathlib import Path

import pandas as pd

project_dir = Path(__file__).resolve().parents[2]


def main():
    df = pd.read_table(
        str(project_dir / "data" / "mmseqs2" / "clustered.tsv"), header=None
    )
    df = df.set_axis(["cluster_id", "pdbid"], axis=1)
    df["cluster_id"] = df.groupby("cluster_id").ngroup()
    df = df.sort_values(["cluster_id", "pdbid"])
    df.to_csv(str(project_dir / "data" / "protein_cluster.csv"), index=False)


if __name__ == "__main__":
    main()
