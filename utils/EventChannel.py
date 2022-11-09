import asyncio


class EventChannel(object):
    def __init__(self):
        self.subscribers = {}

    def unsubscribe(self, event, callback):
        if event is not None or event != ""\
                and event in self.subscribers.keys():
            self.subscribers[event] = list(
                filter(
                    lambda x: x is not callback,
                    self.subscribers[event]
                )
            )

    def subscribe(self, event, callback):
        if not callable(callback):
            raise ValueError("callback must be callable")

        if event is None or event == "":
            raise ValueError("Event cant be empty")

        if event not in self.subscribers.keys():
            self.subscribers[event] = [callback]
        else:
            self.subscribers[event].append(callback)

    async def publish(self, event, args):
        print(event)
        if event in self.subscribers.keys():
            callbacks = self.subscribers[event]
            await asyncio.gather(*[callback(args) for callback in callbacks])

