#!/usr/bin/python3


class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node

    def set_data(self, data):
        self.data = data

    def set_next(self, next_node):
        self.next_node = next_node
