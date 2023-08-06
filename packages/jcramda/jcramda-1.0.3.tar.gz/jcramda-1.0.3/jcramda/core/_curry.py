from abc import ABCMeta
from inspect import signature, Parameter, getfullargspec, FullArgSpec
from functools import wraps, partial
from typing import Callable, List, TypeVar, Union

__all__ = (
    'EmptyParam',
    'curry',
    'flip',
    'is_curried',
    '_',
    'CurriedF',
)
_CRT = TypeVar('_CRT', covariant=True)
CurriedF = Union[Callable[..., _CRT], _CRT]
EmptyParam = Parameter.empty
_ = EmptyParam


def _count_args(spec: FullArgSpec):
    return len(spec.args) + len(spec.kwonlyargs)


def update_args(fn, args, kws):
    old_args = list(args)
    new_kws = kws or {}
    new_args = []
    if isinstance(fn, partial):
        new_args = (old_args.pop(0) if x is _ else x for x in fn.args)
        if fn.keywords:
            new_kws.update(fn.keywords)
        fn = fn.func

    return partial(fn, *new_args, *old_args, **new_kws)


def is_filled(fn: partial, spec):
    return _ not in fn.args and \
        len(spec.args or ()) <= len(fn.args) + len(spec.defaults or ()) and \
        {*spec.kwonlyargs} <= {*fn.keywords, *(spec.kwonlydefaults or ())}


def _need_curried_f(spec):
    return _count_args(spec) > 1 or spec.varargs or spec.varkw


def make_curry(fn, spec):
    @wraps(fn)
    def curried(*args, **kwargs):
        updated_fn = update_args(fn, args, kwargs)
        if is_filled(updated_fn, spec):
            return updated_fn()
        else:
            return wraps(fn)(make_curry(updated_fn, spec))
    curried.__curried__ = True
    return curried


def curry(fn: Callable):
    spec = getfullargspec(fn)
    # 只有一个参数或者没有参数时：返回方法本身
    return make_curry(fn, spec) if _need_curried_f(spec) else fn


def is_curried(f):
    return hasattr(f, '__curried__') and f.__curried__


def flip(f):
    """
    反转一个【双参数】方法的参数位置

    ps: 如果需要修改多参数方法的位置，请使用 `_` 占位符
    :param f:
    :return:
    """
    @curry
    @wraps(f)
    def flipped(a, b, *args, **kwargs):
        return f(b, a, *args, **kwargs)
    flipped.__doc__ = f'**fliped two params on head**\n{flipped.__doc__}'
    return flipped


