import operator as _op
from functools import reduce
from typing import Tuple, Callable, Any, Iterable
from itertools import islice
from ._curry import curry, flip, _


__all__ = (
    'lt', 'le', 'eq', 'ne', 'ge', 'gt', 'not_', 'truth', 'false_', 'is_', 'is_not', 'is_a', 'not_a',
    'not_none', 'is_none', 'between', 'not_in', 'cmp_range', 'clamp', 'dec', 'inc',
    'add', 'sub', 'and_', 'floordiv', 'div', 'inv', 'lshift', 'mod', 'mul', 'matmul',
    'neg', 'or_', 'pos', 'pow_', 'xor', 'concat', 'in_', 'countof', 'delitem', 'getitem',
    'index', 'setitem', 'attr', 'props', 'bind', 'eq_by', 'case', 'indexall',
    'identity', 'when', 'always', 'if_else', 'all_', 'any_', 'all_pass', 'one_pass', 'default_to', 'import_',
    'from_import_as', 'eq_attr', 'eq_prop', 'has_attr', 'try_catch', 'else_to',
)


# Comparison ===========================

eq = curry(_op.eq)
ne = curry(_op.ne)
lt = flip(_op.lt)
le = flip(_op.le)
ge = flip(_op.ge)
gt = flip(_op.gt)


@curry
def eq_by(func, a, b):
    return func(a) == func(b)


@curry
def cmp_range(rng: range, v):
    if v in rng:
        return 0
    return 1 if v >= range.stop else -1


@curry
def between(_min, _max, v):
    """
    _min <= v < _max
    :param _min:
    :param _max:
    :param v:
    :return:
    """
    return cmp_range(range(_min, _max), v) == 0


@curry
def clamp(_min, _max, v):
    result = cmp_range(range(_min, _max), v)
    if result == 0:
        return v
    return _min if result < 0 else _max


# Logical ===============================

not_ = _op.not_
truth = _op.truth
is_ = flip(_op.is_)
is_not = flip(_op.is_not)
is_a = curry(lambda types, obj: isinstance(obj, types))
not_a = curry(lambda types, obj: not isinstance(obj, types))
is_none = is_(None)
not_none = is_not(None)
and_ = curry(lambda a, b: a and b)
or_ = curry(lambda a, b: a or b)



def false_(a):
    return False if a else True

# Math


@curry
def add(a, b):
    return a + b


sub = flip(_op.sub)
dec = sub(1)
inc = add(1)
floordiv = flip(_op.floordiv)
div = flip(_op.truediv)
inv = _op.inv
lshift = flip(_op.lshift)
mod = flip(_op.mod)
mul = curry(_op.mul)
matmul = curry(_op.matmul)
neg = _op.neg
pos = _op.pos
pow_ = flip(_op.pow)
xor = curry(_op.xor)


# Sequence Base
@curry
def concat(a, b, *args):
    return reduce(_op.concat, (a, b, *args))


in_ = curry(_op.contains)
not_in = curry(lambda a, b: b not in a)
countof = flip(_op.countOf)
delitem = flip(_op.delitem)
getitem = flip(_op.getitem)
setitem = curry(lambda d, key, value: _op.setitem(d, key, value))

attr = _op.attrgetter
props = _op.itemgetter
bind = _op.methodcaller


# iadd = flip(_op.iadd)
# iand = flip(_op.iand)
# iconcat = flip(_op.iconcat)
# ifloordiv = flip(_op.ifloordiv)
# ilshift = flip(_op.ilshift)
# imod = flip(_op.imod)
# imul = flip(_op.imul)
# imatmul = flip(_op.imatmul)
# ior = flip(_op.ior)
# ipow = flip(_op.ipow)
# irshift = flip(_op.irshift)
# isub = flip(_op.isub)
# idiv = flip(_op.itruediv)
# ixor = flip(_op.ixor)


# customs ==============================
@curry
def index(x, xs, start=0, end=None):
    try:
        return _op.indexOf(tuple(islice(xs, start, end)), x)
    except ValueError:
        return None


@curry
def indexall(x, xs, start=0, end=None):
    result = []
    for i, v in enumerate(islice(xs, start, end)):
        if v == x:
            result.append(i)
    return iter(result)


@curry
def identity(f, *args, **kw):
    if callable(f):
        return f(*args, **kw)
    return f


def when(*cases: Tuple[Callable, Any], else_=None):
    # noinspection PyBroadException
    def cond(value):
        for f, elem in cases:
            try:
                if f(value):
                    return identity(elem, value)
            except Exception:
                continue
        return identity(else_, value)
    return cond


@curry
def case(cases: dict, v, default=None):
    return identity(cases.get(v), v) or default


@curry
def always(x, _):
    return x


@curry
def if_else(pred, success, failed, value):
    return success(value) if pred(value) else failed(value)


# noinspection PyBroadException
@curry
def try_catch(f, failed, value):
    try:
        return f(value)
    except Exception:
        return failed(value)


@curry
def all_(funcs: Iterable[Callable[[Any], bool]], v):
    return all(f(v) for f in funcs)


@curry
def one_pass(func, iterable) -> bool:
    for x in iterable:
        if func(x):
            return True
    return False


@curry
def all_pass(func, iterable) -> bool:
    for x in iterable:
        if not func(x):
            return False
    return True


@curry
def any_(funcs: Iterable[Callable[[Any], bool]], v):
    for f in funcs:
        if f(v):
            return True
    return False


@curry
def default_to(df, raw):
    return raw or df


@curry
def else_to(else_f, raw, args=(), kwargs={}):
    return raw or else_f(*args, **kwargs)


def import_(module_name, package=None):
    from importlib import import_module
    try:
        return import_module(module_name, package)
    except TypeError:
        return None


@curry
def from_import_as(_name: str, package=None):
    if package:
        name, module_name = (_name, package)
    else:
        name, module_name = _name.rsplit('.', 1)
    super_module = import_(module_name)
    return getattr(super_module, name, None)


@curry
def eq_attr(attr_name, o1, o2):
    attr_getter = _op.attrgetter(attr_name)
    return attr_getter(o1) == attr_getter(o2)


@curry
def eq_prop(prop_name, s1, s2):
    proper = _op.itemgetter(prop_name)
    return proper(s1) == proper(s2)


@curry
def has_attr(attr_name, obj, pred=None):
    if hasattr(obj, attr_name):
        return pred(getattr(obj, attr_name)) if callable(pred) else True
    return False
