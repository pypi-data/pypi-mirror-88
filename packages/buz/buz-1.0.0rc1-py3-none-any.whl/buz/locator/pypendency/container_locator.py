from collections import defaultdict
from typing import List, DefaultDict, Generic, TypeVar

from pypendency.container import AbstractContainer

from buz import Handler
from buz import Message
from buz.locator import Locator
from buz.locator.pypendency import HandlerAlreadyRegisteredException
from buz.locator.pypendency import HandlerNotFoundException
from buz.locator.pypendency import HandlerNotRegisteredException

K = TypeVar("K", bound=Message)
V = TypeVar("V", bound=Handler)


class ContainerLocator(Locator, Generic[K, V]):
    CHECK_MODE_REGISTER_TIME = "register"
    CHECK_MODE_GET_TIME = "get"

    def __init__(self, container: AbstractContainer, check_mode: str = CHECK_MODE_REGISTER_TIME) -> None:
        self.__container = container
        self.__check_mode = check_mode
        self.__mapping: DefaultDict[str, List[str]] = defaultdict(lambda: [])
        self.__handler_ids: List[str] = []
        self.__handlers_resolved = False

    def register(self, handler_id: str) -> None:
        self.__guard_handler_already_registered(handler_id)
        if self.__check_mode == self.CHECK_MODE_REGISTER_TIME:
            self.__guard_handler_not_found(handler_id)
        self.__handler_ids.append(handler_id)
        self.__handlers_resolved = False

    def __guard_handler_already_registered(self, handler_id: str) -> None:
        if handler_id in self.__handler_ids:
            raise HandlerAlreadyRegisteredException(handler_id)

    def __guard_handler_not_found(self, handler_id: str) -> None:
        if not self.__container.has(handler_id):
            raise HandlerNotFoundException(handler_id)

    def unregister(self, handler_id: str) -> None:
        self.__guard_handler_not_registered(handler_id)
        self.__handler_ids.remove(handler_id)
        self.__handlers_resolved = False

    def __guard_handler_not_registered(self, handler_id: str) -> None:
        if handler_id not in self.__handler_ids:
            raise HandlerNotRegisteredException(handler_id)

    def get(self, message: K) -> List[V]:
        if not self.__handlers_resolved:
            self.__resolve_handlers()
        handler_ids = self.__mapping.get(message.fqn(), [])
        return [self.__container.get(handler_id) for handler_id in handler_ids]

    def __resolve_handlers(self) -> None:
        self.__mapping = defaultdict(lambda: [])
        for handler_id in self.__handler_ids:
            if self.__check_mode == self.CHECK_MODE_GET_TIME:
                self.__guard_handler_not_found(handler_id)
            handler: V = self.__container.get(handler_id)
            message_fqn = handler.handles().fqn()
            self.__mapping[message_fqn].append(handler_id)
        self.__handlers_resolved = True
