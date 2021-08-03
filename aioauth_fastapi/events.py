async def create_postgresql_connection():
    pass


async def close_postgresql_connection():
    pass


on_startup = [
    create_postgresql_connection,
]
on_shutdown = [
    close_postgresql_connection,
]
