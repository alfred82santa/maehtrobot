import logging
from asyncio.tasks import ensure_future
from logging.handlers import WatchedFileHandler

import os
from aiotelebot import Bot
from aiotelebot.messages import Update
from functools import partial
from service_client.formatters import ServiceClientFormatter

from maehtrobot.blueprints.telegram_v2.utils import map_telegram_account_to_new_user
from maehtrobot.common.blueprints import Blueprint
from maehtrobot.common.exceptions import NotFound

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'logs')


class TelegramV2Blueprint(Blueprint):
    async def bootstrap(self):
        user_service = self.get_resource('core.users.user_service')
        for name, bot in [(name, bot)
                          for name, bot in self._resources.items()
                          if isinstance(bot, Bot)]:
            bot.register_update_processor(partial(user_update_processor, service_id=name, user_service=user_service))

            ensure_future(bot.start_get_updates())


async def user_update_processor(update: Update, service_id, user_service):
    try:
        #: :type: aiotelebot.messages.User
        service_account = update.get_1st_attr_by_path('*.from')
    except AttributeError as ex:
        return

    try:
        user = await user_service.load_by_service_account(service_id,
                                                          service_account.id)
    except NotFound:
        user = map_telegram_account_to_new_user(service_id, service_account)
        await user_service.create(user)
