import pytest

@pytest.fixture
def mock_consumer(mocker):
    return mocker.patch('busie_consumer.ConsumerWrapper.__init__', new=lambda *args, **kwargs: None)

@pytest.fixture
def kafka_topics():
    return ['topic-a', 'topic-b']

@pytest.fixture
def kafka_config():
    return {'bootstrap.servers': 'localhost:9092', 'group.id': 'foo'}
