import random
from generator import load_records
import sys
from contextlib import contextmanager

@contextmanager
def redirect_stdout(file_obj):
    """Context manager to redirect stdout to a file."""
    # Save the original stdout
    original_stdout = sys.stdout
    # Redirect stdout to the file object
    sys.stdout = file_obj
    try:
        yield
    finally:
        sys.stdout = original_stdout

def run_experiments(dense13, sparse13, dense24, sparse24):
    records = load_records('data/btree_keys.txt')

    def random_insert(tree):
        key = random.randint(100000, 200000)
        print(f"=== Inserting {key} ===")
        tree.insert(key)

    def random_delete(tree):
        key = random.randint(100000, 200000)
        print(f"=== Deleting {key} ===")
        tree.delete(key)

    def random_search(tree, tree_name):
        key = random.choice(records)
        print(f"=== Searching {key} ===")
        found, steps = tree.search(key)
        print(f"[{tree_name}] Search key {key} -> {'Found' if found else 'Not Found'} in {steps} step(s)")

    # Part 4(c1)
    with open('part4c1.log', 'w') as f:
        with redirect_stdout(f):
            print("========== PART 4(c1) ==========")
            print("##################### Two Insertions on the Dense13 Tree #####################")
            for _ in range(2):
                print('')
                print('[Dense13] Insertion: *************')
                random_insert(dense13)
            
            print("\n##################### Two Insertions on the Dense24 Tree #####################")

            for _ in range(2):
                print('')
                print('[Dense24] Insertion: *************')
                random_insert(dense24)

    # Part 4(c2)
    with open('part4c2.log', 'w') as f:
        with redirect_stdout(f):
            print("========== PART 4(c2) ==========")
            print("##################### Two Deletions on the Sparse13 Tree #####################")
            for _ in range(2):
                print('')
                print('[Sparse13] Deletion: *************')
                random_delete(sparse13)
                
            print("\n##################### Two Deletions on the Sparse24 Tree #####################")

            for _ in range(2):
                print('')
                print('[Sparse24] Deletion: *************')
                random_delete(sparse24)

    # Part 4(c3)
    with open('part4c3.log', 'w') as f:
        with redirect_stdout(f):
            print("========== PART 4(c3) ==========")
            print("== Mixed Insert/Delete ==")
            
            # Create a list of trees to iterate over
            trees = [
                (dense13, "Dense13"),
                (sparse13, "Sparse13"),
                (dense24, "Dense24"),
                (sparse24, "Sparse24")
            ]

            # ensure randomness of operations for a total of 5
            for tree, tree_name in trees:
                print(f"\n##################### Five Operations on {tree_name} Tree #####################")
                for op_number in range(1, 6):  # 5 operations per tree
                    # Randomly choose insert/delete
                    is_insert = random.choice([True, False])
                    print(f"\n[{tree_name}] Operation {op_number}: {'Insertion' if is_insert else 'Deletion'} *************")
                    if is_insert == True:
                        random_insert(tree)
                    else:
                        random_delete(tree)

    # Part 4(c4)
    with open('part4c4.log', 'w') as f:
        with redirect_stdout(f):
            print("========== PART 4(c4) ==========")
            print("== Random Searches ==")

            print("\n##################### Five Random Searches on the Dense13 Tree #####################")
            for op_number in range(1,6):
                print(f"Random Search {op_number}: ")
                random_search(dense13, "Dense13")
                print("")

            print("\n\n##################### Five Random Searches on the Sparse13 Tree #####################")
            for op_number in range(1,6):
                print(f"Random Search {op_number}:")
                random_search(sparse13, "Sparse13")
                print("")
            
            print("\n\n##################### Five Random Searches on the Dense24 Tree #####################")
            for op_number in range(1,6):
                print(f"Random Search {op_number}:")
                random_search(dense24, "Dense24")
                print("")
            
            print("\n\n##################### Five Random Searches on the Sparse24 Tree #####################")
            for op_number in range(1,6):
                print(f"Random Search {op_number}:")
                random_search(sparse24, "Sparse24")
                print("")

    # Range search test
    with open('rangeSearch.log', 'w') as f:
        with redirect_stdout(f):
            print("================== Randomized Range Search Test ====================")
            trees = [
                (dense13, "Dense13"),
                (sparse13, "Sparse13"),
                (dense24, "Dense24"),
                (sparse24, "Sparse24")
            ]

            for tree, tree_name in trees:
                print(f"\n##################### Five Range Searches on {tree_name} Tree #####################")
                for op_number in range(1, 6):  
                    # Generate random start and end using existing records
                    key1 = random.choice(records)
                    key2 = random.choice(records)
                    start = min(key1, key2)
                    end = max(key1, key2)
                    # print(f"\n[{tree_name}] Range Search {op_number}: From {start} to {end}")
                    # tree.range_search(start, end)
                    # In the range search test section of tester.py:
                    print(f"\n[{tree_name}] Range Search {op_number}: From {start} to {end}")
                    count = tree.range_count(start, end)
                    print(f"Found {count} keys in range")