#!/usr/bin/python3


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
        graph = Graph(args.v, args.n, args.x)
        if args.t:
            print('Graph generated in {} seconds.'.format(graph.graph_generation_time))

    return


def draw():
    Graph().draw()

    return


def search():
    # TODO: implement search
    return


def test_unit():
    tests = UnitTests()
    tests.test_generator()
    print('Tests passed: {}'.format(tests.tests_passed))
    print('Tests failed: {}'.format(tests.tests_failed))
    return


def read_args():
    parser = argparse.ArgumentParser(description='Generate graphs and search through them.')
    subparsers = parser.add_subparsers(help='commands', dest='command')

    generate_parser = subparsers.add_parser('generate', help='generate graph from given data')
    generate_parser.add_argument('-v', type=int, metavar='<count>', required=True, help='amount of vertices')
    generate_parser.add_argument('-n', type=int, metavar='<count>', required=True, help='minimum amount of neighbours')
    generate_parser.add_argument('-x', type=int, metavar='<count>', required=True, help='maximum amount of neighbours')
    generate_parser.add_argument('-t', action='store_true', help='show generation time')

    draw_parser = subparsers.add_parser('draw', help='draw current graph')

    search_parser = subparsers.add_parser('search', help='search in current graph')

    tests_parser = subparsers.add_parser('test-unit', help='run unit tests')

    args = parser.parse_args()

    if args.command == 'generate':
        generate(args)
        return
    if args.command == 'draw':
        draw()
        return
    if args.command == 'search':
        search()
        return
    if args.command == 'test-unit':
        test_unit()
        return
    if not vars(args):
        parser.parse_args(['-h'])


def main():
    # TODO: implement logger (?)
    read_args()


if __name__ == '__main__':
    main()
