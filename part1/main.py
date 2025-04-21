from generator import generate_unique_records, load_records
from builder import build_dense_tree, build_sparse_tree
from tester import run_experiments
import sys
from contextlib import contextmanager

@contextmanager
def redirect_stdout(file_obj):
    original_stdout = sys.stdout
    sys.stdout = file_obj
    try:
        yield
    finally:
        sys.stdout = original_stdout

def main():
    #### PART 4a: DATA GENERATION ###
    with open('part4a.log', 'w') as f:
        with redirect_stdout(f):
            print("================ Part 4a: Data Generation =================")
            print('Check data/btree_keys.txt for generated records')
            print('Check generator.py for the data generation code')
            data_file = "data/btree_keys.txt"
            generate_unique_records(data_file)
            records = load_records(data_file)

    #### PART 4b: BUILDING 2 B+ TREES ####
    with open('part4b.log', 'w') as f:
        with redirect_stdout(f):
            print("")
            print("================ Part 4b: Building 4 B+ Trees=================")
            print("################### START BUILDING DENSE TREE WITH ORDER 13 ###################")
            print("#################################################################")
            dense13 = build_dense_tree(records, 13)

            print("")
            print("################### START BUILDING SPARSE TREE WITH ORDER 13 ###################")
            print("#################################################################")
            sparse13 = build_sparse_tree(records, 13)

            print("")
            print("################### START BUILDING DENSE TREE WITH ORDER 24 ###################")
            print("#################################################################")
            dense24 = build_dense_tree(records, 24)

            print("")
            print("################### START BUILDING SPARSE TREE WITH ORDER 24 ###################")
            print("#################################################################")
            sparse24 = build_sparse_tree(records, 24)

    #### PART 4c: RUNNING EXPERIMENTS ####
    run_experiments(dense13, sparse13, dense24, sparse24)

if __name__ == "__main__":
    main()