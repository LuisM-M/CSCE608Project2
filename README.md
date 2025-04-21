# B+ Tree and Hash Join Project

This project consists of two parts: a B+ Tree implementation and a Hash Join implementation. Each part generates log files for different experiments and operations.

## Project Structure

### Part 1: B+ Tree
- **Files under part1 subfolder**:
    - `bplustree.py`: B+ Tree implementation.
    - `node.py`: Node structure for the B+ Tree.
    - `generator.py`: Generates unique records for the tree.
    - `builder.py`: Builds dense/sparse B+ Trees.
    - `tester.py`: Runs insertion, deletion, search, and range operations.
    - `main.py`: Main script to generate data, build trees, and run experiments.
- **Logs**: 
    - `part4a.log`: Generates data in data/btree_keys.txt.
    - `part4b.log`: Builds all 4 B+ Trees.
    - `part4c1.log`: 2 Inserts on each dense B+ Tree.
    - `part4c2.log`: 2 Deletions on each sparse B+ Tree.
    - `part4c3.log`: 5 mixed operations on each B+ Tree.
    - `part4c4.log`: 5 Searches on each B+ Tree.
    - `rangeSearch.log`: 5 Range Searches on each B+ Tree.

### Part 2: Hash Join
- **Files**:
    - `join_hash.py`: Implements hash-based join.
- **Logs**: 
    - `experiment5_1.log`: Results of Experiment 5.1.
    - `experiment5_2.log`: Results of Experiment 5.2.


## Requirements
- Python 3.x
- No external dependencies required.

## Installation
1. Clone the repository.
2. Ensure Python 3 is installed.

## Usage

### Part 1: B+ Tree
1. **Generate Data and Run Experiments**:
    ```bash
    cd part1
    python3 main.py

### Part 2: Hash Join
1. **Generate Data and Run Experiments**:
    ```bash
    cd part2
    python3 join_hash.py