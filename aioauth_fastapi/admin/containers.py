from dependency_injector import containers, providers
from .storage import Storage


class AdminContainer(containers.DeclarativeContainer):
    database = providers.Dependency()
    storage = providers.Singleton(Storage, database=database)
