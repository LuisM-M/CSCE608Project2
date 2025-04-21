from bplustree import BPlusTree

##### PART 2: BUILDING B+ TREES #####
def build_dense_tree(records: list[int], order: int) -> BPlusTree:
    tree = BPlusTree(order)
    # Insert sorted keys in order make dense tree
    for key in sorted(records):
        tree.insert(key)
    return tree

def build_sparse_tree(records: list[int], order: int) -> BPlusTree:
    tree = BPlusTree(order)
    # Insert keys where nodes are as sparse as possible
    # I skip some keys to ensure sparsity
    step = max(1, len(records) // (order * 10))  # step can be adjusted
   
    for key in sorted(records)[::step]:
        tree.insert(key)
    return tree
