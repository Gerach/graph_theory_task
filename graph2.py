#!/usr/bin/python3

import matplotlib.pyplot as plt
import networkx as nx
import random
import time

from linked_list import LinkedList
from graph_io import GraphIO


def random_vertex(vertices, except_vertices=None):
    vertices_cp = vertices.copy()

    for except_vertex in except_vertices:
        vertices_cp.remove(except_vertex)

    return random.choice(vertices_cp)


class Graph:
    def __init__(self, vertices_amount=None, neighbours_min=None, neighbours_max=None, print_to_stdout=False,
                 is_digraph=False):
        self.neighbours_min = neighbours_min
        self.neighbours_max = neighbours_max
        self.print_to_stdout = print_to_stdout
        self.is_digraph = is_digraph

        self.vertices = []
        for vertex in list(range(vertices_amount)):
            self.vertices.append({'name': vertex, 'weight': 1})
        self.adjacencies = []

    def get_vertices(self):
        vertices = []

        for vertex in self.vertices:
            vertices.append(vertex['name'])

        return vertices

    def get_edges(self):
        edges = []

        for adjacency in self.adjacencies:
            targets = []
            vertices = adjacency.print()

            for vertex in vertices[:-1]:
                targets.append(vertex['name'])

            source = vertices[-1]['name']

            for target in targets:
                edges.append([source, target])

        return edges

    def generate(self):
        start_time = time.process_time()

        for vertex in self.vertices:
            adjacency = LinkedList(vertex)
            adjacency.insert(vertex)
            added_neighbours = [vertex]

            if vertex['name'] == 0:
                slice_end = 0
            else:
                slice_end = vertex['name']

            while not (adjacency.size() > self.neighbours_min):
                current_neighbours = 0

                for walked_vertex in self.vertices[:slice_end]:
                    neighbour_to_others = self.adjacencies[walked_vertex['name']].search(vertex)
                    if neighbour_to_others:
                        current_neighbours += 1

                current_neighbours += adjacency.size() - 1

                if current_neighbours >= self.neighbours_max:
                    break

                if len(self.vertices) == len(added_neighbours):
                    break

                mirrored_neighbour = False
                neighbour_neighbours = 0
                neighbour_occurrences = 0

                random_neighbour = random_vertex(self.vertices, added_neighbours)
                valid_neighbour = True

                if random_neighbour['name'] < vertex['name']:
                    if not self.is_digraph:
                        mirrored_neighbour = self.adjacencies[random_neighbour['name']].search(vertex)
                    neighbour_neighbours = self.adjacencies[random_neighbour['name']].size() - 1

                for walked_vertex in self.vertices[:slice_end]:
                    neighbour_to_others = self.adjacencies[walked_vertex['name']].search(random_neighbour)
                    if neighbour_to_others:
                        neighbour_occurrences += 1

                if (mirrored_neighbour
                        or (neighbour_occurrences + neighbour_neighbours >= self.neighbours_max)):
                    valid_neighbour = False

                added_neighbours.append(random_neighbour)
                if valid_neighbour:
                    adjacency.insert(random_neighbour)

            self.adjacencies.append(adjacency)

        if self.print_to_stdout:
            for adjacency in self.adjacencies:
                print(adjacency.print())

        end_time = time.process_time()

        return end_time - start_time

    def draw(self):
        graph = nx.Graph()
        vertices = self.get_vertices()
        edges = self.get_edges()

        graph.add_nodes_from(vertices)
        graph.add_edges_from(edges)

        nx.draw(graph, with_labels=True)
        plt.show()
