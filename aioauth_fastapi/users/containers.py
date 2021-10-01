from dependency_injector import containers, providers

from .repositories import UserRepository
from .services import UserService


class UserContainer(containers.DeclarativeContainer):

    database = providers.Dependency()

    user_repository = providers.Singleton(UserRepository, database)

    user_service = providers.Singleton(UserService, user_repository=user_repository)
