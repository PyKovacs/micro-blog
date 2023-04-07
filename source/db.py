from enum import Enum, auto
from typing import Any, Dict, Protocol

from pymongo import MongoClient
from pymongo.cursor import Cursor


class Repositories(Enum):
    USERS = auto()
    ENTRIES = auto()


class DBCrudInterface(Protocol):
    def __init__(self, client: Any, collection: Repositories) -> None:
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
    def __init__(self, client: MongoClient, collection: Repositories) -> None:
        if collection == Repositories.ENTRIES:
            self.db = client.techieblog.entries
        elif collection == Repositories.USERS:
            self.db = client.techieblog.users
        else:
            raise ValueError(f'Collection {collection} not found in repositories.')

    def create(self, **kwargs) -> bool:
        document: Dict[Any, Any] = kwargs.get('document')
        if document:
            result = self.db.insert_one(document)
            if result.acknowledged:
                return True
        return False

    def read(self, **kwargs) -> Cursor:
        document: Dict[Any, Any] = kwargs.get('document')
        return self.db.find(document)

    def update(self, **kwargs) -> bool:
        pass

    def delete(self, **kwargs) -> bool:
        pass


#####################################################################
#####################################################################

def get_db_crud_users(active_crud: DBCrudInterface, active_client: Any) -> DBCrudInterface:
    return active_crud(active_client, Repositories.USERS)


def get_db_crud_entries(active_crud, active_client: Any) -> DBCrudInterface:
    return active_crud(active_client, Repositories.ENTRIES)
