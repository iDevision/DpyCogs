import sys
import discord
import pathlib
import os.path
import requests
import re
from colorama import Fore
import tempfile
import io
import tarfile

file = pathlib.Path(__file__).parent
tempdir = pathlib.Path(tempfile.gettempdir()) / 'dpyc_cache'

with open(file / '__main__.py') as f:
    __version__ = re.findall(r"^__version__ = '([0-9]+\.[0-9]+\.[0-9]+a?)'$", f.read(), flags=re.M)[0]
del f, file,  re

class CogInstaller:
    def __init__(self, cogs, *, install_directory, prompt=False, custom_temp_dir=None, verbose=False):
        self.should_prompt = prompt
        self.custom_temp_dir = pathlib.Path(custom_temp_dir) if custom_temp_dir else None
        self.install_cogs = iter(set(map(str.lower, cogs)))
        self.install_dir = install_directory
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': f'DpyCogs {__version__} Python {".".join(map(str, sys.version_info[:3]))} discord.py {discord.__version__}'})
        self._final = {}

    def create_temporary_directory(self):
        if self.custom_temp_dir:
            if not os.path.isdir(self.custom_temp_dir):
                os.mkdir(self.custom_temp_dir)
            return self.custom_temp_dir
        if not os.path.isdir(tempdir):
            os.mkdir(tempdir)
        return tempdir

    def prompt(self, msg):
        if self.should_prompt:
            return True
        while True:
            yn = input(f'{msg} (Y/n)> ')
            if yn.lower() == 'y':
                return True
            elif yn.lower() == 'n':
                return False

    def unzip_file(self, path):
        with tarfile.open(path, 'r:gz') as tar:
            for member in tar.getmembers():
                if self.verbose:
                    print(member.name + ('/' if member.isdir() else ''))
                tar.extract(member, self.install_dir)

    def finish_install(self):
        for name, hsh in self._final.items():
            fname = self.create_temporary_directory() / (hsh+'.tar.gz')
            assert os.path.exists(fname)
            self.unzip_file(fname)
        print(Fore.GREEN, "Installation complete.", Fore.RESET, sep="")

    def install_next(self):
        try:
            cog = next(self.install_cogs)
        except StopIteration:
            self.finish_install()
            return
        print("fetching ", Fore.GREEN, cog, Fore.RESET, sep='')
        find = self.session.get("http://localhost:8080/search", data={"query": cog})
        if find.status_code == 404:
            print(Fore.RED, 'error:', Fore.RESET, ' cog ', Fore.GREEN, cog, Fore.RESET, ' was not found', sep='')
            return self.install_next()
        real = list(find.json().keys())[0]
        hsh = find.json()[real]
        msg = f'Install {Fore.GREEN}{real}{Fore.RESET}?'
        if not self.prompt(msg):
            return self.install_next()
        path = self.create_temporary_directory()
        _f = path / (hsh+'.tar.gz')
        if os.path.isfile(_f):
            print("using cached:", hsh+'.tar.gz')
            self._final[real] = hsh
            return self.install_next()
        file = self.session.get('http://localhost:8080/fetch/'+hsh+'.tar.gz', stream=True)
        leng = int(file.headers['Content-Length'])
        tot = 0
        print('0%', end='')
        with open(_f, 'wb') as f:
            for chunk in file.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
                tot += len(chunk)
                print(f'\r{tot/leng:.0%}          ', flush=True, end='')
        print()
        self._final[real] = hsh
        self.install_next()



