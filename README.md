# FPBR-dataset

FPBR dataset: https://github.com/nozomu-y/FPBR-dataset/blob/main/data/partitioned_cluster.csv

## Building the dataset

### Prerequisites

- Python 3
- mmseqs2

### Installing the dependencies

```bash
pip3 install -r requirements.txt
```

### Downloading the data

```bash
python3 src/download/get_fastas.py
python3 src/download/get_html_sources.py
```

The above scripts uses `time.sleep` to avoid overloading the servers.
The default sleep time is 60 seconds.
Change the sleep time at your own risk.

### Creating the protein clusters

```bash
python3 src/create_protein_clusters/concat_fastas.py
cd data/mmseqs2
mmseqs createdb all.fasta DB
mmseqs cluster -c 0.4 DB DB_clu tmp
mmseqs createtsv DB DB DB_clu clustered.tsv
cd ../..
python3 src/create_protein_clusters/parse_mmseqs2_output.py
```

### Creating the ligand clusters

```bash
python3 src/create_ligand_clusters/parse_pdbbind_html.py
python3 src/create_ligand_clusters/calculate_distance.py
python3 src/create_ligand_clusters/cluster_by_distance.py
```

### Combining the protein and ligand clusters

```bash
python3 src/create_combined_clusters/combine_clusters.py
```

### Partitioning the dataset

```bash
python3 src/create_data_partitioning/partition_data.py
```
