from plmbr.pipe import Pipe, I
from typing import Any, Iterator, List
import os
from pathlib import Path
from itertools import zip_longest


def path(file):
    return str(
        Path(os.path.dirname(os.path.abspath(__file__))) / file
    )


def check(exp, msg=''):
    assert exp, msg


class validate(Pipe[I, I]):
    def __init__(self, *valids):
        self.valids = valids

    def pipe(self, items: Iterator[I]) -> Iterator[I]:
        res = list(items)
        if len(res) < len(self.valids):
            raise Exception(
                f'Expecting at least {len(self.valids)} items got {res}'
            )

        for valid, item in zip(self.valids, res):
            valid(item)

        return items
