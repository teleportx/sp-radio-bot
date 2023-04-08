import psycopg2
import config as cfg


class Database:
    def __init__(self, host: str, port: int, user: str, password: str, dbname: str):
        self.connection = None
        self.cursor = None

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname

        self.connect()
        self.connection.close()

    def connect(self):
        self.connection = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password,
                                           host=self.host, port=self.port)
        self.cursor = self.connection.cursor()

    def insert_ban(self, user_id: str, reason: str = 'NULL'):
        self.connect()

        self.cursor.execute(f"INSERT INTO bans(user_id, reason) VALUES ('{user_id}', '{reason}');")
        self.connection.commit()

        self.connection.close()

        cfg.Discord.bans.append(user_id)

    def get_bans(self) -> list:
        self.connect()

        self.cursor.execute(f"SELECT * FROM public.bans;")
        fetched = self.cursor.fetchall()

        self.connection.close()

        return fetched

    def delete_ban(self, user_id: str):
        self.connect()

        self.cursor.execute(f"DELETE FROM public.bans WHERE user_id='{user_id}';")
        self.connection.commit()

        self.connection.close()

        cfg.Discord.bans.pop(cfg.Discord.bans.index(user_id))
