#!/usr/bin/python3

import matplotlib.pyplot as plt
import networkx as nx
import random
import time

from graph_io import GraphIO
from heap import Heap


def random_vertex(vertices, except_vertices=None):
    vertices_cp = vertices.copy()

    for except_vertex in except_vertices:
        try:
            vertices_cp.remove(except_vertex)
        except ValueError:
            continue

    if vertices_cp:
        return random.choice(vertices_cp)

    return None


def initialize_single_source(vertices, source):
    initialized_vertices = {}

    for v_id, vertex in enumerate(vertices):
        if int(vertex) == source:
            initialized_vertices[v_id] = {'distance': 0, 'parent': None}
        else:
            initialized_vertices[v_id] = {'distance': 1000000, 'parent': None}

    return initialized_vertices


def extract_min(vertices):
    min_val = 1000000
    min_id = None

    for key, vertex in vertices.items():
        if vertex['distance'] < min_val:
            min_val = vertex['distance']
            min_id = key

    return min_id


def get_adjacent_vertices(graph, existing_vertices, current_vertex_id):
    adjacent_vertices = []

    for edge in graph:
        if int(edge['source']) not in existing_vertices or int(edge['target']) not in existing_vertices:
            continue
        if int(edge['source']) == int(current_vertex_id) or int(edge['target']) == int(current_vertex_id):
            adjacent_vertices.append(edge)

    return adjacent_vertices


def relax(s_id, t_id, target_weight, initialized_vertices):
    target_weight = initialized_vertices[s_id]['distance'] + target_weight

    if target_weight < initialized_vertices[t_id]['distance']:
        initialized_vertices[t_id]['distance'] = target_weight
        initialized_vertices[t_id]['parent'] = s_id

    return initialized_vertices


def get_shortest_path_and_length(covering_graph, from_id, to_id):
    path = ''
    total_distance = 0

    while to_id != from_id:
        total_distance += covering_graph[to_id]['distance']
        path += str(to_id) + ' '
        to_id = covering_graph[to_id]['parent']

    path += str(to_id)

    return path[::-1], total_distance


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
                self.vertices.append(vertex_id)
                self.adjacencies.append([])

    def get_edges(self):
        edges = []

        for source, nbrs in enumerate(self.adjacencies):
            for target in nbrs:
                edges.append([source, target])

        return edges

    def get_edge_weights(self):
        edge_weights = {}

        for adjacency in self.adjacencies:
            vertices = adjacency.get()
            source = vertices[-1]['id']

            for vertex in vertices[:-1]:
                target = vertex['id']
                weight = vertex['weight']

                edge_weights[(source, target)] = weight

        return edge_weights

    def get_vertex_id(self, vertex_name):
        for i, vertex in enumerate(self.vertices):
            if vertex == vertex_name:
                return i

        raise IndexError('Can\'t find index for vertex "{}"'.format(vertex_name))

    def generate(self):
        start_time = time.process_time()
        vertices_valid_for_nbr = self.vertices.copy()

        for vertex in self.vertices:
            added_vertices = [vertex]

            while len(self.adjacencies[vertex]) < self.neighbours_min:
                random_nbr = random_vertex(vertices_valid_for_nbr, added_vertices)

                if not random_nbr:
                    break

                if vertex in self.adjacencies[random_nbr]:
                    vertices_valid_for_nbr.remove(random_nbr)
                elif len(self.adjacencies[random_nbr]) == self.neighbours_max:
                    vertices_valid_for_nbr.remove(random_nbr)
                else:
                    self.adjacencies[vertex].append(random_nbr)

                added_vertices.append(random_nbr)

        if self.print_to_stdout:
            for adjacency in self.adjacencies:
                print(adjacency)

        end_time = time.process_time()
        self.graph_io.dump(self.is_digraph, self.adjacencies)

        return end_time - start_time

    def load(self):
        self.is_digraph, self.adjacencies = self.graph_io.load()
        self.vertices = list(range(len(self.adjacencies)))

    def draw(self, show_weights):
        if self.is_digraph:
            graph = nx.DiGraph()
        else:
            graph = nx.Graph()

        vertices = self.vertices
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

        vertices = self.adjacencies[current_vertex_id].get()

        for neighbour in vertices[:-1]:
            if neighbour['color'] == 'WHITE':
                self.depth_first_search_visit(neighbour)

    def depth_first_search(self, vertex_name, draw):
        if vertex_name not in self.vertices:
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
                print(adjacency.get())

    def breadth_first_search(self, vertex, draw):
        return

    def get_graph(self):
        heap = []

        for adjacency in self.adjacencies:
            vertices = adjacency.get()
            source = vertices[-1]['id']

            for vertex in vertices[:-1]:
                target = vertex['id']
                weight = vertex['weight']

                node = {'source': source, 'target': target, 'weight': weight}
                reverse_node = {'source': target, 'target': source, 'weight': weight}

                if node not in heap and reverse_node not in heap:
                    heap.append(node)

        return heap

    def search_dijkstra(self, node_from):
        vertices = self.vertices
        graph = self.get_graph()
        initialized_vertices = initialize_single_source(vertices, node_from)

        covering_graph = {}

        while initialized_vertices:
            min_distance_vertex_id = extract_min(initialized_vertices)
            covering_graph[min_distance_vertex_id] = initialized_vertices[min_distance_vertex_id]
            adjacent_vertices = get_adjacent_vertices(graph, initialized_vertices, min_distance_vertex_id)

            for edge in adjacent_vertices:
                if int(edge['source']) == min_distance_vertex_id:
                    target_id = int(edge['target'])
                else:
                    target_id = int(edge['source'])

                initialized_vertices = relax(
                    min_distance_vertex_id,
                    target_id,
                    int(edge['weight']),
                    initialized_vertices
                )

            del initialized_vertices[min_distance_vertex_id]

        return covering_graph

    def get_all_shortest_paths(self):
        vertices = self.vertices
        heap = []

        for from_vertex in vertices:
            total_distance = 0
            covering_graph = self.search_dijkstra(int(from_vertex))

            for to_vertex in vertices:
                if int(to_vertex) == int(from_vertex):
                    continue

                path, distance = get_shortest_path_and_length(covering_graph, int(from_vertex), int(to_vertex))
                total_distance += distance

            heap.append({'id': int(from_vertex), 'total_distance': total_distance})

        heap = Heap().build_min_heap(heap)
        print(heap)
        print('Best place to put gaisrine is at node: {}'.format(heap[0]['id']))

    def approximate_vertex_cover(self):
        cover = []
        edges = self.get_edges()
        return
