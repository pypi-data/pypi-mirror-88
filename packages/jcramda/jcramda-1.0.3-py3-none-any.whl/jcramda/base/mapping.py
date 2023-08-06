"""
Ramda mapping functions
"""
from collections import OrderedDict
from typing import Iterable, Union, Any, Mapping, MutableMapping, Dict, Callable

from jcramda.base.comparison import is_a_dict, is_a_func, is_a_int, is_a_mapper, is_simple_iter
from jcramda.base.sequence import nth
from jcramda.core import (curry, delitem, co, first, foreach, setitem, not_a, not_none,
                          of, all_, truth, is_a, when, eq, fold, mapof, filter_, filter_of)

__all__ = (
    'prop',
    'loc',
    'obj',
    'keys',
    'values',
    'remove',
    'des',
    'map_with_keys',
    'map_update',
    'map_apply',
    'firstitem',
    'firstvalue',
    'firstkey',
    'obj_zip',
    'update_path',
    'key_map',
    'trans_keys',
    'popitem',
    'sorted_by_key',
    'assign',
    'mstrip',
    'strip_none',
    'strip_empty',
    'flat_concat',
    'orderby',
    'ordered_key',
    'ordered_value',
    'pickall',
    'pick',
    'invert',
    'key_tree',
    'keys_eq',
    'itempath',
    'path_eq',
    'where',
    'where_eq',
    'pluck',
    'depop',
    'map_dict',
)

not_dict = not_a(dict)


@curry
def prop(prop_name: str, mapper: Mapping, default=None):
    result = mapper
    for key in prop_name.split('.'):
        result = result.get(key, default)
    return result


@curry
def loc(prop_name, mapper):
    if hasattr(mapper, 'loc'):
        return mapper.loc[prop_name]
    if is_a_int(prop_name):
        prop_name = nth(prop_name)(mapper)
    if hasattr(mapper, 'get'):
        return mapper.get(prop_name)
    return None


@curry
def obj(_keys: Union[str, Iterable[Any]], _values):
    if isinstance(_keys, str):
        return {_keys: _values}
    return dict(zip(_keys, _values))


def keys(mapper: Mapping):
    return mapper.keys()


def values(mapper: Mapping):
    return mapper.values()


def items(mapper: Mapping):
    return mapper.items()


@curry
def des(_keys: Iterable, mapper: Mapping):
    return of(loc(k, mapper) for k in _keys)


@curry
def pickall(_keys: Iterable, mapper: Mapping):
    return dict(zip(_keys, des(_keys, mapper)))


@curry
def pick(_keys: Iterable, mapper: Mapping):
    return dict(
        # filter(None, map(lambda k: (k, loc(k, mapper)) if k in mapper else None, _keys))
        ((k, loc(k, mapper)) for k in _keys if k in mapper)
    )


@curry
def map_update(f, d, v):
    """

    :param f: (v) -> dict
    :param d: dict  updated dict
    :param v: a value
    :return: dict
    """
    d.update(f(v))
    return d


map_with_keys = curry(lambda func, _keys, mapper: map(func, des(_keys, mapper)))

# ( f: (x) -> dict, seqs: [x1, x2 ... xn] ) -> { **f(x1), **f(x2) ... **f(xn) }
map_apply = curry(lambda f, seqs: fold(map_update(f), {}, seqs))


@curry
def remove(_keys: Iterable, mapper: MutableMapping):
    foreach(lambda k: delitem(k, mapper), _keys)
    return mapper


# (d: dict) -> d.values()[0]
firstitem = co(first, items)
firstvalue = co(first, values)
firstkey = co(first, keys)


@curry
def obj_zip(_keys: Iterable, _values: Iterable):
    return dict(zip(_keys, _values))


@curry
def update_path(_path: str, upset, d: MutableMapping):
    paths = tuple(reversed(_path.split('.')))
    new_value = upset(prop(_path, d)) if is_a_func(upset) else upset
    query = fold(lambda r, k: {k: r}, {paths[0]: new_value}, paths[1:])
    d.update(query)
    return d


@curry
def key_map(fn, d: Mapping):
    if not is_a_dict(d):
        return d
    r: Dict = {}
    foreach(lambda k: setitem(r, fn(k), d[k]), d.keys())
    return r


@curry
def trans_keys(key_fn, d, deep=False):
    if is_simple_iter(d):
        result = (trans_keys(key_fn, item, deep) if is_a_dict(item) else item for item in d)
    elif is_a_dict(d):
        result = key_map(key_fn, d)
    else:
        return d

    if deep:
        for key in result:
            result[key] = trans_keys(key_fn, result[key], deep)

    return result


@curry
def popitem(key, d: MutableMapping):
    return d.pop(key)


@curry
def sorted_by_key(key_f, d, reverse=False):
    return OrderedDict(sorted(d.items(), key=key_f, reverse=reverse))


def assign(*args):
    mappers = filter_of(is_a_dict, args)
    if not mappers:
        return {}
    return dict(zip(mapof(keys, mappers), mapof(values, mappers)))


@curry
def mstrip(f, mapper):
    return type(mapper)(filter_(f, mapper.items()))


strip_none = mstrip(lambda item: not_none(item[1]))
strip_empty = mstrip(lambda item: truth(item[1]))


_need_checked_type = is_a((Mapping, list, tuple))


def flat_concat(*args, **kwargs):
    """ 平铺传入的字典
    如果传入参数中有Mapping，则只处理Mapping
    如果传入参数中没有Mapping，则会处理 Sequence[Mapping]
    否则什么都不处理
    :param args: Union[list, dict]
    :param kwargs:
    :return:
    """
    dicts = filter_(all_([is_a_mapper, truth]), of(args))
    lists = of(*filter_(all_([is_simple_iter, truth]), args))

    merged = assign(*dicts, kwargs)
    if merged:
        return dict(
            ((k, flat_concat(v) if _need_checked_type(v) else v) for (k, v) in merged.items() if v)
        )

    return of(flat_concat(x) if _need_checked_type(x) else x for x in lists) \
        or {*filter_(truth, args)}


@curry
def orderby(key_f, d: dict, reverse=False):
    """
    对字典进行排序

    > r = orderby(lambda item: item[1], {'a':3, 'b':1})
    > print(r)
    > OrderedDict([('b', 1), ('a', 3)])

    :param key_f: Tuple[_K, _V] -> Comparable
    :param d: dict
    :param reverse: bool
    :return:
    """
    return OrderedDict(sorted(d.items(), key=key_f, reverse=reverse))


ordered_key = orderby(None)
ordered_value = orderby(lambda x: x[1])


def invert(d: Mapping):
    """
    invert a mapper's key and value
    :param d:
    :return:
    """
    r: Dict = {}
    for k, v in d.items():
        r[v] = of(r[v], k) if v in r else k
    return r


def key_tree(d, prefix=''):
    result = []
    for k, v in when(
            (is_a_mapper, items),
            (is_a(list), enumerate),
            else_=[])(d):
        key_node = f'{prefix}{k}'
        result.append(key_node)
        result += key_tree(v, prefix=f'{key_node}.')
    return result


@curry
def itempath(paths: Union[str, Iterable], mapping):
    r = mapping
    for x in paths.split('.') if isinstance(paths, str) else paths:
        r = when((is_a_mapper, loc(x)), (is_a(Iterable), nth(x)))(r)
        if r is None:
            return None
    return r


@curry
def path_eq(paths: Union[str, Iterable], pred, mapping):
    check = pred if is_a_func(pred) else eq(pred)
    return check(itempath(paths, mapping))


@curry
def pluck(key, mapper: Mapping, *args):
    return tuple(prop(key, d) for d in (mapper, *args))


@curry
def keys_eq(d1, d2) -> bool:
    return keys(d1) == keys(d2)


@curry
def where(pred: Dict[Any, Callable[[Any], bool]], mapping: Mapping) -> bool:
    return all(k in mapping and f(mapping[k]) for (k, f) in pred.items())


@curry
def where_eq(pred, mapping):
    if keys_eq(pred, mapping):
        return where(pred, mapping)
    return False


@curry
def depop(_keys, mapping):
    return tuple(mapping.pop(key) for key in _keys if key in mapping)


@curry
def map_dict(f, mapping):
    return dict(f(k, v) for (k, v) in mapping.items())
