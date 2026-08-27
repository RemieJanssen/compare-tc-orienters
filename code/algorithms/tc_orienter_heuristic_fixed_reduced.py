import networkx as nx
import itertools

# Checking whether tree-child
def is_tree_child(graph, indeg, i):
  if len(list(graph.successors(i))) == 0:
    return True
  for j in graph.successors(i):
    if indeg[j] == 1:
      return True
  return False

# Function select_vertices
def select_vertices(n, r):
  # Create a list of vertices
  vertices = list(range(n))
  # Generate vertex combinations using the combinations function
  selected_vertices = list(itertools.combinations(vertices, r))
  return selected_vertices

# Function orientation
def orientation(G, e_rho, v_num):
  N = nx.Graph()
  N.add_nodes_from(range(v_num))

  # Inserting a root
  root = max(N.nodes) + 1
  N.add_node(root)
  N.add_edge(root, e_rho[0])
  N.add_edge(root, e_rho[1])

  return N


def product_without_duplicates_or_neighbours(lists, G, forbidden=None, chosen=None, i=0):
    """Generates the Cartesian product of a list of lists, but skips combinations with duplicates.

    Args:
        lists (list(list(int))): A list of lists, where each inner list contains elements to combine.
        G: XXX
    Yields:
        set(int): A combination of elements, one from each inner list, without duplicates.
    """
    if chosen is None:
        chosen = []
        lists = sorted(lists, key=len)  # Sort the lists by length to optimize the search
    if forbidden is None:
        forbidden = set()
    if i == len(lists):
        yield set(chosen)
    else:
        for item in lists[i]:
            if item in chosen or item in forbidden:
                continue
            chosen.append(item)
            forbidden_new = forbidden.union(set(G.neighbors(item)))
            yield from product_without_duplicates_or_neighbours(lists, G, forbidden=forbidden_new, chosen=chosen, i=i+1)
            chosen.pop()

def get_relevant_side_nodes(cycle_basis):
    # returns all nodes in the cycle basis that
    # - have degree 3 (generator nodes)
    # - have two neighbours of degree 2 (but only pick one per side!)
    # - have a neighbour of degree 3 and a neighbour of degree 2 that has a neighbour of degree 3
    union_of_blob_generators = nx.Graph()
    for cycle in cycle_basis:
        union_of_blob_generators.add_edges_from(zip(cycle, cycle[1:]+[cycle[0]]))

    selected_nodes = []
    nodes = [v for v in union_of_blob_generators.nodes()]
    # first get all degree-3 nodes and remove them
    for v in nodes:
        if union_of_blob_generators.degree(v) == 3:
            selected_nodes += [v]
            union_of_blob_generators.remove_node(v)

    # now all remaining components are the side paths
    # select all vertices if length <=2
    # select an arbitrary middle one if length >2

    for path in nx.connected_components(union_of_blob_generators):
        if len(path) <= 2:
            selected_nodes += path
        else:
            for node in path:
                if union_of_blob_generators.degree(node) == 2:
                    selected_nodes += [node]
                    break
    return selected_nodes



def find_candidate_sets(G):
    # loop through min_cycle with a custom product
    # first compute sides (union of all edges in the cycles)
    # if side has length>=3, use middle node as retic candidate, and remove other nodes as retic candidates
    # -> fine for all sides except where the root is? Or is it also fine for those? Proof needed!
    # cut when:
    #  - distance to another chosen node is <=1, i.e. add neighbours of chosen node to forbidden set
    #  - 2 nodes on the same side (is caught by the previous, icw using middle node for long sides?!)

    # Array for storing minimal cycles
    min_cycle = nx.minimum_cycle_basis(G)
    relevant_nodes = get_relevant_side_nodes(min_cycle)
    print("cycles: ",min_cycle)
    print("relevant nodes: ", relevant_nodes)
    for cycle in min_cycle:
        cycle = [v for v in cycle if v in relevant_nodes]
    print("reduced cycles: ", min_cycle)

    distances = dict(nx.all_pairs_shortest_path_length(G))

    max_distance = float('-inf')
    max_distance_sets = []



    no_of_candidates_considered = 0
    for r in product_without_duplicates_or_neighbours(min_cycle, G):
        sum_distance = 0
        for u, v in itertools.combinations(r, 2):
            distance = distances[u][v]
            if distance <= 1:
                # reticulations are next to each other or duplicates
                # so this cannot be tree-child
                continue
            else:
                sum_distance += distance

        if sum_distance > max_distance:
            no_of_candidates_considered +=1
            max_distance = sum_distance
            max_distance_sets = [r]
        elif sum_distance == max_distance:
            no_of_candidates_considered +=1
            max_distance_sets.append(r)

    print("candidates_considered: ", no_of_candidates_considered)
    print("final_number_of_candidates: ", len(max_distance_sets))
    return max_distance_sets


def tree_child_orient_heuristic_fixed_reduced(G):
    v_num = G.number_of_nodes()

    # Finding the maximum distance combination
    max_distance_sets = find_candidate_sets(G)

    for r_set in max_distance_sets:
        i_max = 0
        i_max = r_set

        indeg = [1] * (v_num+1)
        for i in i_max:
            indeg[i] = 2
        indeg[v_num] = -1

        G_temp = nx.Graph()
        # N is an undirected graph, N2 is a directed graph
        N2 = nx.DiGraph()
        N = nx.Graph()
        N2.add_nodes_from(range(v_num + 1))

        for root_edge in G.edges():
            G_temp.clear()
            N.clear()
            N2.clear()
            N2.add_nodes_from(range(v_num + 1))
            G_temp = G.copy()
            N = orientation(G_temp, root_edge, v_num)
            G_temp.remove_edge(root_edge[0], root_edge[1])

            k = 0
            while k < v_num:
                k += 1
                for i in range(v_num):
                    if N.degree(i) == indeg[i]:
                        for j in list(G_temp.neighbors(i)):
                            N.add_edge(i, j)
                            N2.add_edge(i, j)
                            G_temp.remove_edge(i, j)
            N2.add_edge(v_num, root_edge[0])
            N2.add_edge(v_num, root_edge[1])


            if nx.is_weakly_connected(N2) and all(is_tree_child(N2, indeg, l) for l in range(v_num + 1)):
                return True
    return False

