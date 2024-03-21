import argparse
import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import scipy.spatial.distance as ssd
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage

project_dir = Path(__file__).resolve().parents[2]


def plot_dendrogram(linkage_result, pdbids):
    plt.figure(num=None, figsize=(160, 90), dpi=300, facecolor="w", edgecolor="k")
    with plt.rc_context({"lines.linewidth": 0.5}):
        dendrogram(
            linkage_result,
            labels=pdbids,
            truncate_mode="lastp",
            p=1000,
        )
    plt.ylabel("Distance")
    plt.show()


def main(tanimoto_distance):
    with open(project_dir / "data/distance_matrix.pkl", "rb") as f:
        (pdbids, dist_matrix) = pickle.load(f)

    dist_array = ssd.squareform(dist_matrix)
    linkage_result = linkage(dist_array, method="single", metric="euclidean")
    distance_threshold = tanimoto_distance
    cluster_result = fcluster(linkage_result, distance_threshold, criterion="distance")

    data = []
    for p, c in zip(pdbids, cluster_result):
        d = {}
        d["pdbid"] = p
        d["cluster_id"] = c
        data.append(d)
    df = pd.DataFrame(data)
    df = df[["cluster_id", "pdbid"]]
    df = df.sort_values(["cluster_id", "pdbid"])
    df["cluster_id"] -= 1
    df.to_csv(project_dir / "data/ligand_cluster.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tanimoto-distance",
        type=float,
        required=True,
    )
    args = parser.parse_args()
    tanimoto_distance = args.tanimoto_distance
    main(tanimoto_distance)
