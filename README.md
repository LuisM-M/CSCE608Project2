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
    - ' 

### Part 2: Hash Join
- **Files**:
  - `join_hash.py`: Implements hash-based join.
- **Logs**: 

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