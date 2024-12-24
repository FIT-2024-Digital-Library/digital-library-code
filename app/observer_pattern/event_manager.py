from app.observer_pattern.observable_event import ObservableEvent
from app.observer_pattern.subscriber_interface import SubscriberInterface


class EventManager:
    def __init__(self):
        self.observations: dict[ObservableEvent, list[SubscriberInterface]] = {}

    def subscribe(self, event: ObservableEvent, subscriber: SubscriberInterface):
        if event not in self.observations.keys():
            self.observations[event] = [subscriber]
        else:
            self.observations[event].append(subscriber)

    def unsubscribe(self, event: ObservableEvent, subscriber: SubscriberInterface):
        if event not in self.observations.keys():
            pass
        else:
            self.observations[event].remove(subscriber)

    def notify_all(self, event, *args):
        if event in self.observations.keys():
            for subscriber in self[]
