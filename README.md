# compare-tc-orienters
Compare output and running time of algorithms for Tree-Child orientation from tree-child-orienter and phyloroot.


## Authorship statement

This repository of tests is based on the Tree-Child Orienter repository by Hayamizu.
It includes their set of test networks and the code for their orientation algorithm.
This repo replaces their experiments with new experiments.
Including tests for several other algorithms for Tree-Child Orientation.

The original repo was used for the experiments in the paper:

> Tsuyoshi Urata, Manato Yokoyama, and Momoko Hayamizu. **Orientability of Undirected Phylogenetic Networks to a Desired Class: Practical Algorithms and Application to Tree-Child Orientation**. In _24th International Workshop on Algorithms in Bioinformatics (WABI 2024)_. Leibniz International Proceedings in Informatics (LIPIcs), Volume 312, pp. 9:1-9:17, Schloss Dagstuhl – Leibniz-Zentrum für Informatik (2024) https://doi.org/10.4230/LIPIcs.WABI.2024.9

The current repo provides the experiments for the upcoming paper:

> Remie Janssen **XXX**


## Repository Structure

The repository is organized as follows:
* `conda`: The definition file of the conda environment used for the experiments
* `code`: Contains all the code used for the experiments
  * `algorithms`: The implementations or wrappers of the algorithms
    * `TC-orientation`: Implementation of our practical exponential algorithm for C-Orientation, adapted to the Tree-Child Orientation problem (Algorithm 1)
    * `TC-orientation-bruteforce-huber2024`: Implementation of the existing exact exponential-time algorithm for C-Orientation  ([Algorithm 2 in Huber et al 2024](https://doi.org/10.1016/j.jcss.2023.103480))
    * `TC-orientation-heuristic`: Implementation of our heuristic method specifically developed for the tree-child orientation problem (Algorithm 2)
  * `experiment.py`: The main python method to run and time each algorithm with a common CLI
  * `properties.py`: Code to compute several properties for all the input networks
* `data`: Contains the input networks used for the experiments (copied from https://github.com/hayamizu-lab/tree-child-orienter/)
  * `inputs`: Data sets used in the experiments
* `results`: Aggregated results of all running times and algorithm output

## Usage

### Environment set-up

First, clone this repository to your local machine and access the main directory using the command below:
```terminal
git clone https://github.com/RemieJanssen/compare-tc-orienters.git
cd compare-tc-orienters
```

To run this project, you may require the following packages:
+ sys
+ numpy
+ networkx
+ matplotlib
+ networkx
+ csv
+ itertools
+ time
+ scipy
+ phyloroot

You can install these with conda with:
```
conda env update -f ./conda/compare-tc-orienters.source.yaml
```

To use the exact environment used for the experiments, instead use `./conda/compare-tc-orienters.yaml`.

Activate the environment and you're ready to run the experiments.

### Experiments

The full set of experiments can be run with Snakemake on an LSF cluster with:
```
snakemake --profile default_lsf
```

Or locally with
```
snakemake
```

## Important change in Hayamizu code

For the Huber brute force algorithm, the reticulation sets are generated with `itertools.combinations` instead of `itertools.permutations`!