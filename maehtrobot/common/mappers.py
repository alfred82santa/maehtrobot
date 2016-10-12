from dirty_models.base import Unlocker
from motor.motor_asyncio import AsyncIOMotorCollection

from maehtrobot.common.exceptions import NotFound
from maehtrobot.common.models import PersistentModel
from maehtrobot.common.services import PagingOffset


class MongoMapper:

    def __init__(self, model_class, collection: AsyncIOMotorCollection):
        self.model_class = model_class
        self.collection = collection

    async def load(self, id):
        id = self.map_id_to(id)
        result = await self.collection.find_one(id)

        if result is None:
            raise NotFound("{0} with id '{1}' not found".format(self.model_class.__name__, id))

        return result

    def map_from(self, data):
        return self.model_class(data=data)

    def map_id_to(self, id):
        return id

    async def find(self, filter_list, paging=None):
        cursor = self.collection.find(filter_list)
        if isinstance(paging, PagingOffset):
            if paging.offset:
                cursor.skip(paging.offset)
            if paging.limit:
                cursor.limit(paging.limit)

        result = []
        async for item in cursor:
            result.append(self.map_from(item))

        return result

    async def update(self, model: PersistentModel):
        id = self.map_id_to(model.id)
        data = self.map_update_to(model)

        await self.collection.update({'_id': id}, data)

    def map_update_to(self, model: PersistentModel):
        return model.export_data()

    async def insert(self, model):
        data = self.map_insert_to(model)

        with Unlocker(model):
            model.id = await self.collection.insert(data)

        return model.id

    def map_insert_to(self, model: PersistentModel):
        return model.export_data()

    async def delete(self, id):
        id = self.map_id_to(id)
        await self.collection.remove(id)



