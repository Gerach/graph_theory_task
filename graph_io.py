#!/usr/bin/python3

from linked_list import LinkedList


class GraphIO:
    def __init__(self, filename='graph.data'):
        self.filename = filename

    def dump(self, is_digraph, adjacencies):
        data = ''

        if is_digraph:
            data += 'is digraph\n'
        else:
            data += '\n'

        for adjacency in adjacencies:
            data += " ".join(str(x) for x in adjacency)
            if adjacency is not adjacencies[-1]:
                data += '\n'

        with open(self.filename, 'w') as file:
            file.write(data)

    def load(self):
        adjacencies_formatted = []

        with open(self.filename, 'r') as file:
            data = file.readlines()

        is_digraph = bool(data[0].strip())

        for nbrs in data[1:]:
            if nbrs.strip():
                nbrs_str = nbrs.strip().split(' ')
                adjacency = [int(x) for x in nbrs_str]
            else:
                adjacency = []
            adjacencies_formatted.append(adjacency)

        return is_digraph, adjacencies_formatted
