from dirty_models.fields import StringIdField, StringField, ModelField, ArrayField, HashMapField
from dirty_models.models import HashMapModel, CamelCaseMeta

from maehtrobot.common.models import PersistentModel, BaseModel


class Personality(BaseModel):
    first_name = StringField()
    last_name = StringField()


class ServiceAccount(HashMapModel, metaclass=CamelCaseMeta):

    user_id = StringIdField(read_only=True)
    """
    User identifier on service.
    """

    first_name = StringField()
    """
    User first name on service.
    """

    last_name = StringField()
    """
    User last name on service.
    """

    user_name = StringIdField(read_only=True)
    """
    User username on service.
    """

    personalities = HashMapField(field_type=ModelField(model_class=Personality))
    """
    Hashmap where keys are room identifier and values are user personality in each one.
    """


class User(PersistentModel):

    user_name = StringIdField(read_only=True)
    """
    User username on platform.
    """

    first_name = StringField()
    """
    User first name on platform.
    """

    last_name = StringField()
    """
    User lasr name on platform.
    """

    service_accounts = HashMapField(field_type=ModelField(model_class=ServiceAccount))
    """
    Hashmap where keys are service identifier and values are user personality in each one.
    """
