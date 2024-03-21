from pathlib import Path

import numpy as np
import pandas as pd

project_dir = Path(__file__).resolve().parents[2]

np.random.seed(seed=0)


def main():
    ligand_cluster_df = pd.read_csv(str(project_dir / "data" / "ligand_cluster.csv"))
    protein_cluster_df = pd.read_csv(str(project_dir / "data" / "protein_cluster.csv"))
    ligand_cluster_df = ligand_cluster_df.rename(
        columns={"cluster_id": "ligand_cluster_id"}
    )
    protein_cluster_df = protein_cluster_df.rename(
        columns={"cluster_id": "protein_cluster_id"}
    )
    df = pd.merge(ligand_cluster_df, protein_cluster_df, on="pdbid", how="inner")
    df = df[["pdbid", "ligand_cluster_id", "protein_cluster_id"]]

    ligand_cluster_num = df["ligand_cluster_id"].max() + 1
    protein_cluster_num = df["protein_cluster_id"].max() + 1
    cluster_count = np.zeros((ligand_cluster_num, protein_cluster_num), dtype=int)

    for _, row in df.iterrows():
        cluster_count[row["ligand_cluster_id"], row["protein_cluster_id"]] += 1

    selected_clusters = []
    selected_complex_total = 0
    for protein_cluster_id in range(protein_cluster_num):
        selected_complex_count = np.max(cluster_count[:, protein_cluster_id])
        selected_ligand_cluster_id = np.random.choice(
            np.where(cluster_count[:, protein_cluster_id] == selected_complex_count)[0]
        )
        selected_clusters.append(
            (selected_ligand_cluster_id, protein_cluster_id, selected_complex_count)
        )
        selected_complex_total += selected_complex_count
    print(selected_complex_total)

    df["combined_cluster_id"] = np.nan
    for selected_cluster in selected_clusters:
        df.loc[
            (df["ligand_cluster_id"] == selected_cluster[0])
            & (df["protein_cluster_id"] == selected_cluster[1]),
            "combined_cluster_id",
        ] = selected_cluster[0]
    df = df.dropna()
    df["combined_cluster_id"] = pd.Categorical(df["combined_cluster_id"])
    df["combined_cluster_id"] = df["combined_cluster_id"].cat.codes

    df.to_csv(str(project_dir / "data" / "combined_cluster.csv"), index=False)


if __name__ == "__main__":
    main()
