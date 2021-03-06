# !/usr/bin/env python
import pika
from setting import HOST,PORT,RABBIT_USER,RABBIT_PASSWORD

class mq_consumer:
    def __init__(self):
        credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = HOST, port = 5672,
                                                                            virtual_host = 'raspberry', credentials =credentials,
                                                                            heartbeat_interval = 0))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='file_queue')

    def init_consumer(self,callback_func):
        self.channel.basic_consume(callback_func,
                              queue='file_queue',
                              no_ack=True)
        self.channel.start_consuming()

def test_callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

if __name__ == '__main__':
    mq_obj = mq_consumer()
    mq_obj.init_consumer(test_callback)
