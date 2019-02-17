#!/usr/bin/python3


import matplotlib.pyplot as plt
import networkx as nx
import random
import time

from edge_list import EdgeList
from graph_io import GraphIO


class Graph:
    def __init__(self, vertices_amount=None, neighbours_min=None, neighbours_max=None, print_to_stdout=False):
        self.graph = EdgeList()
        self.graph_io = GraphIO()

        self.vertices_amount = vertices_amount
        self.nbr_min = neighbours_min
        self.nbr_max = neighbours_max

        self.graph_generation_time = None

        if self.vertices_amount and self.nbr_min and self.nbr_max:
            start_time = time.process_time()
            while True:
                self.generate_graph()
                if print_to_stdout:
                    for edge in self.graph.edges:
                        print(edge)
                if self.is_whole():
                    self.graph_io.dump(self.graph)
                    break
            end_time = time.process_time()
            self.graph_generation_time = end_time - start_time
            return

        self.graph = self.graph_io.load()

    def is_whole(self):
        all_vertices = self.graph.get_vertices()
        connected_vertices = [all_vertices[0]]

        for vertex in connected_vertices:
            for edge in self.graph.edges:
                if vertex == edge[0] and edge[1] not in connected_vertices:
                    connected_vertices.append(edge[1])
                elif vertex == edge[1] and edge[0] not in connected_vertices:
                    connected_vertices.append(edge[0])

        if sorted(connected_vertices) == sorted(all_vertices):
            return True

        return False

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
