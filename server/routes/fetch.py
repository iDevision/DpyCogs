import difflib
import os.path
from tornado import web
from ._utils import get_file_and_hash

class CogFetcher(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def get(self, hash):
        if not os.path.isfile('server/static/'+hash+'.tar.gz'):
            print("not found")
            self.set_status(404)
            await self.finish({"error":"nothing found"})
            return
        c = self.application.db.cursor()
        c.execute("SELECT name FROM files WHERE hash=?;", (hash,))
        get = c.fetchone()
        if not get:
            print("not in db")
            self.set_status(400)
            await self.finish({"error":"file was not found in the database"})
            return
        get = get[0]
        self.set_status(200)
        hsh, data = get_file_and_hash(hash)
        self.set_header("X-File-Hash", hsh)
        self.set_header("X-Cog-Name", get)
        self.set_header("Content-Type", "application/gzip")
        await self.finish(data)

def setup(app):
    app.add_handlers('.*', [('/fetch/([a-fA-F0-9]{64})\.tar\.gz', CogFetcher)])

