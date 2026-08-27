# directories, files = glob_wildcards("data/{dir}/{file}.csv")
# dir_prefix = ""

directories, files = glob_wildcards("data/leaf_n10_experiment1/{dir}/{file}.csv")
dir_prefix = "leaf_n10_experiment1/"

# directories, files = glob_wildcards("data/leaf_n10_experiment2/{dir}/{file}.csv")
# dir_prefix = "leaf_n10_experiment2/"


paths = [dir_prefix+d+"/"+f for d,f in zip(directories, files)]

algos = [
    # "PR_BF",
    # "PR_FPT",
    # "PR_FPT_CB_CHOOSE",
    # "PR_FPT_CB_PROD",
    # "PR_FPT_CB_COMB",
    # "TCO_H",
    # "TCO_H_F",
    "TCO_H_FR",
    # "TCO_BF",
    # "TCO_BF_O",
    # "TCO_BF_F",
    # "TCO_CB",
]

# can be at most 2 weeks for LSF
# set low to test the snakemake run
experiment_runtime_limit_min = 10000

rule all:
    input:
        ["results/aggregated.csv", "results/aggregated_properties.csv"]


rule aggregate:
    resources:
        runtime_min=60,
        mem_mb=1000
    threads:
        1
    input:
        expand("results_raw/{path}__{algo}",
               path=paths, algo=algos)
    output:
        "results/aggregated.csv"
    shell:
        "cat {input} >> results/aggregated.csv"

rule experiment:
    resources:
        runtime_min=experiment_runtime_limit_min,
        mem_mb=16000
    threads:
        1
    input:
        "data/{path}.csv"
    output:
        "results_raw/{path}__{algo}"
    shell:
        "python code/experiment.py -f {input} -o {output} -a {wildcards.algo}"

rule aggregate_properties:
    resources:
        runtime_min=10,
        mem_mb=1000
    threads:
        1
    input:
        expand("results_properties/{path}", path=paths)
    output:
        "results/aggregated_properties.csv"
    shell:
        "cat {input} >> results/aggregated_properties.csv"

rule properties:
    resources:
        runtime_min=5,
        mem_mb=2000
    threads:
        1
    input:
        "data/{path}.csv"
    output:
        "results_properties/{path}"
    shell:
        "python code/properties.py -f {input} -o {output}"