# Phlag analysis of the mammalian phylogeny
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19713368.svg)](https://doi.org/10.5281/zenodo.19713368)

This repository contains the Phlag analysis results, gene trees, species trees, and supporting data for the mammalian dataset (experiment E4) presented in:

> Şapcı AOB, Arasti S, Braun EL, Mirarab S. **Phlag: Scalable detection of genomic regions with unexplained phylogenetic heterogeneity.** Bioinformatics, ISMB issue (2026).

Phlag is available at [github.com/bo1929/phlag](https://github.com/bo1929/phlag).

## Files

- `alltrees.tree.gz`: Compressed gene trees (19,465 trees) inferred from chromosome 3 of the mammalian alignment by [Foley et al.](https://www.science.org/doi/10.1126/science.abl8189). We estimated gene trees using IQ-TREE under the GTR+G4 model from 1Kbp subalignments selected with minimum missing data from each 10Kbp segment.

- `labelled_species_tree.nwk`: Species tree in Newick format with 241 mammalian taxa and internal nodes labelled `I0`–`I239` with branch lengths.

- `ref.topology`: Reference species tree topology.

- `qqs.txt`: Precomputed quartet quartet site (QQS) frequencies for all gene trees and internal branches, used as input to Phlag.

- `pos`: Genomic positions (on the human chromosome 3 coordinate) for each gene tree window.

- `order.txt`: File identifiers for each gene tree locus/window.

- `taxon_map.txt`: Mapping from internal node labels (`I0`–`I239`) to taxonomic family names via NCBI taxonomy.

- `taxon_map_order.txt`: Mapping from internal node labels to taxonomic order names.

- `taxdump.tar.gz`: NCBI taxonomy database dump used by `map_lca.py`.

- `map_lca.py`: Python script (using ete3) for resolving internal node labels to their lowest common ancestor in NCBI taxonomy.

- `prep.sh`: Preprocessing script that extracts Hellinger distances from Phlag prediction files and produces summary files.

- `echo_cmd.sh`: Script containing the Phlag commands used to generate predictions under different hyperparameter settings.

## Phlag predictions

- `all_pred-{PARAMS}-chr3/`: Directories containing Phlag output for chromosome 3 under different hyperparameter combinations. Each directory contains:
  * `distances_chr3.txt`: Hellinger distance between the null and alternative emission distributions for each internal branch.
  * `pred-I{NODE}-{PARAMS}.txt`: Per-branch prediction file containing the Phlag command, the modified species tree, decoded state predictions, and the distance metric.

  The naming convention encodes hyperparameters as follows:
  * `eap{beta}`: expected number of anomalies (`--expected-num-anomalies`), e.g., `eap50`: beta = 50.
  * `ep{1-rho}`: expected anomaly proportion (`--expected-anomaly-proportion`), e.g., `ep005`: 1-rho = 0.05.
  * `penalty{lambda}` / `npenalty{N}`: prior penalty strength (`lambda`), with `n` prefix indicating a negative value.

  Available parameter combinations:
  * `all_pred-eap50_ep005_penalty15-chr3`
  * `all_pred-eap50_ep002_penalty15-chr3`
  * `all_pred-eap40_ep005_penalty15-chr3`
  * `all_pred-eap100_ep005_penalty15-chr3`  (the main paper analysis)
  * `all_pred-eap100_ep010_penalty15-chr3`

## Description
Phlag was applied to 19,465 gene trees inferred from chromosome 3 of the mammalian genome alignment by Foley et al., covering 241 species. Gene trees were estimated by selecting 1Kbp subalignments with minimum missing data from each 10Kbp segment and running IQ-TREE under GTR+G4. Phlag was applied to 136 internal branches under key mammalian orders (Carnivora, Chiroptera, Primates, Artiodactyla, and Rodentia), retaining branches that define a quadripartition in at least 90% of the gene trees. Each branch was analyzed individually (single focal branch) using the prior-updated mode with topology-order emissions.
