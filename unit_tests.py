#!/usr/bin/python3


import random
from graph2 import Graph


class UnitTests:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0

    # TODO: also test nbr_min and nbr_max
    def test_generator(self):
        for i in range(10000):
            print('Generating graph #{}'.format(i + 1))
            vertices = random.randrange(10, 100)
            nbrs_min = random.randrange(1, 6)
            nbrs_max = random.randrange(5, 10)

            graph = Graph(vertices, nbrs_min, nbrs_max)
            graph.generate()
