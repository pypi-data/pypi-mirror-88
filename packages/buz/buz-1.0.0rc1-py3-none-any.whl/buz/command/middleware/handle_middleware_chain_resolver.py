from typing import List

from buz.command import Command, CommandHandler
from buz.command.middleware import HandleMiddleware, HandleCallable
from buz.middleware import MiddlewareChainBuilder


class HandleMiddlewareChainResolver:
    def __init__(self, middlewares: List[HandleMiddleware]):
        self.__middlewares = middlewares
        self.__middleware_chain_builder: MiddlewareChainBuilder[
            HandleCallable, HandleMiddleware
        ] = MiddlewareChainBuilder(middlewares)

    def resolve(self, command: Command, command_handler: CommandHandler, handle: HandleCallable) -> None:
        chain_callable: HandleCallable = self.__middleware_chain_builder.get_chain_callable(
            handle, self.__get_middleware_callable
        )
        chain_callable(command, command_handler)

    def __get_middleware_callable(self, middleware: HandleMiddleware, next_callable: HandleCallable) -> HandleCallable:
        return lambda command, command_handler: middleware.on_handle(command, command_handler, next_callable)
