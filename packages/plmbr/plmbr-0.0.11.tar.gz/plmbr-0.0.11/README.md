# plmbr

Type safe, reusable pipes to process streams of data.

```python
from typing import Tuple
from plmbr.pipes import *
from plmbr.pipe import Pipe

if __name__ == '__main__':
    double_x: Pipe[Dict, Dict] = to(lambda p: {'x': p['x'] * 2, 'y': p['y']})
    point = Tuple[int, int]
    double_y: Pipe[Dict, Dict] = to(lambda p: {'x': p['x'], 'y': p['y'] * 2})

    (
        zip(range(5), range(5))
        - keep[point](lambda p: p[0] >= 2)
        - to[point, Dict](lambda p: {'x': p[0], 'y': p[1]})
        - json_dumps()
        > save('points.json')
    )

    (
        open('points.json')
        - json_loads()
        + [
            double_x,
            double_y,
        ]
        > log()
    )

    # {'x': 4, 'y': 2}
    # {'x': 6, 'y': 3}
    # {'x': 8, 'y': 4}
    # {'x': 2, 'y': 4}
    # {'x': 3, 'y': 6}
    # {'x': 4, 'y': 8}
```