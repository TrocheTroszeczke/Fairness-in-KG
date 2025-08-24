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
input_file = '../../data/person-data-prof-prop_ind/train.txt'
output_file = '../../data/person-data-prof-prop_ind/train.txt'
edges_to_change = ['/people/person/profession1', '/people/person/profession2',
                   '/people/person/profession3', '/people/person/profession4',
                   '/people/person/profession5', '/people/person/profession6',
                   '/people/person/profession7']
mapping = {
    '/people/person/profession1': "/m/0frz0",
    '/people/person/profession2': "/m/0cbd2",
    '/people/person/profession3': "/m/05snw",
    '/people/person/profession4': "/m/0dgd_",
    '/people/person/profession5': "/m/0fj9f",
    '/people/person/profession6': "/m/05t4q",
    '/people/person/profession7': "/m/0kyk",
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
