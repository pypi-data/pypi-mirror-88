from enum import Enum

from jcramda.core import curry, co, attr, bind, index, is_a
from jcramda.base.sequence import find_true, nth
from jcramda.base.comparison import attr_eq

__all__ = (
    'is_enum',
    'members',
    'valueof',
    'nameof',
    'e_index_of',
    'e_index_by',
    'enum_name',
    'enum_value',
)

is_enum = is_a(Enum)


members = co(
    bind('values'),
    attr('__members__'),
)


@curry
def valueof(v, e):
    return co(
        find_true(attr_eq('value', v)),
        members,
    )(e)


@curry
def nameof(name, e):
    return co(
        find_true(attr_eq('name', name)),
        members,
    )(e)


# (member, Enum) -> int
e_index_of = curry(lambda m, e: index(m, members(e)))

e_index_by = curry(lambda i, e: nth(i)(members(e)))


def enum_name(e):
    return e.name if is_enum(e) else e


def enum_value(e):
    return e.value if is_enum(e) else e
