import paho.mqtt.client as mqtt
import sys
import random
from threading import Thread
from abyssaldestrucion.client.Message import Message

class Main:

    def __init__(self):
        self.message = Message.Message()
        self.game_on = True
        self.server = mqtt.Client()
        print("Server created")
        self.handle_methods()
        self.server.connect("127.0.0.1")
        self.subscribe_on_topics()

        # thread logic

        self.server.loop_forever()



    def handle_methods(self):
        pass

    def subscribe_on_topics(self):
        pass

    def on_message(self, client, obj, msg):
        # if no other handler serviced that message
        print("Should not have got message from that topic: " + msg.topic)

    def on_message_sonar_in(self):
        pass

    def on_message_turn(self):
        pass

    def on_message_weapon(self):
        pass

    def on_connect(self, client, userdata, flags, rc):
        print("Client connected")

    def on_publish(self, client, obj, mid):
        pass

    def on_subscribe(self, client, obj, mid, granted_ops):
        pass
