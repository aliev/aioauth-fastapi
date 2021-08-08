from .services import UserService
from .repositories import UserRepository
from dependency_injector import containers, providers


class UserContainer(containers.DeclarativeContainer):

    storage = providers.Dependency()
    redis = providers.Dependency()

    user_repository = providers.Singleton(UserRepository, storage)

    user_service = providers.Singleton(UserService, user_repository)
