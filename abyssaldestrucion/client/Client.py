import paho.mqtt.client as mqtt
import sys
import random
from Topics import Topics, main_topic


class Client:

    def on_message(self, client, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def on_connect(self, client, userdata, flags, rc):
        print("Client connected")

    def on_publish(self, client, obj, mid):
        pass

    def on_subscribe(self, client, obj, mid, granted_ops):
        pass

    # def on_log(self, ):
    #     pass

    def subscribe_on_topics(self, client):
        client.subscribe(main_topic + "/+", 0)

    def handle_methods(self, client):
        client.on_message = self.on_message
        client.on_connect = self.on_connect
        client.on_publish = self.on_publish
        client.on_subscribe = self.on_subscribe


    def __init__(self):
        self.id = random.randrange(0, 1000, 1)
        client = mqtt.Client(str(self.id))

#        client.on_log = self.on_log
        self.handle_methods(client)
        client.connect("127.0.0.1")
        self.subscribe_on_topics(client)
        client.loop_forever()

client = Client()
