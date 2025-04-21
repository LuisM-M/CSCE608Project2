import random
import os
from typing import Set
####### PART 1: DATA GENERATION  #######
def generate_unique_records(output_file: str, count: int = 10000,
                            min_val: int = 100000, max_val: int = 200000) -> None:
    random.seed(608) # this ensures rerpoducibility but can be removed to have true randomness
    records: Set[int] = set()
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    while len(records) < count:
        records.add(random.randint(min_val, max_val - 1))
    # output file
    with open(output_file, 'w') as f:
        for record in sorted(records):
            f.write(f"{record}\n")

def load_records(input_file: str) -> list[int]:
    with open(input_file, 'r') as f:
        return [int(line.strip()) for line in f.readlines()]
