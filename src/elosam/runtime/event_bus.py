class EventBus:
    def __init__(self):
        self._events = []

    def publish(self, event, *args):
        self._events.append(event)

    def subscribe(self, event, fn):
        pass

    def all(self):
        return list(self._events)
