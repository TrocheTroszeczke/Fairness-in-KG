def get_edges(source_file, keyword, edge_output_file):
    edges = []

    # Wczytaj węzły z pliku node_file
    with open(source_file, 'r', encoding='utf-8') as nf:
        for line in nf:
            if keyword in line:
                _, edgeName, _ = line.strip().split()
                edges.append(edgeName)

    edges = list(set(edges))
    print(edges)

    with open(edge_output_file, 'a', encoding='utf-8') as out:
        for edge in edges:
            out.writelines(f'{edge}\n')

get_edges("/data/FB15k-237/train.txt", "/people/",
          "C:\\Users\\Ania\\Desktop\\fairness-in-kg\\sialp-fork\\data\\person-data\\tmp\\edges.txt")