#!/usr/bin/python3


import matplotlib.pyplot as plt
import networkx as nx


class Graph:
    def __init__(self, vertices_amount=None, neighbours_min=None, neighbours_max=None):
        self.vertices = ['a', 'b', 'c', 1, 2, 'd', 'e']
        self.edges = [('a', 'b'), ('a', 'c'), ('a', 1), ('a', 2), ('c', 'd'), (1, 2), (1, 'd'), ('d', 'e')]
        self.vertices_amount = vertices_amount
        self.nbr_min = neighbours_min
        self.nbr_max = neighbours_max

        if self.vertices_amount and self.nbr_min and self.nbr_max:
            # generate graph
            # write it to file
            return

        # read graph from file, exception if something goes wrong

    def generate(self):
        # TODO: implement graph generation
        # TODO: implement graph generation time monitor
        return

    def draw(self):
        graph = nx.Graph()

        graph.add_nodes_from(self.vertices)
        graph.add_edges_from(self.edges)

        nx.draw(graph, with_labels=True)
        plt.show()

    def search(self):
        # TODO: implement searching through graph
        # TODO: implement search time monitor
        return
