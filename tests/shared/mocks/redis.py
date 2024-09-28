from uuid import UUID
from asyncpg.pgproto.pgproto import UUID as _UUID


class RedisMock:
    database = {}

    async def get(self, name):
        return RedisMock.database.get(name, None)

    async def set(self, name, value, ex):
        RedisMock.database[name] = value
        return True

    async def ttl(self, name):
        return 100

    async def delete(self, name):
        return RedisMock.database.pop(name, None)
