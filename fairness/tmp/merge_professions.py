lines = []
input_file = '../../data/person-data-prof-gender/test.txt'
output_file = '../../data/person-data-prof-gender/test.txt'
e1 = ['/tr/0frz0', '/tr/0np9r', '/tr/04f2zj', '/tr/0q04f', '/tr/0dxtg', '/tr/09jwl', '/tr/05vyk']
e2 = ['/tr/0cbd2', '/tr/0n1h', '/tr/0nbcg', '/tr/05xjb', '/tr/0dz3r', '/tr/0d1pc', '/tr/089fss', '/tr/03sbb']
e3 = ['/tr/05snw', '/tr/04gc2', '/tr/0fnpj', '/tr/099md', '/tr/06wkj0', '/tr/05z96', '/tr/08z956', '/tr/066dv']
e4 = ['/tr/0dgd_', '/tr/0d8qb', '/tr/0mn6', '/tr/0g0vx', '/tr/0gl2ny2', '/tr/0xzm', '/tr/06q2q', '/tr/0htp']
e5 = ['/tr/0fj9f', '/tr/04gf49c', '/tr/0g7nc', '/tr/080ntlp', '/tr/05sxg2', '/tr/0dl08', '/tr/0gbbt', '/tr/064xm0']
e6 = ['/tr/05t4q', '/tr/094hwz', '/tr/09lbv', '/tr/0747nrk', '/tr/0lgw7', '/tr/04pyp5', '/tr/0557q', '/tr/07s467s']
e7 = ['/tr/0kyk', '/tr/0jgxn', '/tr/04s2z', '/tr/047rgpy', '/tr/0d2b38', '/tr/09j9h', '/tr/0d2ww', '/tr/067nv']


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