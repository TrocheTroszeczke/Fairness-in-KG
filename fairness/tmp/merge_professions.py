lines = []
input_file = '../../data/person-data-prof_ind/test.txt'
output_file = '../../data/person-data-prof_ind/test.txt'
e1 = ['/m/0frz0', '/m/0np9r', '/m/04f2zj', '/m/0q04f', '/m/0dxtg', '/m/09jwl', '/m/05vyk']
e2 = ['/m/0cbd2', '/m/0n1h', '/m/0nbcg', '/m/05xjb', '/m/0dz3r', '/m/0d1pc', '/m/089fss', '/m/03sbb']
e3 = ['/m/05snw', '/m/04gc2', '/m/0fnpj', '/m/099md', '/m/06wkj0', '/m/05z96', '/m/08z956', '/m/066dv']
e4 = ['/m/0dgd_', '/m/0d8qb', '/m/0mn6', '/m/0g0vx', '/m/0gl2ny2', '/m/0xzm', '/m/06q2q', '/m/0htp']
e5 = ['/m/0fj9f', '/m/04gf49c', '/m/0g7nc', '/m/080ntlp', '/m/05sxg2', '/m/0dl08', '/m/0gbbt', '/m/064xm0']
e6 = ['/m/05t4q', '/m/094hwz', '/m/09lbv', '/m/0747nrk', '/m/0lgw7', '/m/04pyp5', '/m/0557q', '/m/07s467s']
e7 = ['/m/0kyk', '/m/0jgxn', '/m/04s2z', '/m/047rgpy', '/m/0d2b38', '/m/09j9h', '/m/0d2ww', '/m/067nv']


nodes1 = []
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 3:
            node1, edge, node2 = parts
            if node1 not in nodes1:
                if node2 in e1 and edge.startswith("/people/person/profession"):
                    edge = "/people/person/profession1"
                    node2 = e1[0]
                elif node2 in e2 and edge.startswith("/people/person/profession"):
                    edge = "/people/person/profession2"
                    node2 = e2[0]
                elif node2 in e3 and edge.startswith("/people/person/profession"):
                    edge = "/people/person/profession3"
                    node2 = e3[0]
                elif node2 in e4 and edge.startswith("/people/person/profession"):
                    edge = "/people/person/profession4"
                    node2 = e4[0]
                elif node2 in e5 and edge.startswith("/people/person/profession"):
                    edge = "/people/person/profession5"
                    node2 = e5[0]
                elif node2 in e6 and edge.startswith("/people/person/profession"):
                    edge = "/people/person/profession6"
                    node2 = e6[0]
                elif node2 in e7 and edge.startswith("/people/person/profession"):
                    edge = "/people/person/profession7"
                    node2 = e7[0]
                nodes1.append(node1)
                lines.append([node1, edge, node2])

with open(output_file, 'w', encoding='utf-8') as out:
    for line in lines:
        out.write("\t".join(line) + "\n")