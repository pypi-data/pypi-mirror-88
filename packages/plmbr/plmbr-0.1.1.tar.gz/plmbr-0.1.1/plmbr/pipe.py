""" Essential building blocks for a plmbr. """
from abc import ABC, abstractmethod
from typing import Iterable, Iterator, Generic, TypeVar, List, Union, Sequence
from itertools import tee, chain

I = TypeVar('I')
O = TypeVar('O')
T = TypeVar('T')


class _Tap(Generic[I]):
    def __init__(self, items: Iterator[I]):
        self.items = items

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.items)

    def __sub__(self, pipe: 'Pipe[I, O]') -> '_Tap[O]':
        return _Tap(pipe(self))

    def __gt__(self, pipe: 'Pipe[I, O]'):
        g = pipe(self)
        try:
            while True:
                next(g)
        except Exception as e:
            print(e)


class Pipe(ABC, Generic[I, O]):
    """ 
    A base class for all pipes.
    """
    @abstractmethod
    def pipe(self, items: Iterator[I]) -> Iterator[O]: ...

    def __call__(self, items: Iterator[I]) -> Iterator[O]:
        return self.pipe(items)

    def __rsub__(self, items: Union[Sequence[I], Iterable[I]]) -> '_Tap[O]':
        return _Tap(self((i for i in items)))

    def __sub__(self, pipe: 'Pipe[O, T]') -> 'Pipe[I, T]':
        return _PipePipe(self, pipe)


class _PipePipe(Pipe[I, T]):
    def __init__(self, p: Pipe[I, O], q: Pipe[O, T]):
        self.p = p
        self.q = q

    def pipe(self, items: Iterator[I]) -> Iterator[T]:
        return self.q(self.p(items))
