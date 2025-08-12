nodes = []
input_file = '../../data/person-data-v2/test.txt'
sensitive_edge = '/people/person/profession'

with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 3:
            node1, edge, node2 = parts
            if edge == sensitive_edge:
                nodes.append(node2)

print([set(nodes)])