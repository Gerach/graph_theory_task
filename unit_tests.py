#!/usr/bin/python3


import random
from graph import Graph


class UnitTests:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0

    def test_generator(self):
        for i in range(100):
            vertices = random.randrange(10, 100)
            nbrs_min = random.randrange(1, 6)
            nbrs_max = random.randrange(5, 10)

            graph = Graph(vertices, nbrs_min, nbrs_max)
            if graph.is_whole():
                self.tests_passed += 1
            else:
                self.tests_failed += 1

        return
