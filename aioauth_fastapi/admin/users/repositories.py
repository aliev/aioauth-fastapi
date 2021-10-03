from aioauth_fastapi.storage.db import Database


class UserAdminRepository:
    def __init__(self, database: Database):
        self.database = database
