import argparse
import discord
import sys

__all__ = ['main', '__version__']
__version__ = '0.0.1'
__doc__ = """DpyCogs v{}
A utility to help install public cogs."""

parser = argparse.ArgumentParser(usage="A utility to help install cogs for discord.py.")
parser.add_argument('-v', '--version', help='Displays version info then exits.', action='store_true')
parser.add_argument('-n', '--new', nargs='?', help='Creates a new bot to use with discord.py and cogs.')

def main(argv):
    args = parser.parse_args(argv)
    if args.version:
        print("""DpyCogs v{}
discord.py v{}
Python v{}.{}.{}""".format(__version__, discord.__version__, *sys.version_info))
        sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])
