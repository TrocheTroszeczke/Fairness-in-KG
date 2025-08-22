import random
from collections import Counter

def balance_edges(lines_to_change, edges_to_change, mapping):
    while True:
        # policz wystąpienia e
        counts = Counter(e for _, e, _ in lines_to_change)

        min_count = min(counts.get(e, 0) for e in edges_to_change)
        max_count = max(counts.get(e, 0) for e in edges_to_change)

        if min_count == max_count or min_count + 1 == max_count or min_count - 1 == max_count:
            break

        most_common_e = max(edges_to_change, key=lambda x: counts.get(x, 0))
        least_common_e = min(edges_to_change, key=lambda x: counts.get(x, 0))

        # wybierz losowy indeks do podmiany
        idxs = [i for i, (_, e, _) in enumerate(lines_to_change) if e == most_common_e]
        if not idxs:
            break
        idx = random.choice(idxs)

        # podmień e oraz n2 zgodnie z mappingiem
        n1, _, _ = lines_to_change[idx]
        lines_to_change[idx] = [n1, least_common_e, mapping[least_common_e]]

    return lines_to_change


nodes = []
input_file = '../../data/person-data-tr-v2-prop/valid.txt'
output_file = '../../data/person-data-tr-v2-prop/valid.txt'
edges_to_change = ['/people/person/gender1', '/people/person/gender2',
                   '/people/person/gender3','/people/person/gender4', '/people/person/gender5']
mapping = {
    '/people/person/gender1': "/m/05zppz",
    '/people/person/gender2': "/m/02zsn",
    '/people/person/gender3': "/m/05zppz",
    '/people/person/gender4': "/m/05zppz",
    '/people/person/gender5': "/m/05zppz",
}

lines = []
lines_to_change = []
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 3:
            node1, edge, node2 = parts
            if edge not in edges_to_change:
                lines.append([node1, edge, node2])
            else:
                lines_to_change.append([node1, edge, node2])

print(lines_to_change)
balanced = balance_edges(lines_to_change, edges_to_change, mapping)
print(balanced)

lines_to_save = balanced + lines
random.shuffle(lines_to_save)

with open(output_file, 'w', encoding='utf-8') as out:
    for line in lines_to_save:
        out.write("\t".join(line) + "\n")
