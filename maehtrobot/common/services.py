

class BasePaging:

    __slots__ = []


class PagingOffset(BasePaging):

    __slots__ = ['offset', 'limit']

    def __init__(self, offset=0, limit=100):
        self.offset = offset
        self.limit = limit


class PagingPage(BasePaging):

    __slots__ = ['page', 'limit']

    def __init__(self, page=0, page_size=100):
        self.page = page
        self.page_size = page_size

class BaseService:
    pass


class BaseMapperService(BaseService):
    def __init__(self, mapper):
        self.mapper = mapper


class BaseCRUDService(BaseMapperService):

    async def load(self, id):
        return await self.mapper.load(id)

    async def create(self, model):
        return await self.mapper.insert(model)

    async def update(self, model):
        return await self.mapper.update(model)

    async def delete(self, id):
        return await self.mapper.delete(id)

    async def list(self, filter_list, paging):
        return await self.mapper.find(filter_list, paging)