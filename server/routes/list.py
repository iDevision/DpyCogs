import difflib
import json
from tornado import web
from ._utils import get_file_and_hash

class FileList(web.RequestHandler):
    async def get(self):
        cursor = self.application.db.cursor()
        cursor.execute("SELECT name, hash FROM files;")
        files = cursor.fetchall()
        data = dict(files)
        sel = self.get_body_argument("query")
        get = difflib.get_close_matches(sel, data.keys())
        if not get:
            self.set_status(404)
            await self.finish({"error":"found nothing by that argument"})
            return
        self.set_status(200)
        self.set_header("Content-Type", "application/json")
        await self.finish(json.dumps({k: data[k] for k in get}))

def setup(app):
    app.add_handlers('.*', [('/search', FileList)])

