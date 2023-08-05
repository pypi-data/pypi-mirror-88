"""
Messaging
---------

Low-level messaging interface to connect to various
messaging backends such as Kafka and processing pipelines 
such as spark streaming. 

"""
import json
import traceback
from pykafka import KafkaClient

class MessagingBase(object):
    """
    Base class to handle the interfacing with various messaging
    backends.

    """
    def __init__(self, config, *args, **kwargs):
        """
        Initialize the messaging object

        Args:
            config (dict): Configuration
        """
        self.config = config
        if not isinstance(config, dict):
            raise Exception("Invalid config type. Expecting dict")

    def connect(self):
        """
        Initialize the messsaging backend
        """
        pass

    def produce(self, topic, callback, params):
        """
        Generate and post records into the stream

        Args:
            topic (str): Kafka topic to produce
            callback (method): method to call to generate stream input
            params (dict): Parameters to pass to callback

        Returns:
            None
        """
        raise Exception("Not implemented")

    def consume(self, topic, callback, params):
        """
        Generate and post records into the stream

        Args:
            topic (str): Kafka topic to consume
            callback (method): method to call to consume stream input
            params (dict): Parameters to pass to callback

        Returns:
            None
        """
        raise Exception("Not implemented")

    def stop(self):
        pass

class KafkaMessaging(MessagingBase):
    """

    Implementation of an interface to Kafka

    Example::

        mg = KafkaMessaging({
            "hosts": ["127.0.0.1:9092", "127.0.0.1:9093"],
            "consume_params": {
                "consumer_group": 'testgroup',
                "auto_commit_enable": True,
                "zookeeper_connect": 'localhost:2181'
            })
        mg.connect()
        def handler(params, data):
            ....
        mg.consume('orders', handler, {'region': 'south'})

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'hosts' not in self.config:
            raise Exception("Kafka hosts must be specified")

    def connect(self):
        hosts = self.config.get('hosts')
        hosts = ",".join(hosts)
        self.client = KafkaClient(hosts=hosts)

    def produce(self, topic, callback, params):
        topic = self.client.topics[topic]
        producer_params = self.config.get('produce_params',{})
        with topic.get_sync_producer(**producer_params) as producer:
            for data in callback(params):
                producer.produce(json.dumps(data).encode('utf-8'))



    def consume(self, topic, callback, params):
        topic = self.client.topics[topic]

        consume_params = self.config.get('consume_params',{})
        balanced_consumer = topic.get_balanced_consumer(**consume_params)
        try:
            for message in balanced_consumer:
                if message is not None:
                    try:
                        callback(params, message)
                    except:
                        traceback.print_exc()
        finally:
            balanced_consumer.stop()

