from typing import Optional, Any, TypeVar, Generic, Callable
from abc import ABC, abstractmethod
from jcramda.core import is_none, is_a
from jcramda.base import nth, prop


__all__ = (
    'Just',
    'Nothing',
    'Maybe',
)


_TV = TypeVar('_TV')


class NothingValueError(RuntimeError):
    ...


class Maybe(Generic[_TV], ABC):
    def __new__(cls, *args, **kwargs):
        if cls is Nothing:
            return cls()
        v = nth(0, args)
        empty_f = prop('empty_func', kwargs, default=is_none)
        if is_a(Nothing, v) or empty_f(v):
            return super(Maybe, cls).__new__(Nothing)
        if cls is Maybe:
            cls = Just
        return super(Maybe, cls).__new__(cls, *args, **kwargs)
        

    @abstractmethod
    def get(self) -> _TV: ...

    @abstractmethod
    def empty(self) -> bool: ...

    @abstractmethod
    def get_or(self, or_value: _TV): ...

    @abstractmethod
    def get_else(self, else_func: Callable[[], _TV]): ...

    @abstractmethod
    def map(self, func: Callable[[_TV], Any]): ...

    @abstractmethod
    def flatmap(self, func: Callable[[_TV], Any]): ...

    @staticmethod
    def of(v, empty_func=is_none):
        while is_a_factor(v):
            if v.empty:
                return v
            v = v.get()
        return Just(v, empty_func) if not empty_func(v) else Nothing()


class Nothing(Maybe):

    def get(self):
        raise NothingValueError('a nothing value')

    def empty(self) -> bool:
        return True

    def get_or(self, or_value):
        return or_value

    def get_else(self, else_func):
        return else_func()

    def map(self, func):
        return self

    def flatmap(self, func):
        return self
    
    def __repr__(self):
        return 'Maybe::Nothing'


is_a_factor = is_a(Maybe)
is_nothing = is_a(Nothing)


class Just(Maybe):

    def __init__(self, v: Optional[Any], empty_func=is_none):
        self._value = v
        self._empty_func = empty_func

    @property
    def empty(self) -> bool:
        return self._empty_func(self._value)

    def get(self):
        if self.empty:
            raise NothingValueError('a empty value')
        return self._value

    def get_or(self, or_value):
        return or_value if self.empty else self._value

    def get_else(self, else_func):
        return else_func() if self.empty else self._value

    def map(self, func):
        return Just(func(self._value), empty_func=self._empty_func)

    def flatmap(self, func):
        result = func(self._value)
        while is_a_factor(result):
            result = result.get()
        return Just(result, empty_func=self._empty_func)

    def __repr__(self):
        return f'Maybe::Just({self._value})'
