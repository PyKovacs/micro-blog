from typing import Protocol, Any, Dict
from pymongo.collection import Collection
from pymongo.cursor import Cursor


class IDBCrud(Protocol):
    def __init__(self, db_client: Any) -> None:
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
    def __init__(self, db_client: Collection) -> None:
        self.db_client = db_client

    def create(self, **kwargs) -> bool:
        document: Dict[Any, Any] = kwargs.get('document')
        if document:
            result = self.db_client.insert_one(document)
            if result.acknowledged:
                return True
        return False

    def read(self, **kwargs) -> Cursor:
        document: Dict[Any, Any] = kwargs.get('document')
        return self.db_client.find(document)

    def update(self, **kwargs) -> bool:
        pass

    def delete(self, **kwargs) -> bool:
        pass
