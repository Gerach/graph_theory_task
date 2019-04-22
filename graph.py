#!/usr/bin/python3

import matplotlib.pyplot as plt
import networkx as nx
import random
import time

from linked_list import LinkedList
from graph_io import GraphIO
from heap import Heap


def random_vertex(vertices, except_vertices=None):
    vertices_cp = vertices.copy()

    for except_vertex in except_vertices:
        vertices_cp.remove(except_vertex)

    return random.choice(vertices_cp)


class Graph:
    def __init__(self, vertices_amount=None, neighbours_min=None, neighbours_max=None, print_to_stdout=False,
                 is_digraph=False, random_weight=False):
        self.neighbours_min = neighbours_min
        self.neighbours_max = neighbours_max
        self.print_to_stdout = print_to_stdout
        self.is_digraph = is_digraph
        self.adjacencies = []
        self.graph_io = GraphIO()
        self.vertices = []
        self.subgraph = []
        self.heap = []

        if random_weight:
            self.generate_random_weight = vertices_amount * 5
        else:
            self.generate_random_weight = False

        if vertices_amount:
            for vertex_id in range(vertices_amount):
                vertex = {'id': vertex_id, 'weight': 1}
                self.vertices.append(vertex)
                adjacency = LinkedList(vertex)
                adjacency.insert(vertex)
                self.adjacencies.append(adjacency)

    def get_vertices(self):
        all_vertices = []

        for adjacency in self.adjacencies:
            vertices = adjacency.print()
            all_vertices.append(vertices[-1]['id'])

        return all_vertices

    def get_edges(self):
        edges = []

        for adjacency in self.adjacencies:
            targets = []
            vertices = adjacency.print()

            for vertex in vertices[:-1]:
                targets.append(vertex['id'])

            source = vertices[-1]['id']

            for target in targets:
                edges.append([source, target])

        return edges

    def get_edge_weights(self):
        edge_weights = {}

        for adjacency in self.adjacencies:
            vertices = adjacency.print()
            source = vertices[-1]['id']

            for vertex in vertices[:-1]:
                target = vertex['id']
                weight = vertex['weight']

                edge_weights[(source, target)] = weight

        return edge_weights

    def get_vertex_id(self, vertex_name):
        for i, vertex in enumerate(self.get_vertices()):
            if vertex == vertex_name:
                return i

        raise IndexError('Can\'t find index for vertex "{}"'.format(vertex_name))

    def generate(self):
        start_time = time.process_time()

        for i, vertex in enumerate(self.vertices):
            added_neighbours = [vertex]

            if vertex['id'] == 0:
                slice_end = 0
            else:
                slice_end = vertex['id']

            while not (self.adjacencies[i].size() > self.neighbours_min):
                current_neighbours = 0

                for walked_vertex in self.vertices[:slice_end]:
                    neighbour_to_others = self.adjacencies[walked_vertex['id']].search(vertex)
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

                if random_neighbour['id'] < vertex['id']:
                    neighbour_neighbours = self.adjacencies[random_neighbour['id']].size() - 1

                for walked_vertex in self.vertices[:slice_end]:
                    mirrored_neighbour = self.adjacencies[random_neighbour['id']].search(vertex)
                    neighbour_to_others = self.adjacencies[walked_vertex['id']].search(random_neighbour)
                    if neighbour_to_others:
                        neighbour_occurrences += 1

                if (mirrored_neighbour
                        or (neighbour_occurrences + neighbour_neighbours >= self.neighbours_max)):
                    valid_neighbour = False

                added_neighbours.append(random_neighbour)

                if valid_neighbour:
                    random_neighbour_cp = random_neighbour.copy()
                    if self.generate_random_weight:
                        random_weight = random.randrange(self.generate_random_weight)
                    else:
                        random_weight = 1

                    random_neighbour_cp['weight'] = random_weight
                    random_nbr_id = self.get_vertex_id(random_neighbour_cp['id'])
                    self.adjacencies[i].insert(random_neighbour_cp)
                    if not self.is_digraph:
                        vertex_cp = vertex.copy()
                        vertex_cp['weight'] = random_weight
                        self.adjacencies[random_nbr_id].insert(vertex_cp)

        if self.print_to_stdout:
            for adjacency in self.adjacencies:
                print(adjacency.print())

        end_time = time.process_time()
        self.graph_io.dump(self.is_digraph, self.adjacencies)

        return end_time - start_time

    def load(self):
        self.is_digraph, self.adjacencies = self.graph_io.load()

    def draw(self, show_weights):
        if self.is_digraph:
            graph = nx.DiGraph()
        else:
            graph = nx.Graph()

        vertices = self.get_vertices()
        edges = self.get_edges()

        graph.add_nodes_from(vertices)
        graph.add_edges_from(edges)

        pos = nx.spring_layout(graph)

        nx.draw(graph, pos,  with_labels=True)

        if show_weights:
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=self.get_edge_weights())

        plt.show()

    def depth_first_search_visit(self, vertex):
        current_vertex_id = None

        for i, adjacency in enumerate(self.adjacencies):
            if vertex['id'] == adjacency.get_tail()['id']:
                current_vertex_id = i

        for adjacency in self.adjacencies:
            for color in ['WHITE', 'BLACK']:
                colored_vertex = vertex
                colored_vertex['color'] = color
                adjacency.color(colored_vertex, 'BLACK')

        vertices = self.adjacencies[current_vertex_id].print()

        for neighbour in vertices[:-1]:
            if neighbour['color'] == 'WHITE':
                self.depth_first_search_visit(neighbour)

    def depth_first_search(self, vertex_name, draw):
        if vertex_name not in self.get_vertices():
            print('Vertex "{}" not found in graph.'.format(vertex_name))
            return

        for adjacency in self.adjacencies:
            adjacency.color_all('WHITE')

        current_vertex_id = self.get_vertex_id(vertex_name)
        vertex_node = self.adjacencies[current_vertex_id].get_tail()

        self.depth_first_search_visit(vertex_node)

        for adjacency in self.adjacencies:
            tail = adjacency.get_tail()
            if tail['color'] == 'BLACK':
                self.subgraph.append(adjacency)

        if draw:
            self.adjacencies = self.subgraph
            self.draw(False)
        else:
            for adjacency in self.subgraph:
                print(adjacency.print())

    def breadth_first_search(self, vertex, draw):
        return

    def get_heap(self):
        heap = []

        for adjacency in self.adjacencies:
            vertices = adjacency.print()
            source = vertices[-1]['id']

            for vertex in vertices[:-1]:
                target = vertex['id']
                weight = vertex['weight']

                node = {'source': source, 'target': target, 'weight': weight}
                reverse_node = {'source': target, 'target': source, 'weight': weight}

                if node not in heap and reverse_node not in heap:
                    heap.append(node)

        return heap

    def search_dijkstra(self, node_from, node_to):
        graph = self.get_heap()
        heap = Heap().build_min_heap(graph)

        for i in heap:
            print(i)
