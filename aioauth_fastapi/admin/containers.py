from dependency_injector import containers, providers

from aioauth_fastapi.admin.oauth2.services import Oauth2AdminService

from .oauth2.repositories import Oauth2AdminRepository
from .users.repositories import UserAdminRepository
from .users.services import UserAdminService


class AdminContainer(containers.DeclarativeContainer):

    database = providers.Dependency()

    oauth2_admin_repository = providers.Singleton(
        Oauth2AdminRepository, database=database
    )
    user_admin_repository = providers.Singleton(UserAdminRepository, database=database)

    user_admin_service = providers.Singleton(
        UserAdminService, users_admin_repository=user_admin_repository
    )
    oauth2_admin_service = providers.Singleton(
        Oauth2AdminService, oauth2_admin_repository=oauth2_admin_repository
    )
