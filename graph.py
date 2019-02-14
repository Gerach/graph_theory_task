#!/usr/bin/python3


class Graph:
    def __init__(self, vertices=None, neighbours_min=None, neighbours_max=None):
        self.vertices = vertices
        self.nbr_min = neighbours_min
        self.nbr_max = neighbours_max

        if self.vertices and self.nbr_min and self.nbr_max:
            # generate graph
            # write it to file
            return

        # read graph from file, exception if something goes wrong
