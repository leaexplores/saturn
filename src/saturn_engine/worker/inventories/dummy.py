import dataclasses
from typing import Optional

from . import Inventory
from . import Item


class DummyInventory(Inventory):
    @dataclasses.dataclass
    class Options:
        count: int

    def __init__(self, options: Options, **kwrags: object) -> None:
        self.count = options.count or 1000

    async def next_batch(self, after: Optional[str] = None) -> list[Item]:
        n = int(after) + 1 if after is not None else 0
        n_end = min(n + 100, self.count)
        if n_end == n:
            return []
        return [Item(id=str(i), args={"n": i}) for i in range(n, n_end)]
