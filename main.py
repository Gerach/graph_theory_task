#!/usr/bin/python3


import argparse
from graph import Graph


def main():
    parser = argparse.ArgumentParser(description='Generate graphs and search through them.')
    subparsers = parser.add_subparsers(help='commands')

    generate_parser = subparsers.add_parser('generate', help='generate graph from given data')
    generate_parser.add_argument('-v', type=int, metavar='<count>', required=True, help='amount of vertices')
    generate_parser.add_argument('-n', type=int, metavar='<count>', required=True, help='minimum amount of neighbours')
    generate_parser.add_argument('-x', type=int, metavar='<count>', required=True, help='maximum amount of neighbours')

    draw_parser = subparsers.add_parser('draw', help='draw current graph')

    search_parser = subparsers.add_parser('search', help='search in current graph')

    args = parser.parse_args()

    try:
        if args.v and args.n and args.x:
            graph = Graph(args.v, args.n, args.x)
    except AttributeError:
        pass

    # TODO: implement draw

    # TODO: implement search


if __name__ == '__main__':
    main()
