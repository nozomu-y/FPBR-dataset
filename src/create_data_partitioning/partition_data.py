from pathlib import Path

import pandas as pd

project_dir = Path(__file__).resolve().parents[2]


def get_insufficient_cluster(complex_nums, ratios):
    total_num = sum(complex_nums.values())
    if total_num == 0:
        return "train"
    current_ratios = {
        "train": complex_nums["train"] / total_num,
        "val": complex_nums["val"] / total_num,
        "test": complex_nums["test"] / total_num,
    }
    selected_insufficient_cluster = "train"
    lowest_ratio = 1.0
    for key, ratio in ratios.items():
        ratio = current_ratios[key] / ratios[key]
        if ratio < lowest_ratio:
            selected_insufficient_cluster = key
            lowest_ratio = ratio

    return selected_insufficient_cluster


def main():
    df = pd.read_csv(project_dir / "data" / "combined_cluster.csv")
    count_df = df.groupby("combined_cluster_id")["pdbid"].count()
    count_df = count_df.sort_values(ascending=False)
    print(count_df)

    ratios = {
        "train": 0.8,
        "val": 0.1,
        "test": 0.1,
    }
    selected_clusters = {
        "train": [],
        "val": [],
        "test": [],
    }
    complex_nums = {
        "train": 0,
        "val": 0,
        "test": 0,
    }

    for cluster_id, num in count_df.items():
        selected_cluster = get_insufficient_cluster(complex_nums, ratios)
        selected_clusters[selected_cluster].append(cluster_id)
        complex_nums[selected_cluster] += num

    for cluster in ratios.keys():
        print(
            f"{cluster}: {len(selected_clusters[cluster])} clusters, {complex_nums[cluster]} complexes"
        )

    df["partition"] = ""
    for cluster in ratios.keys():
        df.loc[
            df["combined_cluster_id"].isin(selected_clusters[cluster]), "partition"
        ] = cluster
    df.sort_values(by=["pdbid"], inplace=True)
    df.to_csv(project_dir / "data" / "partitioned_cluster.csv", index=False)

    df = df.sample(frac=1)
    df.reset_index(drop=True, inplace=True)
    df.loc[: complex_nums["train"], "partition"] = "train"
    df.loc[
        complex_nums["train"] : complex_nums["train"] + complex_nums["val"] - 1,
        "partition",
    ] = "val"
    df.loc[complex_nums["train"] + complex_nums["val"] :, "partition"] = "test"
    df.sort_values(by=["pdbid"], inplace=True)
    df.to_csv(project_dir / "data" / "random_cluster.csv", index=False)

    return


if __name__ == "__main__":
    main()
