from collections import Counter

def remove_some_edges(input_file, output_file, edges_file):
    lines = []
    edges = []

    with open(edges_file, 'r', encoding='utf-8') as f:
        for line in f:
            edge = line.split('\n')[0]
            edges.append(edge)

    # print(edges)

    # 1. Wczytaj linie i zlicz wierzchołki
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            # print(parts[1] in edges)
            if parts[1] in edges:
                lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as out:
        for line in lines:
            out.write(line)
def remove_singleton_node_lines(input_file, output_file):
    lines = []
    node_counter = Counter()

    # 1. Wczytaj linie i zlicz wierzchołki
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                node1, edge, node2 = parts
                lines.append((node1, line))
                lines.append((node2, line))
                node_counter[node1] += 1
                node_counter[node2] += 1

    # 2. Odfiltruj linie, które zawierają wyłącznie wierzchołki o liczności 1
    unique_lines = set()
    for i in range(0, len(lines), 2):
        node1, line = lines[i]
        node2, _ = lines[i+1]
        if not (node_counter[node1] == 1 and node_counter[node2] == 1):
            unique_lines.add(line)

    # 3. Zapisz wynik
    with open(output_file, 'w', encoding='utf-8') as out:
        for line in unique_lines:
            out.write(line)


remove_some_edges(
    input_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\FB15k-237\\train.txt',
    output_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\person-data\\tmp\\train.txt',
    edges_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\person-data\\tmp\\edges.txt'
)

remove_singleton_node_lines(
    input_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\person-data\\tmp\\train.txt',
    output_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\person-data\\train.txt'
)

# remove_some_edges(
#     input_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\FB15k-237\\train.txt',
#     output_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\FB15k-237-filtered_ind\\tmp\\gender_linie.txt',
#     edges_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\FB15k-237-filtered_ind\\tmp\\edges.txt'
# )
