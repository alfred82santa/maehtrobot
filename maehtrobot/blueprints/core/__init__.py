from maehtrobot.common.blueprints import Blueprint


class CoreBlueprint(Blueprint):

    def create_children(self):
        from .users import UserBlueprint

        user_bp = UserBlueprint()
        user_bp.parent = self
        self.add_child('users', user_bp)

        user_bp.create_resources()
        user_bp.create_children()

        print('eeooo')



