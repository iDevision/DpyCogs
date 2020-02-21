import difflib
from tornado import web
from ._utils import get_file_and_hash

class CogFetcher(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def get(self):
        c = self.application.db.cursor()
        sel = self.get_body_argument("query")
        c.execute("SELECT hash FROM files WHERE name=?", (sel,))
        get = c.findone()
        if not get:
            self.set_status(404)
            await self.finish({"error":"found nothing by that argument"})
            return
        self.set_status(200)
        hsh, data = get_file_and_hash(get)
        self.set_header("X-File-Hash", hsh)
        self.set_header("X-File-Name", get)
        self.set_header("Content-Type", "application/gzip")
        await self.finish(data)

def setup(app):
    app.add_handlers('.*', [('/fetch', CogFetcher)])

