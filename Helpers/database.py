import sqlite3
from Renderable.LogicRenderable import LogicRenderable

class Database:
    client = sqlite3.connect("game_database.db")
    def __init__(self):
        self.cur = self.client.cursor()
        try:
            self.cur.execute(
                "DROP TABLE RENDER_TABLE"
            )
        except Exception as e:
            print(e)
        try:
            self.cur.execute(
                "CREATE TABLE RENDER_TABLE(x, y, z, scale, texture_id, geometry_id, r, g, b, program_id, id)"
            )
        except Exception as e:
            print(e)
        
    def insert_renderable(self, renderable:LogicRenderable):
        self.cur.execute(
            "INSERT INTO RENDER_TABLE VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(renderable.mapped_object)
        )
db = Database()