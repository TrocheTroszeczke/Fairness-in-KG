import random
from collections import Counter

def balance_edges(lines_to_change, edges_to_change, mapping, target_ratios):
    total = len(lines_to_change)
    # policz, ile docelowo powinno przypadać na każdy edge
    target_counts = {
        e: int(total * target_ratios[e]) for e in edges_to_change
    }

    # czasem zaokrąglenia nie dadzą dokładnie total
    # wyrównaj nadmiar/niedobór
    diff = total - sum(target_counts.values())
    if diff != 0:
        # popraw losowo lub wg największego niedoboru
        for e in edges_to_change:
            if diff == 0:
                break
            target_counts[e] += 1
            diff -= 1

    # iteracyjnie zmieniaj nadmiarowe krawędzie na brakujące
    while True:
        counts = Counter(e for _, e, _ in lines_to_change)

        # sprawdź, czy wszystkie wartości są zgodne z targetem
        if all(counts.get(e, 0) == target_counts[e] for e in edges_to_change):
            break

        # znajdź edge z nadmiarem i edge z niedoborem
        overfull = [e for e in edges_to_change if counts.get(e, 0) > target_counts[e]]
        underfull = [e for e in edges_to_change if counts.get(e, 0) < target_counts[e]]

        if not overfull or not underfull:
            break

        most_common_e = random.choice(overfull)
        least_common_e = random.choice(underfull)

        # wybierz losowy element z most_common_e
        idxs = [i for i, (_, e, _) in enumerate(lines_to_change) if e == most_common_e]
        if not idxs:
            break
        idx = random.choice(idxs)

        # podmień e i n2
        n1, _, _ = lines_to_change[idx]
        lines_to_change[idx] = [n1, least_common_e, mapping[least_common_e]]

    return lines_to_change




nodes = []
input_file = '../../data/person-data-tr-v2-prop/valid.txt'
output_file = '../../data/person-data-tr-v2-prop/valid.txt'
edges_to_change = ['/people/person/gender1', '/people/person/gender2']
mapping = {
    '/people/person/gender1': "/m/02zsn",
    '/people/person/gender2': "/m/02zsn"
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
target_ratios = {
    '/people/person/gender1': 0.6,
    '/people/person/gender2': 0.4
}

balanced = balance_edges(lines_to_change, edges_to_change, mapping, target_ratios)

print(balanced)

lines_to_save = balanced + lines
random.shuffle(lines_to_save)

with open(output_file, 'w', encoding='utf-8') as out:
    for line in lines_to_save:
        out.write("\t".join(line) + "\n")
