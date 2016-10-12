class Filter:
    def __repr__(self):
        return self.__str__()


class FieldFilter(Filter):
    __slots__ = ['field']

    def __init__(self, field):
        self.field = field


class FieldValueFilter(Filter):
    __slots__ = ['value']

    def __init__(self, field, value):
        super(FieldValueFilter, self).__init__(field)
        self.value = value

    def __str__(self):
        return '{}{}{}'.format(self.field, self.operator, self.value)


class EqualFilter(FieldValueFilter):
    opereator = '='


class LessThanFilter(FieldValueFilter):
    opereator = '<'


class LessThanOrEqualFilter(FieldValueFilter):
    opereator = '<='


class GreaterThanFilter(FieldValueFilter):
    opereator = '>'


class GreaterThanOrEqualFilter(FieldValueFilter):
    opereator = '>='


class LikeFilter(FieldValueFilter):
    opereator = '~='


class BetweenFilter(FieldFilter):
    __slots__ = ['min', 'max']

    def __init__(self, field, min, max):
        super(BetweenFilter, self).__init__(field)
        self.min = min
        self.max = max

    def __str__(self):
        return '{}<{}>{}'.format(self.min, self.field, self.max)


class FieldMultiValuesFilter(Filter):
    __slots__ = ['values']

    def __init__(self, field, values):
        super(FieldMultiValuesFilter, self).__init__(field)
        self.values = values

    def __str__(self):
        return '{}{}'.format(self.field,
                             self.operator.format(','.join([str(item)
                                                            for item in self.values])))


class HasFilter(FieldMultiValuesFilter):
    operator = '={{{}}}'


class InFilter(FieldMultiValuesFilter):
    operator = '=[{}]'


class FilterCollection(Filter):
    __slots__ = ['filters']

    def __init__(self, filters):
        self.filters = filters

    def __str__(self):
        return '{}({})'.format(self.operator, ','.join([str(item) for item in self.filters]))


class OrFilter(FilterCollection):
    operator = 'OR'


class AndFilter(FilterCollection):
    operator = 'AND'


class NotFilter(FilterCollection):
    operator = 'NOT'


class XorFilter(FilterCollection):
    operator = 'XOR'
