#!/usr/bin/python3


import matplotlib.pyplot as plt
import networkx as nx
import random
import time

from edge_list import EdgeList


class Graph:
    def __init__(self, vertices_amount=None, neighbours_min=None, neighbours_max=None):
        self.graph = EdgeList()

        self.vertices_amount = vertices_amount
        self.nbr_min = neighbours_min
        self.nbr_max = neighbours_max

        self.graph_generation_time = None

        if self.vertices_amount and self.nbr_min and self.nbr_max:
            start_time = time.process_time()
            self.generate_graph()
            for edge in self.graph.edges:
                print(edge)
            end_time = time.process_time()
            self.graph_generation_time = end_time - start_time
            # self.draw()
            # dump graph to file
            return

        # read graph from file, exception if something goes wrong

    def generate_graph(self):
        if isinstance(self.graph, EdgeList):
            for vertex in range(self.vertices_amount):
                src_vertex_nbrs = self.graph.count_nbrs(vertex)

                if src_vertex_nbrs >= self.nbr_max:
                    continue

                while True:
                    random_vertex = random.randrange(self.vertices_amount)
                    if random_vertex == vertex:
                        continue
                    dst_vertex_nbrs = self.graph.count_nbrs(random_vertex)
                    if dst_vertex_nbrs < self.nbr_max:
                        break

                generated_edge = (vertex, random_vertex)
                self.graph.append(generated_edge)

    def draw(self):
        graph = nx.Graph()

        graph.add_nodes_from(self.graph.get_vertices())
        graph.add_edges_from(self.graph.edges)

        nx.draw(graph, with_labels=True)
        plt.show()

    def search(self):
        # TODO: implement searching through graph
        # TODO: implement search time monitor
        return
