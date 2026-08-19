import numpy as np
import networkx as nx
import csv
import argparse


def blob_properties(graph):
    blob_properties = []
    # For each biconnected component
    for bicomponent in nx.biconnected_components(graph):
        # A bicomponent is a blob if it consists of at least 2 nodes
        if len(bicomponent) > 2:
            blob = graph.subgraph(bicomponent)
            # leaves have been removed, to reticulation number is:
            retics = len(blob.edges) - len(blob.nodes) + 1
            blob_size = len(bicomponent)
            blob_level = retics
            blob_properties += [(blob_size, blob_level)]
    return blob_properties


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

def properties(filename):
    G = readcsv(filename)
    blobs = blob_properties(G)
    level = max([blob[1] for blob in blobs]) if blobs else 0
    number_of_blobs = len(blobs)
    properties = {
        "number_of_nodes": len(G.nodes),
        "number_of_edges": len(G.edges),
        "number_of_reticulations": len(G.edges) - len(G.nodes) + 1,
        "blob_properties": blobs,
        "level": level,
        "number_of_blobs": number_of_blobs
    }

    return properties

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
    return parser.parse_args()


if __name__ == "__main__":
    cmd_args = cmd_parser()
    graph_properties = properties(cmd_args.file)
    out_print = f"{cmd_args.file},{graph_properties["number_of_nodes"]},{graph_properties["number_of_edges"]},{graph_properties["number_of_reticulations"]},{graph_properties["level"]},{graph_properties["number_of_blobs"]},{"|".join([f"{blob[0]};{blob[1]}" for blob in graph_properties["blob_properties"]])}\r\n"
    print(out_print)
    if cmd_args.output:
        with open(cmd_args.output, "w+") as f:
            f.write(out_print)
