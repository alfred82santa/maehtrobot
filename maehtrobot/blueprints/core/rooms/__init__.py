from maehtrobot.common.blueprints import Blueprint


class RoomBlueprint(Blueprint):

    def create_resources(self):
        from .mappers import RoomMapper
        from .services import RoomService
        from .models import Room

        user_mapper = RoomMapper(model_class=User,
                                 collection=self.get_resource('main_mongo_database')['rooms'])

        self.add_resource('room_mapper', user_mapper)

        user_service = RoomService(mapper=user_mapper)

        self.add_resource('room_service', user_service)
