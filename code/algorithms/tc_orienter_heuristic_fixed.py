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

def find_max_distance_set(G):
    # Array for storing minimal cycles
    min_cycle = nx.minimum_cycle_basis(G)

    distances = dict(nx.all_pairs_shortest_path_length(G))

    max_distance = float('-inf')
    max_distance_sets = []

    for r in itertools.product(*min_cycle):
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
            max_distance = sum_distance
            max_distance_sets = [r]
        elif sum_distance == max_distance:
            max_distance_sets.append(r)

    return max_distance, max_distance_sets


def tree_child_orient_heuristic_fixed(G):
    v_num = G.number_of_nodes()

    # Finding the maximum distance combination
    _, max_distance_sets = find_max_distance_set(G)

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

