class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []  # If leaf: [next_leaf], else: [child nodes]

    def __str__(self):
        if self.is_leaf:
            return f"LeafNode(keys={self.keys})"
        else:
            return f"InternalNode(keys={self.keys})"
