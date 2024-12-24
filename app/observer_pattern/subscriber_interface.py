from abc import abstractmethod

from app.observer_pattern.observable_event import ObservableEvent


class SubscriberInterface:
    @abstractmethod
    def notify(self, event: ObservableEvent, *args):
        pass
