import sys
if sys.version_info > (3, 7) and sys.platform == 'win32':
    import asyncio
    loop = asyncio.SelectorEventLoop()
    asyncio.set_event_loop(loop)
    del loop, asyncio
from tornado import ioloop, web
import importlib
import os
import sqlite3

if not os.path.isdir("server/static"):
    os.mkdir("server/static")

class App(web.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = sqlite3.connect("cog.db")
        cur = self.db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS files (name VARCHAR(32) NOT NULL PRIMARY KEY UNIQUE, hash CHAR(64) NOT NULL UNIQUE);")
        self.db.commit()
        self.d_modules = []
        for route in os.listdir("server/routes"):
            if route.startswith("_"):
                continue
            route = route[:-3]
            modn = f'routes.{route}'
            mod = importlib.import_module(modn)
            mod.setup(self)
            self.d_modules.append(mod)
    
    def start(self):
        self.listen(8080)
        ioloop.IOLoop.current().start()

if __name__ == '__main__':
    app = App()
    app.start()

