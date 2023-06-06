import json
import pika

params = pika.URLParameters('amqps://kydwwrjg:q5Rgo2DMjVir5qRnW_q1XyIXeRFUkpqc@sparrow.rmq.cloudamqp.com/kydwwrjg')
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
