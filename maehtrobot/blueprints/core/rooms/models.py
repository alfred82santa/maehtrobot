from dirty_models.fields import StringIdField, StringField, ArrayField
from maehtrobot.common.models import PersistentModel


class Assistant(PersistentModel):
    user_id = StringIdField(read_only=True)
    role = StringIdField()


class Room(PersistentModel):
    service_id = StringIdField(read_only=True)
    """
    Service where is room.
    """

    room_id = StringIdField(read_only=True)
    """
    Room identifier on service.
    """

    title = StringField()
    """
    Room title.
    """

    type = StringIdField()
    """
    Room type
    """

    assistants = ArrayField(field_type=StringIdField(), read_only=True)
    """
    Room assistants
    """
