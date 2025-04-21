from node import BPlusTreeNode

class BPlusTree:
    def __init__(self, order):
        self.root = BPlusTreeNode(is_leaf=True)
        self.order = order

        self.min_keys_leaf = order // 2 
        self.max_keys_leaf = order - 1

        self.min_keys_internal = order // 2
        self.max_keys_internal = order - 1

    #### PART 3: OPERATIONS ON B+ TREE #################################
    def search(self, key):
        current_node = self.root
        steps = 0

        while not current_node.is_leaf:
            steps += 1
            i = 0
            while i < len(current_node.keys) and key >= current_node.keys[i]:
                i += 1
            current_node = current_node.children[i]

        steps += 1  
        found = key in current_node.keys
        return found, steps

    # RANGE SEARCH
    def range_search(self, start, end):
        results = []
        node = self.root
        while not node.is_leaf:
            node = node.children[0]
        while node:
            for key in node.keys:
                if start <= key <= end:
                    results.append(key)
            if node.children:
                node = node.children[-1]
            else:
                break
        print("Range search result:", results)
        return results
    
    # RANGE COUNT
    def range_count(self, start, end):
        count = 0
        node = self.root
        while not node.is_leaf:
            node = node.children[0]
        while node:
            for key in node.keys:
                if start <= key <= end:
                    count += 1
            if node.children:
                node = node.children[-1]
            else:
                break
        return count

    # INSERTION
    def insert(self, key):
        print(f"Inserting {key}")
        old_root = str(self.root)
        root, new_key, new_child = self._insert(self.root, key)
        if new_child:
            new_root = BPlusTreeNode()
            new_root.keys = [new_key]
            new_root.children = [root, new_child]

            self.root = new_root
            print(f"[Insert] Created new root: {new_root}")
        print("Before Insert:", old_root)
        print("After Insert:", self.root)

    # Helper function for insertion
    def _insert(self, node, key):
        if node.is_leaf:
            print(f"[Insert] Leaf node before insertion: {node.keys}") # added for clarity
            if key in node.keys:
                return node, None, None
            node.keys.append(key)
            node.keys.sort()
            
            if len(node.keys) > self.max_keys_leaf:
                print(f"[Insert] Leaf node overflow detected (needs split)")
                return self._split_leaf(node)
            print(f"[Insert] Leaf node after insertion: {node.keys}") # also added for clarirty
            return node, None, None

        for i, item in enumerate(node.keys):
            if key < item:
                child, new_key, new_child = self._insert(node.children[i], key)
                break
        else:
            i = len(node.keys)
            child, new_key, new_child = self._insert(node.children[-1], key)

        if new_child:
            # print(f"[Insert] ) need to be cleaerr

            print(f"BEFORE Internal Node Update: {node.keys} (Node ID: {id(node)})")
            node.keys.insert(i, new_key)
            node.children.insert(i + 1, new_child)
            # print(f"AFTER Internal Node Update: {node.keys}")
            print(f"AFTER Internal Node Update: {node.keys} (Node ID: {id(node)})")
            if len(node.keys) > self.max_keys_internal:
                print(f"[Insert] Internal node overflow detected (needs split)")
                return self._split_internal(node)
        return node, None, None

    # Helper function for splitting nodes
    def _split_leaf(self, node):
        print(f"\n[Split] Splitting leaf node (BEFORE): {node}")
        print(f"\n[Split] Splitting leaf node (BEFORE): {node.keys}") ## change
        split_index = (self.order + 1) // 2
        new_node = BPlusTreeNode(is_leaf=True)
        new_node.keys = node.keys[split_index:]
        node.keys = node.keys[:split_index]
        if node.children:
            new_node.children = node.children
        node.children = [new_node]
        print(f"[Split] Propagating key: {new_node.keys[0]}")
        return node, new_node.keys[0], new_node
    
    # Helper function for splitting internal nodes
    def _split_internal(self, node):
        print(f"\n[Split] Splitting internal node (BEFORE): {node}")
        split_index = len(node.keys) // 2
        new_node = BPlusTreeNode()

        up_key = node.keys[split_index]
        new_node.keys = node.keys[split_index+1:]
        new_node.children = node.children[split_index+1:]
        node.keys = node.keys[:split_index]
        node.children = node.children[:split_index+1]

        print(f"[Split] Key to propagate up: {up_key}")
        print(f"[Split] Internal node split into: {node.keys} (Left) and {new_node.keys} (Right)")
        return node, up_key, new_node

    # DELETION
    def delete(self, key):
        print(f"\nDeleting {key}")
        old_root = str(self.root)
        changed = self._delete(self.root, key)

        if changed and len(self.root.keys) == 0 and not self.root.is_leaf:
            self.root = self.root.children[0]
        print("Before Delete:", old_root)
        print("After Delete:", self.root)

    # Helper function for deletion    
    def _delete(self, node, key):
        if node.is_leaf:
            print(f"[Delete] Leaf node before deletion: {node}")
            if key in node.keys:
                print(f"[Delete] Key {key} found. Removing...")
                node.keys.remove(key)
                print(f"[Delete] Leaf node after deletion: {node}")
                underflow = len(node.keys) < self.min_keys_leaf
                if underflow:
                    print(f"[Delete] Leaf underflow detected (needs adjustment).")
                return underflow
            else:
                print(f"[Delete] Key {key} not found in leaf node.")
                return False

        for i, item in enumerate(node.keys):
            if key < item:
                underfull = self._delete(node.children[i], key)
                break
        else:
            underfull = self._delete(node.children[-1], key)
            i = len(node.children) - 1

        if underfull:
            print(f"\n[Underflow] Parent node: {node}")
            print(f"[Underflow] Affected child index: {i}")
            left = node.children[i - 1] if i > 0 else None
            right = node.children[i + 1] if i + 1 < len(node.children) else None
            print(f"[Underflow] Left sibling: {left}")
            print(f"[Underflow] Right sibling: {right}")

            # CASE 1: Borrow from left sibling
            if node.children[i].is_leaf and left and len(left.keys) > self.min_keys_leaf:
                print(f"\n[Borrow Left] Sibling before borrow: {left}")
                # move the last key from left sibling to underfull node
                borrowed_key = left.keys.pop(-1)
                node.children[i].keys.insert(0, borrowed_key)

                # update key in parentnode
                node.keys[i - 1] = borrowed_key
                print(f"[Borrow Left] Sibling after borrow: {left}")
                return False

            # CASE 2: Borrow from right sibling
            elif node.children[i].is_leaf and right and len(right.keys) > self.min_keys_leaf:
                print(f"\n[Borrow Right] Sibling before borrow: {right}")
                # move the first key from right sibling to underfull node
                borrowed_key = right.keys.pop(0)
                node.children[i].keys.append(borrowed_key)

                #update key in parent node
                node.keys[i] = right.keys[0]
                print(f"[Borrow Right] Sibling after borrow: {right}")
                return False

            # CASE 3: Merge with left sibling
            elif left:
                print(f"\n[Merge Left] Left sibling before merge: {left}")
                if not node.children[i].is_leaf:
                    left.keys.append(node.keys[i - 1])
                # combine keys and children
                left.keys += node.children[i].keys
                left.children += node.children[i].children

                #remove merged child and parent key
                del node.children[i]
                del node.keys[i - 1]
                print(f"[Merge Left] Merged node: {left}")
            
            # CASE 4: Merge with right sibling
            elif right:
                print(f"\n[Merge Right] Right sibling before merge: {right}")
                
                # for internal nodes: propagate the key down
                if not node.children[i].is_leaf:
                    node.children[i].keys.append(node.keys[i])
                # combine keys and children



                node.children[i].keys += right.keys
                node.children[i].children += right.children
                del node.children[i + 1]
                del node.keys[i]
                print(f"[Merge Right] Merged node: {node.children[i]}")

            return len(node.keys) < self.min_keys_internal

        return False

    # VALIDATION function
    def validate(self):
        def _validate_node(node, is_leaf, depth=0):

            # first, im checking node type matches
            # the expected type (leaf or internal)
            if node.is_leaf != is_leaf:
                raise ValueError("Leaf/internal type mismatch")
            

            # validation for root node
            if node == self.root:
                if len(node.keys) >= self.order:
                    raise ValueError("Root overflow")
            else:
                # non-root nodes
                min_keys = self.min_keys_leaf if is_leaf else self.min_keys_internal  # Corrected
                if len(node.keys) < min_keys:
                    raise ValueError("Node underflow")
            #recursively check children
            if not node.is_leaf:
                for child in node.children:
                    _validate_node(child, child.is_leaf, depth + 1)
        # starting validationfrom the root node
        _validate_node(self.root, self.root.is_leaf)