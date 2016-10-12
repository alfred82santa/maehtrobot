from maehtrobot.common.exceptions import NotFound
from maehtrobot.common.services import BaseCRUDService, PagingOffset


class RoomService(BaseCRUDService):
    async def load_by_service_room(self, service_id, room_id):
        filter = {'serviceId': service_id, 'roomId': room_id}

        item_list = await self.list(filter, PagingOffset(limit=1))
        if len(item_list) < 1:
            raise NotFound("Service room not found for service '{0}' and room ID '{1}'".format(service_id,
                                                                                               room_id))
        return item_list[0]
