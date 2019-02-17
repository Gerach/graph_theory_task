#!/usr/bin/python3


from edge_list import EdgeList


class GraphIO:
    def __init__(self, filename='graph.data'):
        self.filename = filename

    def dump(self, graph):
        with open(self.filename, 'w') as file:
            for edge in graph.edges:
                file.write('{}\n'.format(str(edge)))

    def load(self):
        graph = EdgeList()
        with open(self.filename, 'r') as file:
            edges_str = file.readlines()
            for edge_str in edges_str:
                st_vertex, nd_vertex = edge_str.strip().strip('(').strip(')').split(', ')
                edge = (int(st_vertex), int(nd_vertex))
                graph.append(edge)

        return graph
