import types
import json

import pytest

from busie_consumer import BaseConsumer, ConsumedMessageError
from busie_consumer.helpers import ConsumerWrapper

def test_base_consumer_construction(mocker, mock_consumer, kafka_topics, kafka_config):
    mock_subscribe = mocker.patch('busie_consumer.BaseConsumer.subscribe')
    c = BaseConsumer(topics=kafka_topics, config=kafka_config)
    assert isinstance(c, ConsumerWrapper)
    assert c._TOPICS == kafka_topics
    assert c._CONFIG == kafka_config
    mock_subscribe.assert_called_once_with(kafka_topics)

@pytest.mark.parametrize(('kw', 'error_class'), (
    ({'topics': []}, RuntimeError),
    ({}, RuntimeError),
    ({'topics': ['a']}, RuntimeError),
    ({'topics': ['a'], 'config': {}}, RuntimeError),
    ({'topics': ['a'], 'config': {'bootstrap.servers': 'foo'}}, RuntimeError),
    ({'topics': ['a'], 'config': {'group.id': 'bar'}}, RuntimeError)
))
def test_base_consumer_construction_errors(mocker, kw, error_class):
    mock_subscribe = mocker.patch('busie_consumer.BaseConsumer.subscribe')
    with pytest.raises(error_class):
        BaseConsumer(**kw)
    mock_subscribe.assert_not_called()

def test_base_consumer_start(mocker, kafka_config, kafka_topics):
    mocker.patch('busie_consumer.BaseConsumer.__init__', new=lambda *args, **kwargs: None)
    mocker.patch('busie_consumer.BaseConsumer.subscribe')
    mock_poll = mocker.patch('busie_consumer.BaseConsumer.poll')
    mock_close = mocker.patch('busie_consumer.BaseConsumer.close')
    mock_message = mocker.MagicMock()
    mock_poll.side_effect = [None, mock_message]
    mock_message.error.return_value = None
    c = BaseConsumer(topics=kafka_topics, config=kafka_config)
    gen = c.start()
    assert isinstance(gen, types.GeneratorType)
    message = next(gen)
    mock_poll.assert_called_with(1.0)
    assert message == mock_message

    mock_poll.side_effect = None
    mock_poll.return_value.error.return_value = 'some error'
    with pytest.raises(ConsumedMessageError):
        next(gen)
    mock_close.assert_called_once()

def test_base_consumer_graceful_exit(mocker, kafka_config, kafka_topics):
    mocker.patch('busie_consumer.BaseConsumer.__init__', new=lambda *args, **kwargs: None)
    mocker.patch('busie_consumer.BaseConsumer.subscribe')
    mock_close = mocker.patch('busie_consumer.BaseConsumer.close')
    mock_poll = mocker.patch('busie_consumer.BaseConsumer.poll')
    mock_poll.return_value = mocker.MagicMock()
    mock_poll.return_value.error.return_value = None
    c = BaseConsumer(topics=kafka_topics, config=kafka_config)
    for _ in c.start():
        mock_close.assert_not_called()
        # exit after first iteration
        c._exit_gracefully()
    mock_close.assert_called_once()

def test_send_reply(mocker, kafka_topics, kafka_config):
    mocker.patch('busie_consumer.BaseConsumer.__init__', new=lambda *args, **kwargs: None)
    mock_producer = mocker.patch('busie_consumer.Producer')

    c = BaseConsumer()
    c._CONFIG = 'FOO'
    reply = {'topic': 'foo', 'foo': 'bar'}
    key = 'foobar'
    c.send_reply(dict(reply), key)
    mock_producer.assert_called_once_with(c._CONFIG)
    mock_producer.return_value.produce.assert_called_once_with(reply.pop('topic'), json.dumps(reply), key)
    mock_producer.return_value.flush.assert_called_once()

def test_send_reply_error(mocker, kafka_topics, kafka_config):
    """
    Raise if reply is not a dict or if it does not have `topic` entry
    """
    mocker.patch('busie_consumer.BaseConsumer.__init__', new=lambda *args, **kwargs: None)
    c = BaseConsumer()

    with pytest.raises(ValueError):
        c.send_reply(dict(foo='bar'), 'foo')
    
    with pytest.raises(ValueError):
        c.send_reply('yo', 'foo')
