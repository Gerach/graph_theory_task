#!/usr/bin/python3

from node import Node


class LinkedList:
    def __init__(self, tail):
        self.head = None
        self.tail = tail

    def insert(self, data):
        new_node = Node(data)
        new_node.set_next(self.head)
        self.head = new_node

    def size(self):
        current = self.head
        count = 0

        while current:
            count += 1
            current = current.get_next()

        return count

    def search(self, data):
        current = self.head

        while current:
            if current.get_data() == data:
                return current
            else:
                current = current.get_next()

        return current

    def delete(self, data):
        current = self.head
        previous = None
        found = False

        while current and not found:
            if current.get_data() == data:
                found = True
            else:
                previous = current
                current = current.get_next()

        if current is None:
            raise ValueError("Data not in list")

        if previous is None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())

    def print(self):
        current = self.head
        all_nodes = []

        if current is None:
            raise ValueError("List is empty")

        while current:
            all_nodes.append(current.get_data())
            current = current.get_next()

        return all_nodes
