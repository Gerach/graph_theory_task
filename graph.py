#!/usr/bin/python3


import matplotlib.pyplot as plt
import networkx as nx
import random


class Graph:
    def __init__(self, vertices_amount=None, neighbours_min=None, neighbours_max=None):
        # self.vertices = ['a', 'b', 'c', 1, 2, 'd', 'e']
        # self.edges = [('a', 'b'), ('a', 'c'), ('a', 1), ('a', 2), ('c', 'd'), (1, 2), (1, 'd'), ('d', 'e')]
        self.vertices = []
        self.edges = []

        self.edge_list = []

        self.vertices_amount = vertices_amount
        self.nbr_min = neighbours_min
        self.nbr_max = neighbours_max

        if self.vertices_amount and self.nbr_min and self.nbr_max:
            self.generate_edge_list()
            # write it to file
            return

        # read graph from file, exception if something goes wrong

    def is_valid_edge(self, st_vertex, nd_vertex):
        if st_vertex == nd_vertex:
            return False
        if (st_vertex, nd_vertex) in self.edge_list:
            return False
        if (nd_vertex, st_vertex) in self.edge_list:
            return False
        return True

    def count_nbr_edges(self, nbr_id):
        nbr_count = 0
        for vertex in self.edge_list:
            if nbr_id in vertex:
                nbr_count += 1
        return nbr_count

    def generate_edge_list(self):
        for vertex_id in range(self.vertices_amount):
            cur_vertex_nbrs = self.count_nbr_edges(vertex_id)
            nbr_amount = random.randrange(self.nbr_min, self.nbr_max + 1) - cur_vertex_nbrs

            for nbr in range(nbr_amount):
                valid_nbr = False
                random_nbr_id = None

                while not valid_nbr:
                    random_nbr_id = random.randrange(self.vertices_amount)
                    valid_nbr = self.is_valid_edge(vertex_id, random_nbr_id)
                if self.count_nbr_edges(random_nbr_id) >= self.nbr_max:
                    continue
                self.edge_list.append((vertex_id, random_nbr_id))

        for edge in self.edge_list:
            print(edge)
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
