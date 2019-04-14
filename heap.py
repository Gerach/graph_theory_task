#!/usr/bin/python3

import math

heap = [16, 4, 10, 14, 7, 9, 3, 2, 8, 1]


def parent(node_id):
    return math.ceil((node_id - 2) / 2)


def left(node_id):
    return node_id * 2 + 1


def right(node_id):
    return node_id * 2 + 2


class Heap:
    def __init__(self):
        self.heap_size = None

    def max_heapify(self, graph, node_id):
        """Fixes heap structure to match max conventions

        :param graph:
        :param node_id:
        :return:
        """
        left_id = left(node_id)
        right_id = right(node_id)

        if left_id < self.heap_size and graph[left_id] > graph[node_id]:
            largest_id = left_id
        else:
            largest_id = node_id

        if right_id < self.heap_size and graph[right_id] > graph[largest_id]:
            largest_id = right_id

        if largest_id != node_id:
            graph[node_id], graph[largest_id] = graph[largest_id], graph[node_id]
            graph = self.max_heapify(graph, largest_id)

        return graph

    def build_max_heap(self, graph):
        """Forms maximum priority heap from array

        :param graph:
        :return:
        """
        self.heap_size = len(graph)
        middle_id = math.floor(len(graph) / 2)

        for node_id in range(middle_id, -1, -1):
            graph = self.max_heapify(graph, node_id)

        return graph

    def min_heapify(self, graph, node_id):
        """Fixes heap structure to match min conventions

        :param graph:
        :param node_id:
        :return:
        """
        left_id = left(node_id)
        right_id = right(node_id)

        if left_id < self.heap_size and graph[left_id] < graph[node_id]:
            smallest_id = left_id
        else:
            smallest_id = node_id

        if right_id < self.heap_size and graph[right_id] < graph[smallest_id]:
            smallest_id = right_id

        if smallest_id != node_id:
            graph[node_id], graph[smallest_id] = graph[smallest_id], graph[node_id]
            graph = self.min_heapify(graph, smallest_id)

        return graph

    def build_min_heap(self, graph):
        """Forms minimum priority heap from array

        :param graph:
        :return:
        """
        self.heap_size = len(graph)
        middle_id = math.floor(len(graph) / 2)

        for node_id in range(middle_id, -1, -1):
            graph = self.min_heapify(graph, node_id)

        return graph

    def max_heap_insert(self):
        """Inserts node into heap

        :return:
        """
        return

    def heap_extract_max(self):
        """Gets maximum node from heap

        :return:
        """
        return

    def heap_increase_key(self):
        """Increases node value

        :return:
        """
        return


heap2 = Heap().build_min_heap(heap)
print(heap2)
