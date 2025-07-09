import networkx as nx
from pyvis.network import Network

triples = []
with open("/data/person-data/train.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 3:
            s, p, o = parts
            triples.append((s, p, o))

G = nx.DiGraph()
for s, p, o in triples:
    G.add_node(s)
    G.add_node(o)
    G.add_edge(s, o, label=p)

net = Network(height="800px", width="100%", directed=True, notebook=True)
net.from_nx(G)

for edge in net.edges:
    edge["title"] = edge["label"]  # wyświetlane po najechaniu
    edge["label"] = edge["label"]  # etykieta na krawędzi

print(f"Liczba wierzchołków: {G.number_of_nodes()}, liczba krawędzi: {G.number_of_edges()}")
net.show("graph.html")
