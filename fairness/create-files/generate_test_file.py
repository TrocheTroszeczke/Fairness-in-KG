def extract_nodes_and_edges(input_file, nodes_file, edges_file):
    nodes = set()
    edges = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                node1, edge, node2 = parts
                nodes.update([node1, node2])
                edges.add(edge)

    with open(nodes_file, 'w', encoding='utf-8') as nf:
        for node in sorted(nodes):
            nf.write(node + '\n')

    with open(edges_file, 'w', encoding='utf-8') as ef:
        for edge in sorted(edges):
            ef.write(edge + '\n')

def filter_lines_by_nodes_and_edges(source_file, nodes_file, edges_file, output_file):
    with open(nodes_file, 'r', encoding='utf-8') as nf:
        valid_nodes = set(line.strip() for line in nf if line.strip())

    with open(edges_file, 'r', encoding='utf-8') as ef:
        valid_edges = set(line.strip() for line in ef if line.strip())

    filtered_lines = []

    with open(source_file, 'r', encoding='utf-8') as sf:
        for line in sf:
            parts = line.strip().split()
            if len(parts) == 3:
                node1, edge, node2 = parts
                if node1 in valid_nodes and node2 in valid_nodes and edge in valid_edges:
                    filtered_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as out:
        out.writelines(filtered_lines)

# Krok 1: Wyodrębnij nody i krawędzie z bazowego podgrafu
# extract_nodes_and_edges(
#     input_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\person-data_ind\\train.txt',
#     nodes_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\person-data_ind\\tmp\\nodes.txt',
#     edges_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\person-data_ind\\tmp\\edges.txt'
# )

# Krok 2: Przefiltruj nowy plik na podstawie tych nodów i krawędzi
filter_lines_by_nodes_and_edges(
    source_file='/data/FB15k-237/valid.txt',
    nodes_file='/data/person-data_ind/tmp/nodes.txt',
    edges_file='/data/person-data_ind/tmp/edges.txt',
    output_file='/data/person-data_ind/valid.txt'
)
