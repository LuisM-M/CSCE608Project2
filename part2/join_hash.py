import random
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

######################################### Part 1: Data Generation Implementation #########################################
def generate_S():
    """Generates relation S with 5000 unique B-values (10k-50k) and sequential C-values"""
    B_values = random.sample(range(10000, 50001), 5000)
    assert len(B_values) == len(set(B_values)), "Duplicate B-values found in S!"
    
    S_tuples = [(b, f'C{i}') for i, b in enumerate(B_values)]
    return [S_tuples[i:i+8] for i in range(0, len(S_tuples), 8)]

def generate_R_part5_1(S_B_values):
    selected_Bs = random.choices(S_B_values, k=1000)
    R_tuples = [(f'A{i}', b) for i, b in enumerate(selected_Bs)]
    return [R_tuples[i:i+8] for i in range(0, len(R_tuples), 8)]

def generate_R_part5_2():
    B_values = [random.randint(20000, 30000) for _ in range(1200)]
    R_tuples = [(f'A{i}', b) for i, b in enumerate(B_values)]
    return [R_tuples[i:i+8] for i in range(0, len(R_tuples), 8)]



######################################### Part 2: Virtual Disk I/O Implementation #########################################
disk = {}
disk_io_reads = 0
disk_io_writes = 0

def read_block(relation, block_num):
    global disk_io_reads
    disk_io_reads += 1
    return disk.get(relation, [])[block_num]

def write_block(relation, block):
    global disk_io_writes
    disk_io_writes += 1
    disk.setdefault(relation, []).append(block)

def reset_disk():
    global disk, disk_io_reads, disk_io_writes
    disk = {'S': []}
    disk_io_reads = 0
    disk_io_writes = 0



######################################### Part 3: Hash Function Implementation #########################################
def hash_b(b, num_partitions=14):
    return b % num_partitions




######################################### Part 4: Join Algorithm Implementation #########################################
def partition_relation(relation_name, num_partitions=14):
    for part in range(num_partitions):
        part_name = f"{relation_name}_part_{part}"
        if part_name in disk:
            del disk[part_name]
    
    if relation_name not in disk:
        return

    buffers = [[] for _ in range(num_partitions)]
    for block_num in range(len(disk[relation_name])):
        block = read_block(relation_name, block_num)
        for tuple_ in block:
            b_value = tuple_[0] if relation_name == 'S' else tuple_[1]
            part = hash_b(b_value, num_partitions)
            buffers[part].append(tuple_)

            if len(buffers[part]) == 8:
                write_block(f"{relation_name}_part_{part}", buffers[part].copy())
                buffers[part].clear()
    
    for part in range(num_partitions):
        if buffers[part]:
            write_block(f"{relation_name}_part_{part}", buffers[part].copy())

def two_pass_join(num_partitions=14):
    partition_relation('R', num_partitions)
    partition_relation('S', num_partitions)

    join_result = []
    for part in range(num_partitions):
        ############# process R partition
        r_part_name = f'R_part_{part}'
        r_tuples = []
        if r_part_name in disk:
            for block_num in range(len(disk[r_part_name])):
                r_tuples.extend(read_block(r_part_name, block_num))
        
        #build hash table
        r_hash = {}
        for t in r_tuples:
            r_hash.setdefault(t[1], []).append(t)
        
        ###############process S partition
        s_part_name = f'S_part_{part}'
        if s_part_name in disk:
            for block_num in range(len(disk[s_part_name])):
                s_block = read_block(s_part_name, block_num)
                for s_tuple in s_block:
                    if s_tuple[0] in r_hash:
                        join_result.extend((r[0], r[1], s_tuple[1]) for r in r_hash[s_tuple[0]])
    
    return join_result


######################################### Part 5: Experiment Implementation #########################################
def reset_experiment():
    global disk_io_reads, disk_io_writes
    if 'R' in disk:
        del disk['R']
    for key in list(disk.keys()):
        if key.startswith(('R_part_', 'S_part_')):
            del disk[key]
    disk_io_reads = 0
    disk_io_writes = 0

def run_experiments():
    """Executes and reports results for both experiments"""
    reset_disk()

    # set seed to ensure reproducibility
    random.seed(407)  
    disk['S'] = generate_S()

    # Experiment 5.1
    with open('experiment5_1.log', 'w') as f:
        with redirect_stdout(f):
            print("================ Experiment 5.1 ================")
            print("Generated S with", len(disk['S']), "blocks")
            
            # Print sample S B-values
            print("Sample S B-values:", [t[0] for t in sum(disk['S'][:3], [])][:3], "...", [t[0] for t in sum(disk['S'][-3:], [])][-3:])
            
            reset_experiment()
            S_B_values = [t[0] for block in disk['S'] for t in block]
            disk['R'] = generate_R_part5_1(S_B_values)
            print("\nGenerated R with", len(disk['R']), "blocks")
            
            join_result = two_pass_join()
            print("\nResults:")
            print("- Total joined tuples:", len(join_result))
            print("")
            print("- Disk I/Os :")
            print("\t\t\t  Read:", f"{disk_io_reads}")
            print("\t\t\t Write:", f"{disk_io_writes}")
            print("---------------------------")
            print("\t\t\t TOTAL:", f"{disk_io_reads + disk_io_writes}")
            
            # Print detailed matches
            join_Bs = list(set(t[1] for t in join_result))

            # select 20 random B-values for detailed matches
            selected_B = random.sample(join_Bs, min(20, len(join_Bs)))
            print("\nDetailed matches for selected B-values:")
            for b in sorted(selected_B):
                matches = [t for t in join_result if t[1] == b]
                print(f"\nB={b} ({len(matches)} matches):")
                for match in matches:
                    print(match)

    # Experiment 5.2
    with open('experiment5_2.log', 'w') as f:
        with redirect_stdout(f):
            print("================ Experiment 5.2 ================")
            reset_experiment()
            disk['R'] = generate_R_part5_2()
            print("\nGenerated R with", len(disk['R']), "blocks")
            
            join_result = two_pass_join()
            print("\nResults:")
            print("- Total joined tuples:", len(join_result))
            print("")
            print("- Disk I/Os :")
            print("\t\t\t  Read:", f"{disk_io_reads}")
            print("\t\t\t Write:", f"{disk_io_writes}")
            print("---------------------------")
            print("\t\t\t TOTAL:", f"{disk_io_reads + disk_io_writes}")
            
            # Print all joined tuples
            print("\nAll joined tuples:")
            for t in join_result:
                print(t)

if __name__ == "__main__":
    run_experiments()