import signal
import json

from confluent_kafka import Producer

from .helpers import ConsumerWrapper


class ConsumedMessageError(Exception):
    """A consumed message returned an error"""

class BaseConsumer(ConsumerWrapper):

    def __init__(self, topics=None, config=None):
        self._TOPICS = topics
        self._CONFIG = config
        self._RUN = False

        if not hasattr(self._TOPICS, '__iter__') or not len(self._TOPICS):
            raise RuntimeError('`topics` must be an iterable with at least one topic')

        if not isinstance(self._CONFIG, dict):
            raise RuntimeError('`config` must be a `dict` containing Kafka configuration')

        if not all(['bootstrap.servers' in self._CONFIG, 'group.id' in self._CONFIG]):
            raise RuntimeError('`config` must have at `bootstrap.servers` and `group.id`')

        super().__init__(self._CONFIG)

        self.subscribe(self._TOPICS)
        signal.signal(signal.SIGTERM, self._exit_gracefully)

    def start(self):
        self._RUN = True
        try:
            while self._running():
                try:
                    msg = self.poll(1.0)

                    if msg is None:
                        continue

                    elif msg.error():
                        raise ConsumedMessageError(msg.error())

                    else:
                        yield msg
                except KeyboardInterrupt:
                    break
        finally:
            self.close()

    def _running(self):
        return self._RUN is True

    def _exit_gracefully(self, *args):
        _ = args
        self._RUN = False

    def send_reply(self, reply, key):
        if not isinstance(reply, dict) or 'topic' not in reply:
            raise ValueError('`reply` must be a `dict` with a `topic`')

        p = Producer(self._CONFIG)
        p.produce(reply.pop('topic'), json.dumps(reply), key)
        return p.flush()
