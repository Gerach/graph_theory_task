#!/usr/bin/python3


import time
import argparse
from graph import Graph
from unit_tests import UnitTests


def generate(args):
    if args.v and args.n and args.x:
        if args.n >= args.v:
            print('Invalid input data.')
            return
        if args.x >= args.v:
            args.x = args.v - 1
        graph = Graph(args.v, args.n, args.x, args.p, args.d, args.w)
        completion_time = graph.generate()
        if args.t:
            print('Graph generated in {} seconds.'.format(completion_time))


def draw(args):
    graph = Graph()
    graph.load()
    graph.draw(args.w)


def search(args):
    if args.t == 'dfs':
        graph = Graph()
        graph.load()
        graph.depth_first_search(args.v, args.d)
    elif args.t == 'bfs':
        graph = Graph()
        graph.load()
        graph.breadth_first_search(args.v, args.d)
    else:
        print('"{}" search type is not available. Available types:'.format(args.t))
        print('dfs')
        print('bfs')


def search_dijkstra():
    graph = Graph()
    graph.load()
    graph.get_all_shortest_paths()


def vertex_cover(args):
    if args.a:
        graph = Graph()
        graph.load()
        graph.approximate_vertex_cover()
        return
    elif args.f:
        graph = Graph()
        graph.load()
        # brute force
        return
    else:
        print('No algorithm indicated')
        exit(1)


def test_unit(args):
    start_time = time.process_time()
    tests = UnitTests()
    tests.test_generator()
    end_time = time.process_time()
    graph_generation_time = end_time - start_time
    if args.t:
        print('Tests finished in {} seconds'.format(graph_generation_time))
    print('Tests passed: {}'.format(tests.tests_passed))
    print('Tests failed: {}'.format(tests.tests_failed))


def read_args():
    parser = argparse.ArgumentParser(description='Generate graphs and search through them.')
    subparsers = parser.add_subparsers(help='commands', dest='command')

    generate_parser = subparsers.add_parser('generate', help='generate graph from given data')
    generate_parser.add_argument('-v', type=int, metavar='<count>', required=True, help='amount of vertices')
    generate_parser.add_argument('-n', type=int, metavar='<count>', required=True, help='minimum amount of neighbours')
    generate_parser.add_argument('-x', type=int, metavar='<count>', required=True, help='maximum amount of neighbours')
    generate_parser.add_argument('-d', action='store_true', help='generate digraph')
    generate_parser.add_argument('-w', action='store_true', help='generate random weights')
    generate_parser.add_argument('-t', action='store_true', help='show completion time')
    generate_parser.add_argument('-p', action='store_true', help='print graph to stdout')

    draw_parser = subparsers.add_parser('draw', help='draw current graph')
    draw_parser.add_argument('-w', action='store_true', help='display edge weights')

    search_parser = subparsers.add_parser('search', help='search in current graph')
    search_parser.add_argument('-v', type=str, metavar='<vertex>', required=True, help='search from given vertex')
    search_parser.add_argument('-t', type=str, metavar='<type>', required=True, help='search type')
    search_parser.add_argument('-d', action='store_true', help='draw subgraph')

    search_dijkstra_parser = subparsers.add_parser(
        'search-dijkstra',
        help='search all shortest paths in current graph using dijkstra algorithm'
    )

    vertex_cover_parser = subparsers.add_parser('vertex-cover', help='solve vertex cover task')
    vertex_cover_parser.add_argument('-a', action='store_true', help='solve using approximate algorithm')
    vertex_cover_parser.add_argument('-f', action='store_true', help='solve using brute force algorithm')

    tests_parser = subparsers.add_parser('test-unit', help='run unit tests')
    tests_parser.add_argument('-t', action='store_true', help='show completion time')

    args = parser.parse_args()

    if args.command == 'generate':
        generate(args)
        return
    elif args.command == 'draw':
        draw(args)
        return
    elif args.command == 'search':
        search(args)
        return
    elif args.command == 'search-dijkstra':
        search_dijkstra()
        return
    elif args.command == 'vertex-cover':
        vertex_cover(args)
        return
    elif args.command == 'test-unit':
        test_unit(args)
        return
    else:
        parser.parse_args(['-h'])


def main():
    read_args()


if __name__ == '__main__':
    main()
