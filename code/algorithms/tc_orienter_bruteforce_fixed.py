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
def orientation(v_num, e_rho):
  N = nx.Graph()
  N.add_nodes_from(range(v_num))

  # Inserting a root
  root = max(N.nodes) + 1
  N.add_node(root)
  N.add_edge(root, e_rho[0])
  N.add_edge(root, e_rho[1])

  return N


# Input
def tree_child_orient_huber_bruteforce(G):
  v_num = G.number_of_nodes()
  e_num = G.number_of_edges()
  r_num = e_num - v_num + 1



  G_temp = nx.Graph()
  # N is an undirected graph, N2 is a directed graph
  N2 = nx.DiGraph()
  N = nx.Graph()

  internal_nodes = [node for node in G.nodes if G.degree(node) > 1]

  # Select one of the reticulation sets
  for r_set in itertools.combinations(internal_nodes,r_num):

    # Set the desired in-degrees
    indeg = [1] * (v_num+1)
    for j in r_set:
      indeg[j] = 2
    indeg[v_num] = -1

    for root_edge in G.edges():
      G_temp.clear()
      N.clear()
      N2.clear()
      N2.add_nodes_from(range(v_num + 1))
      G_temp = G.copy()
      N = orientation(v_num, root_edge)
      G_temp.remove_edge(root_edge[0], root_edge[1])
      k = 0

      # Repeatedly run Algorithm 1 in Huber et al. (2024)
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

      # check if N2 has the required degrees
      if any((N2.in_degree(p) != indeg[p] for p in range(v_num))):
        continue

      if nx.is_weakly_connected(N2) and all(is_tree_child(N2, indeg, l) for l in range(v_num + 1)):
        return True
  return False
