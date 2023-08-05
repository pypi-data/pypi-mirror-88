from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Sequence

from buz import Handler
from buz import Message

K = TypeVar("K", bound=Message)
V = TypeVar("V", bound=Handler)


class Locator(ABC, Generic[K, V]):
    @abstractmethod
    def get(self, message: K) -> Sequence[V]:
        pass
