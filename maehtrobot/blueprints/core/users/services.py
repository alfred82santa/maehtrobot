from maehtrobot.common.exceptions import NotFound
from maehtrobot.common.services import BaseCRUDService, PagingOffset


class UserService(BaseCRUDService):


    async def load_by_service_account(self, service_id, user_id):

        filter = {'.'.join(['serviceAccounts', service_id, 'userId']): str(user_id)}

        item_list = await self.list(filter, PagingOffset(limit=1))
        if len(item_list) < 1:
            raise NotFound("Service user account not found for service '{0}' and user ID '{1}'".format(service_id,
                                                                                                       user_id))
        return item_list[0]
