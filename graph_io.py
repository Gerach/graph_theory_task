#!/usr/bin/python3

from linked_list import LinkedList


class GraphIO:
    def __init__(self, filename='graph.data'):
        self.filename = filename

    def dump(self, is_digraph, adjacencies):
        with open(self.filename, 'w') as file:
            if is_digraph:
                file.write('is digraph\n')
            else:
                file.write('\n')
            for adjacency in adjacencies[:-1]:
                vertices = adjacency.print()
                for vertex in vertices[:-1]:
                    file.write('{} {} '.format(str(vertex['name']), str(vertex['weight'])))
                file.write('{} {}\n'.format(str(vertices[-1]['name']), str(vertices[-1]['weight'])))
            vertices = adjacencies[-1].print()
            file.write('{} {}'.format(str(vertices[-1]['name']), str(vertices[-1]['weight'])))

    def load(self):
        adjacencies_formatted = []

        with open(self.filename, 'r') as file:
            lines = file.readlines()
            is_digraph = bool(lines[0].strip())

            for adjacency in lines[1:]:
                vertices = adjacency.strip().split(' ')
                vertices_list = []

                for i in range(int(len(vertices) / 2)):
                    name = vertices[i*2]
                    weight = vertices[i*2 + 1]

                    vertex = {'name': name, 'weight': weight}
                    vertices_list.append(vertex)

                vertices_list.reverse()
                adjacency_formatted = LinkedList(vertices_list[0])
                adjacency_formatted.insert(vertices_list[0])

                for vertex in vertices_list[1:]:
                    adjacency_formatted.insert(vertex)

                adjacencies_formatted.append(adjacency_formatted)

        return is_digraph, adjacencies_formatted
