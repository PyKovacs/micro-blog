from enum import Enum, auto
from typing import Any, Protocol, Type

from pymongo import MongoClient
from pymongo.cursor import Cursor


class Repositories(Enum):
    USERS = auto()
    ENTRIES = auto()


class DBCrudInterface(Protocol):
    def __init__(self, client: Any, repository: Repositories) -> None:
        pass

    def create(self, **kwargs) -> bool:
        pass

    def read(self, **kwargs) -> Cursor:
        pass

    def update(self, **kwargs) -> bool:
        pass

    def delete(self, **kwargs) -> bool:
        pass


class MongoDBCrud:
    def __init__(self, client: MongoClient, repository: Repositories) -> None:
        if repository == Repositories.ENTRIES:
            self.db = client.techieblog.entries
        elif repository == Repositories.USERS:
            self.db = client.techieblog.users
        else:
            raise ValueError(f'Collection {repository} not found in repositories.')

    def create(self, **kwargs) -> bool:
        document = kwargs.get('document')
        if document:
            result = self.db.insert_one(document)
            if result.acknowledged:
                return True
        return False

    def read(self, **kwargs) -> Cursor:
        document = kwargs.get('document')
        return self.db.find(document)

    def update(self, **kwargs) -> bool:
        return False

    def delete(self, **kwargs) -> bool:
        return False


#####################################################################
#####################################################################

def get_db_crud_users(active_crud: Type[DBCrudInterface], active_client: Any) -> DBCrudInterface:
    return active_crud(active_client, Repositories.USERS)


def get_db_crud_entries(active_crud: Type[DBCrudInterface], active_client: Any) -> DBCrudInterface:
    return active_crud(active_client, Repositories.ENTRIES)
