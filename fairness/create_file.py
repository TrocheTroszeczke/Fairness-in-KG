def extend_with_related_lines(source_file, node_file, extended_output_file, edge_output_file):
    nodes = set()
    edges = set()

    # Wczytaj węzły z pliku node_file
    with open(node_file, 'r', encoding='utf-8') as nf:
        for line in nf:
            parts = line.strip().split()
            if len(parts) == 3:
                node1, _, node2 = parts
                nodes.update([node1, node2])

    # Zbierz linie z pliku source_file, które zawierają wierzchołki z node_file
    new_lines = []
    with open(source_file, 'r', encoding='utf-8') as sf:
        for line in sf:
            parts = line.strip().split()
            if len(parts) == 3:
                node1, edge, node2 = parts
                if node1 in nodes or node2 in nodes:
                    new_lines.append(line)
                    edges.add(edge)

    # Dodajemy linie do pliku wynikowego
    with open(extended_output_file, 'a', encoding='utf-8') as out:
        out.writelines(new_lines)

    # Zapisujemy unikalne krawędzie
    with open(edge_output_file, 'w', encoding='utf-8') as ef:
        for edge in sorted(edges):
            ef.write(edge + '\n')


extend_with_related_lines(
    source_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\FB15k-237\\train.txt',
    node_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\FB15k-237-filtered_ind\\tmp\\gender_linie.txt',
    extended_output_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\FB15k-237-filtered_ind\\tmp\\train_v0.txt',
    edge_output_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\FB15k-237-filtered_ind\\tmp\\edges.txt'
)

# extend_with_related_lines(
#     source_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\FB15k-237\\train.txt',
#     node_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\FB15k-237-filtered_ind\\tmp\\train_part0.txt',
#     extended_output_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\FB15k-237-filtered_ind\\tmp\\train_v0.txt',
#     edge_output_file='C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\FB15k-237-filtered_ind\\tmp\\edges.txt'
# )
