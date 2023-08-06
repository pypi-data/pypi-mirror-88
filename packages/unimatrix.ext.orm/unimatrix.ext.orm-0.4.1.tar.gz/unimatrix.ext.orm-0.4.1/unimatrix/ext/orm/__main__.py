"""Specifies the module-level command line interface."""
import argparse

from unimatrix.ext import orm


parser = argparse.ArgumentParser("Database maintenance and debugging")
parser.add_argument('subcommand', help="specify the command to run.")


def main(args):
    if args.subcommand != 'awaitservices':
        raise NotImplementedError
    orm.awaitservices()


if __name__ == '__main__':
    main(parser.parse_args())
