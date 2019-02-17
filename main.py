#!/usr/bin/python3


import argparse
from graph import Graph


def read_args():
    parser = argparse.ArgumentParser(description='Generate graphs and search through them.')
    subparsers = parser.add_subparsers(help='commands')

    generate_parser = subparsers.add_parser('generate', help='generate graph from given data')
    generate_parser.add_argument('-v', type=int, metavar='<count>', required=True, help='amount of vertices')
    generate_parser.add_argument('-n', type=int, metavar='<count>', required=True, help='minimum amount of neighbours')
    generate_parser.add_argument('-x', type=int, metavar='<count>', required=True, help='maximum amount of neighbours')
    generate_parser.add_argument('-t', action='store_true', help='show generation time')

    draw_parser = subparsers.add_parser('draw', help='draw current graph')
    draw_parser.add_argument('-m', type=str, metavar='<name>', required=True, help='name of graph')

    search_parser = subparsers.add_parser('search', help='search in current graph')

    args = parser.parse_args()
    if not vars(args):
        parser.parse_args(['-h'])

    return args


def main():
    # TODO: implement logger (?)
    args = read_args()

    try:
        if args.v and args.n and args.x:
            graph = Graph(args.v, args.n, args.x)
            if args.t:
                print('Graph generated in {} seconds.'.format(graph.graph_generation_time))
            return
        elif args.m:
            Graph().draw()
            return
        # TODO: implement search
    except AttributeError:
        pass


if __name__ == '__main__':
    main()
