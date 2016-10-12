from maehtrobot.common.blueprints import Blueprint


class UserBlueprint(Blueprint):

    def create_resources(self):
        from .mappers import UserMapper
        from .services import UserService
        from .models import User

        user_mapper = UserMapper(model_class=User,
                                 collection=self.get_resource('main_mongo_database')['users'])

        self.add_resource('user_mapper', user_mapper)

        user_service = UserService(mapper=user_mapper)

        self.add_resource('user_service', user_service)
