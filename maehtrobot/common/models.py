from dirty_models.fields import StringIdField, IntegerField, ArrayField, ModelField, BlobField
from dirty_models.models import BaseModel as BaseDirtyModel, CamelCaseMeta


class BaseModel(BaseDirtyModel, metaclass=CamelCaseMeta):
    pass


class PersistentModel(BaseModel):
    id = StringIdField(alias=['_id'], read_only=True)
    """
    Entity identifier
    """


class Paging(BaseModel):
    offset = IntegerField(default=0)
    limit = IntegerField(default=100)


class Filter(BaseModel):
    pass


class FieldFilter(Filter):
    field_name = StringIdField()


class FieldValueFilter(Filter):
    value = BlobField()


class EqualFilter(FieldValueFilter):
    pass


class LessThanFilter(FieldValueFilter):
    pass


class LessThanOrEqualFilter(FieldValueFilter):
    pass


class GreaterThanFilter(FieldValueFilter):
    pass


class GreaterThanOrEqualFilter(FieldValueFilter):
    pass


class LikeFilter(FieldValueFilter):
    pass


class Between(FieldFilter):
    min = BlobField()
    max = BlobField()


class FilterCollection(Filter):
    filters = ArrayField(field_type=ModelField(model_class=Filter))


class OrFilter(FilterCollection):
    pass


class AndFilter(FilterCollection):
    pass