#!/usr/bin/python3


class EdgeList:
    def __init__(self):
        self.edges = []

    def append(self, edge):
        if edge[0] == edge[1]:
            return False
        if edge in self.edges:
            return False
        if (edge[1], edge[0]) in self.edges:
            return False
        self.edges.append(edge)

        return True

    def remove(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            return True
        elif (edge[1], edge[0]) in self.edges:
            self.edges.remove((edge[1], edge[0]))
            return True

        return False

    def contains(self, edge):
        if edge in self.edges:
            return True
        elif (edge[1], edge[0]) in self.edges:
            return True

        return False

    def get_vertices(self):
        vertices = []

        for edge in self.edges:
            if edge[0] not in vertices:
                vertices.append(edge[0])

            if edge[1] not in vertices:
                vertices.append(edge[1])

        return vertices

    def count_nbrs(self, vertex):
        count = 0

        for edge in self.edges:
            if vertex in edge:
                count += 1

        return count
