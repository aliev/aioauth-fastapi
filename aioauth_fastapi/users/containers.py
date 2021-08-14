from .services import UserService
from .repositories import UserRepository
from dependency_injector import containers, providers


class UserContainer(containers.DeclarativeContainer):

    database = providers.Dependency()

    user_repository = providers.Singleton(UserRepository, database)

    user_service = providers.Singleton(UserService, user_repository=user_repository)
