import dataclasses
from typing import Any
from typing import ClassVar
from typing import Optional


@dataclasses.dataclass(eq=False)
class Resource:
    data: Any

    typename: ClassVar[Optional[str]] = None

    @classmethod
    def _typename(cls) -> str:
        return cls.typename or cls.__name__