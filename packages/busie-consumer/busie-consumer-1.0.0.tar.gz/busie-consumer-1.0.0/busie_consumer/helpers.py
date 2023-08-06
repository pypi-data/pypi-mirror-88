from confluent_kafka import Consumer

class ConsumerWrapper(Consumer):
    """Wraps Consumer to ensure Python implementation"""