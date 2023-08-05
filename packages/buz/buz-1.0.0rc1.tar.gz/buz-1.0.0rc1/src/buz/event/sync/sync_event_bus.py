from typing import Collection, List, Optional

from buz.event import Event, EventBus, Subscriber
from buz.event.middleware import (
    PublishMiddleware,
    ConsumeMiddleware,
    PublishMiddlewareChainResolver,
    ConsumeMiddlewareChainResolver,
)
from buz.locator import Locator


class SyncEventBus(EventBus):
    def __init__(
        self,
        locator: Locator[Event, Subscriber],
        publish_middlewares: Optional[List[PublishMiddleware]] = None,
        consume_middlewares: Optional[List[ConsumeMiddleware]] = None,
    ):
        self.__locator = locator
        self.__publish_middleware_chain_resolver = PublishMiddlewareChainResolver(publish_middlewares or [])
        self.__consume_middleware_chain_resolver = ConsumeMiddlewareChainResolver(consume_middlewares or [])

    def publish(self, event: Event) -> None:
        self.__publish_middleware_chain_resolver.resolve(event, self.__perform_publish)

    def __perform_publish(self, event: Event) -> None:
        subscribers = self.__locator.get(event)
        for subscriber in subscribers:
            self.__consume_middleware_chain_resolver.resolve(event, subscriber, self.__perform_consume)

    def __perform_consume(self, event: Event, subscriber: Subscriber) -> None:
        subscriber.consume(event)

    def bulk_publish(self, events: Collection[Event]) -> None:
        for event in events:
            self.publish(event)
