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
        self.adjacencies = []
        self.graph_io = GraphIO()
        self.vertices = []
        self.subgraph = []

        if vertices_amount:
            for name in list(range(vertices_amount)):
                vertex = {'name': name, 'weight': 1}
                self.vertices.append(vertex)
                adjacency = LinkedList(vertex)
                adjacency.insert(vertex)
                self.adjacencies.append(adjacency)

    def get_vertices(self):
        all_vertices = []

        for adjacency in self.adjacencies:
            vertices = adjacency.print()
            all_vertices.append(vertices[-1]['name'])

        return all_vertices

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

    def get_vertex_id(self, vertex_name):
        for i, vertex in enumerate(self.get_vertices()):
            if vertex == vertex_name:
                return i

        raise IndexError('Can\'t find index for vertex "{}"'.format(vertex_name))

    def generate(self):
        start_time = time.process_time()

        for i, vertex in enumerate(self.vertices):
            added_neighbours = [vertex]

            if vertex['name'] == 0:
                slice_end = 0
            else:
                slice_end = vertex['name']

            while not (self.adjacencies[i].size() > self.neighbours_min):
                current_neighbours = 0

                for walked_vertex in self.vertices[:slice_end]:
                    neighbour_to_others = self.adjacencies[walked_vertex['name']].search(vertex)
                    if neighbour_to_others:
                        current_neighbours += 1

                current_neighbours += self.adjacencies[i].size() - 1

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
                    neighbour_neighbours = self.adjacencies[random_neighbour['name']].size() - 1

                for walked_vertex in self.vertices[:slice_end]:
                    mirrored_neighbour = self.adjacencies[random_neighbour['name']].search(vertex)
                    neighbour_to_others = self.adjacencies[walked_vertex['name']].search(random_neighbour)
                    if neighbour_to_others:
                        neighbour_occurrences += 1

                if (mirrored_neighbour
                        or (neighbour_occurrences + neighbour_neighbours >= self.neighbours_max)):
                    valid_neighbour = False

                added_neighbours.append(random_neighbour)

                if valid_neighbour:
                    random_nbr_id = self.get_vertex_id(random_neighbour['name'])
                    self.adjacencies[i].insert(random_neighbour)
                    if not self.is_digraph:
                        self.adjacencies[random_nbr_id].insert(vertex)

        if self.print_to_stdout:
            for adjacency in self.adjacencies:
                print(adjacency.print())

        end_time = time.process_time()
        self.graph_io.dump(self.is_digraph, self.adjacencies)

        return end_time - start_time

    def load(self):
        self.is_digraph, self.adjacencies = self.graph_io.load()

    def draw(self):
        if self.is_digraph:
            graph = nx.DiGraph()
        else:
            graph = nx.Graph()
        vertices = self.get_vertices()
        edges = self.get_edges()

        graph.add_nodes_from(vertices)
        graph.add_edges_from(edges)

        nx.draw(graph, with_labels=True)
        plt.show()

    def insert_into_subgraph(self, name):
        if name not in self.subgraph:
            self.subgraph.append(name)

    def depth_first_search_visit(self, vertex):
        current_vertex_id = None

        for i, adjacency in enumerate(self.adjacencies):
            if vertex == adjacency.get_tail():
                current_vertex_id = i

        for adjacency in self.adjacencies:
            adjacency.color(vertex, 'BLACK')

        self.adjacencies[current_vertex_id].color(vertex, 'BLACK')
        vertices = self.adjacencies[current_vertex_id].print()

        for neighbour in vertices[:-1]:
            if neighbour['color'] == 'WHITE':
                self.insert_into_subgraph(neighbour['name'])
                self.depth_first_search_visit(neighbour)

    def depth_first_search(self, vertex_name, draw):
        if vertex_name not in self.get_vertices():
            print('Vertex "{}" not found in graph.'.format(vertex_name))
            return

        for adjacency in self.adjacencies:
            adjacency.color_all('WHITE')

        current_vertex_id = self.get_vertex_id(vertex_name)
        vertex_node = self.adjacencies[current_vertex_id].get_tail()

        self.subgraph = [vertex_name]
        self.depth_first_search_visit(vertex_node)

        if draw:
            self.draw()
        else:
            print(' '.join(self.subgraph))

    def breadth_first_search(self, vertex, draw):
        return
