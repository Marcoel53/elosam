import inspect
import uuid


class TransportAdapter:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, topic, callback):
        subscription_id = str(uuid.uuid4())

        self._subscribers.setdefault(topic, {})
        self._subscribers[topic][subscription_id] = callback

        return subscription_id

    def unsubscribe(self, subscription_id):
        for topic in list(self._subscribers):
            subscribers = self._subscribers[topic]

            if subscription_id in subscribers:
                del subscribers[subscription_id]

                if not subscribers:
                    del self._subscribers[topic]

                return True

        return False

    async def publish(self, topic, payload):
        results = []

        for callback in self._subscribers.get(topic, {}).values():
            result = callback(payload)

            if inspect.isawaitable(result):
                result = await result

            results.append(result)

        return results
