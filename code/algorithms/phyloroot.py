from phyloroot.main_cli import get_class_checker_and_chain_length
from phyloroot.rooting_exponential import c_orientation_exponential
from phyloroot.rooting_fpt_level import c_orientation_fpt_level

def phyloroot_bruteforce(G):
  # Run orientation algorithm Huber2024 bruteforce
  class_checker, length = get_class_checker_and_chain_length("TC")
  orientations = c_orientation_exponential(G, class_checker)
  if orientations:
      return True
  return False


def phyloroot_fpt(G):
  # Run orientation algorithm Huber2024 fpt
  class_checker, length = get_class_checker_and_chain_length("TC")
  orientations = c_orientation_fpt_level(G, length, class_checker, use_cycle_basis=False)
  if orientations:
      return True
  return False


def phyloroot_fpt_cycle_basis_choose(G):
  # Run orientation algorithm Huber2024 fpt with cycle basis improvement
  class_checker, length = get_class_checker_and_chain_length("TC")
  orientations = c_orientation_fpt_level(G, length, class_checker, use_cycle_basis="choose")
  if orientations:
      return True
  return False


def phyloroot_fpt_cycle_basis_product(G):
  # Run orientation algorithm Huber2024 fpt with cycle basis improvement
  class_checker, length = get_class_checker_and_chain_length("TC")
  orientations = c_orientation_fpt_level(G, length, class_checker, use_cycle_basis="product")
  if orientations:
      return True
  return False


def phyloroot_fpt_cycle_basis_combinations(G):
  # Run orientation algorithm Huber2024 fpt with cycle basis improvement
  class_checker, length = get_class_checker_and_chain_length("TC")
  orientations = c_orientation_fpt_level(G, length, class_checker, use_cycle_basis="combinations")
  if orientations:
      return True
  return False
