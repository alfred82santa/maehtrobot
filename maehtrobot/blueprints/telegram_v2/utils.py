from aiotelebot.messages import User as TelegramUser

from maehtrobot.blueprints.core.users.models import ServiceAccount, User


def map_telegram_account_to_service_account(account: TelegramUser):
    return ServiceAccount(user_id=account.id, first_name=account.first_name,
                          last_name=account.last_name, user_name=account.username,
                          personalities={})


def map_telegram_account_to_new_user(service_id: str, account: TelegramUser):
    service_account = map_telegram_account_to_service_account(account)

    return User(first_name=account.first_name,
                last_name=account.last_name, user_name=account.username,
                service_accounts={service_id: service_account})
