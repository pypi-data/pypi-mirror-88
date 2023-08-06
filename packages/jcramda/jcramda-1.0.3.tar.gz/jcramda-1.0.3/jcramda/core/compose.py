from functools import reduce, partial
from typing import Callable

__all__ = (
    'compose',
    'pipe',
    'co',
    'partial',
    'break_if',
)


class ComposeBorker:
    def __init__(self, last_result, else_=None):
        self._last_result = last_result
        self._else_f = else_

    @property
    def last_result(self):
        return self._else_f(self._last_result) if callable(self._else_f) else self._last_result



def compose(*fns: Callable):
    assert len(fns) > 1, 'compose must have less two functions.'
    def composed_func(*args, **kwargs):
        f, *funcs = reversed(fns)
        result = f(*args, **kwargs)        
        for func in funcs:       
            if isinstance(result, ComposeBorker):
               return result.last_result
            result = func(result)            
        return result

    return composed_func


co = compose


def pipe(*funcs: Callable):
    return compose(*reversed(funcs))


def break_if(pred, else_=None):
    def borker(result):
        if pred(result):
            return ComposeBorker(result, else_)
        return result
    return borker
