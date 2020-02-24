import argparse
import discord
import sys
import os
from colorama import Fore, init as colorama_init
colorama_init()

from install import main as install_main

__all__ = ['main', '__version__']
__version__ = '0.0.1'
__doc__ = """DpyCogs v{}
A utility to help install public cogs."""

BOT = """
import os
from discord.ext import commands

class {0}(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!")
        for cog in os.listdir("cogs"):
            cog = cog[:-3]
            self.load_extension("cogs.{{}}".format(cog))

token = "insert your token here"
if __name__ == "__main__":
    {0}().run(token)
"""

parser = argparse.ArgumentParser(description="A utility to help install cogs for discord.py.", usage='%(prog)s [options]')
parser.add_argument('-v', '--version', help='Displays version info then exits.', action='store_true')
parser.add_argument('-n', '--new', nargs='?', help='Creates a new bot to use with discord.py and cogs.', type=str)

parser.add_argument('method', nargs='...', help='What to do.')

METHODS = {
        "install": install_main
}

def create_new(name="bot"):
    with open(name+'.py', 'x') as f:
        f.write(BOT)
    os.mkdir("cogs")
    print("Done.")
    sys.exit(0)

def main(argv):
    args = parser.parse_args(argv)
    if args.version:
        print("""DpyCogs v{}
discord.py v{}
Python v{}.{}.{}""".format(__version__, discord.__version__, *sys.version_info))
        sys.exit(0)
    if args.new is not None:
        create_new(args.new)
    method = METHODS[args.method[0]]
    method(args.method[1:])

if __name__ == '__main__':
    main(sys.argv[1:])
