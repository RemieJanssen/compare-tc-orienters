import numpy as np
import networkx as nx
import csv
import time
import argparse

from algorithms.phyloroot import phyloroot_bruteforce, phyloroot_fpt, phyloroot_fpt_cycle_basis_choose, phyloroot_fpt_cycle_basis_combinations, phyloroot_fpt_cycle_basis_product
from algorithms.tc_orienter_bruteforce_combinations import tree_child_orient_huber_bruteforce
from algorithms.tc_orienter_bruteforce_fixed import tree_child_orient_huber_bruteforce as tree_child_orient_huber_bruteforce_fixed
from algorithms.tc_orienter_bruteforce_original import tree_child_orient_huber_bruteforce as tree_child_orient_huber_bruteforce_original
from algorithms.tc_orienter_heuristic import tree_child_orient_heuristic
from algorithms.tc_orienter_heuristic_fixed import tree_child_orient_heuristic_fixed
from algorithms.tc_orienter_heuristic_fixed_reduced import tree_child_orient_heuristic_fixed_reduced
from algorithms.tc_orienter_cycles import tree_child_orient

def start():
    global start_time
    start_time = time.perf_counter()

def end(tag="Elapsed time"):
    if "start_time" in globals():
       elapsed_time = time.perf_counter() - start_time
       print("{}: {:.9f} [sec]".format(tag, elapsed_time))
       return elapsed_time
    else:
       print("Function start is not called.")

# Function readcsv
def readcsv(filename):
    distance_matrix = []
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')  # Specify the delimiter
        for row in csv_reader:
            row = [float(value) for value in row]
            distance_matrix.append(row)
    G = nx.from_numpy_array(np.array(distance_matrix))
    return G

def experiment(filename, orientation_algorithm):
    G = readcsv(filename)
    start()
    orientable = orientation_algorithm(G)
    elapsed_time = end()
    return elapsed_time, orientable

def cmd_parser():
    parser = argparse.ArgumentParser(
        description="finds the orientations of an undirected phylogenetic network that belong to a given class of directed networks."
    )
    parser.add_argument(
        "-f",
        "--file",
        help="input file with an undirected phylogenetic network as a adjacency matrix in csv format.",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="output file",
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        help=(
            "An algorithm, choose from: "
            "PR_BF (Phyloroot Bruteforce), "
            "PR_FPT (Phyloroot FPT), "
            "PR_FPT_CB_CHOOSE (Phyloroot FPT with cyclebase: choose), "
            "PR_FPT_CB_PROD (Phyloroot FPT with cyclebase: product), "
            "PR_FPT_CB_COMB (Phyloroot FPT with cyclebase: combinations), "
            "TCO_H (Tree-child orienter Heuristic), "
            "TCO_H_F (Tree-child orienter Heuristic Fixed), "
            "TCO_H_FR (Tree-child orienter Heuristic Fixed Reduced), "
            "TCO_BF (Tree-child orienter Bruteforce Combinations), "
            "TCO_BF_O (Tree-child orienter Bruteforce Original), "
            "TCO_BF_F (Tree-child orienter Bruteforce Fixed), "
            "TCO_CB (Tree-child orienter FPT Cycle base), "
        )
    )
    return parser.parse_args()


if __name__ == "__main__":
    cmd_args = cmd_parser()
    algo_dict = {
        "PR_BF": phyloroot_bruteforce,
        "PR_FPT": phyloroot_fpt,
        "PR_FPT_CB_CHOOSE": phyloroot_fpt_cycle_basis_choose,
        "PR_FPT_CB_PROD": phyloroot_fpt_cycle_basis_product,
        "PR_FPT_CB_COMB": phyloroot_fpt_cycle_basis_combinations,
        "TCO_H": tree_child_orient_heuristic,
        "TCO_H_F": tree_child_orient_heuristic_fixed,
        "TCO_H_FR": tree_child_orient_heuristic_fixed_reduced,
        "TCO_BF": tree_child_orient_huber_bruteforce,
        "TCO_BF_F": tree_child_orient_huber_bruteforce_fixed,
        "TCO_BF_O": tree_child_orient_huber_bruteforce_original,
        "TCO_CB": tree_child_orient,
    }
    elapsed_time, orientable = experiment(cmd_args.file, algo_dict[cmd_args.algorithm])
    out_string = f"elapsed time: {elapsed_time}, orientable: {orientable}"
    print(out_string)
    if cmd_args.output:
        with open(cmd_args.output, "w+") as f:
            f.write(f"{cmd_args.file},{cmd_args.algorithm},{elapsed_time},{orientable}\r\n")
