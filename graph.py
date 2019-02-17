#!/usr/bin/python3


import matplotlib.pyplot as plt
import networkx as nx
import random
import time


def is_valid_edge(st_vertex, nd_vertex, edge_list):
    if st_vertex == nd_vertex:
        return False
    if (st_vertex, nd_vertex) in edge_list:
        return False
    if (nd_vertex, st_vertex) in edge_list:
        return False
    return True


def count_nbrs(nbr_id, edge_list):
    nbr_count = 0
    for vertex in edge_list:
        if nbr_id in vertex:
            nbr_count += 1
    return nbr_count


def edge_list_is_valid(vertices_amount, graph):
    for vertex_id in range(vertices_amount):
        if vertex_id not in [v for edge in graph for v in edge]:
            return False
    return True


class Graph:
    def __init__(self, vertices_amount=None, neighbours_min=None, neighbours_max=None):
        # self.vertices = ['a', 'b', 'c', 1, 2, 'd', 'e']
        # self.edges = [('a', 'b'), ('a', 'c'), ('a', 1), ('a', 2), ('c', 'd'), (1, 2), (1, 'd'), ('d', 'e')]

        self.edge_list = []

        self.vertices_amount = vertices_amount
        self.nbr_min = neighbours_min
        self.nbr_max = neighbours_max

        self.graph_generation_time = None

        if self.vertices_amount and self.nbr_min and self.nbr_max:
            start_time = time.process_time()
            while True:
                self.edge_list = self.generate_edge_list()
                if edge_list_is_valid(self.vertices_amount, self.edge_list):
                    break
            end_time = time.process_time()
            self.graph_generation_time = end_time - start_time
            # dump graph to file
            return

        # read graph from file, exception if something goes wrong

    def generate_edge_list(self):
        edge_list = []

        for vertex_id in range(self.vertices_amount):
            cur_vertex_nbrs = count_nbrs(vertex_id, edge_list)
            nbr_amount = random.randrange(self.nbr_min, self.nbr_max + 1) - cur_vertex_nbrs

            for nbr in range(nbr_amount):
                valid_nbr = False
                random_nbr_id = None

                while not valid_nbr:
                    random_nbr_id = random.randrange(self.vertices_amount)
                    valid_nbr = is_valid_edge(vertex_id, random_nbr_id, edge_list)

                if count_nbrs(random_nbr_id, edge_list) >= self.nbr_max:
                    continue
                edge_list.append((vertex_id, random_nbr_id))

        for edge in edge_list:
            print(edge)

        print()

        return edge_list

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
