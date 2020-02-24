import argparse
import discord
import os.path
import pathlib
import requests
import sys
from colorama import Fore
from _installer import CogInstaller

__all__ = ['main'] 

parser = argparse.ArgumentParser(prog="cog install", usage="%(prog)s [options]", description="Installs cogs.")
parser.add_argument("-i", "--install-directory", help="Uses this install dir for cogs.", type=pathlib.Path, default=pathlib.Path('./cogs'))
parser.add_argument('-y', '--yes', help="Install without prompting.", action='store_true')
parser.add_argument('-v', '--verbose', help="Print debug information.", action='store_true')
parser.add_argument('-t', '--temp-dir', help="Use a custom cache directory", type=pathlib.Path)

parser.add_argument("cogs", nargs='*', help='List of cogs to install.')

def main(argv):
    args = parser.parse_args(argv)
    idir = args.install_directory
    if not os.path.isdir(idir):
        print(Fore.RED, 'error:', Fore.RESET, ' directory does not exist, double check you are in the correct working directory, or specify a directory with the "-i" flag', sep='')
        sys.exit(1)
    if not args.cogs:
        print(Fore.RED, 'error:', Fore.RESET, ' must install at least one cog', sep='')
        sys.exit(1)
    CogInstaller(args.cogs, install_directory=args.install_directory, prompt=args.yes, custom_temp_dir=args.temp_dir, verbose=args.verbose).install_next()

if __name__ == '__main__':
    main(sys.argv[1:])

