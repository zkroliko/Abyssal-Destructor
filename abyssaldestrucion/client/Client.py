import paho.mqtt.client as mqtt
import sys
import random
from Topics import Topics, main_topic


class Client:

    def on_message(self, client, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        # reading message
        

    def on_connect(self, client, userdata, flags, rc):
        print("Client connected")

    def on_publish(self, client, obj, mid):
        pass

    def on_subscribe(self, client, obj, mid, granted_ops):
        pass

    # methods from server

    def game_over(self, game_won):
        if game_won:
            print("Game over! You won!")
            # output for winning
        else:
            print("Game over! You lost!")
            # output for lost

    def vessel_hit(self, lives):
        if lives == 2:
            # change life diode to orange
            pass
        elif lives == 1:
            # change life diode to yellow
            pass
        else:
            # change life diode to red
            pass

    def ping_received(self, rel_dist):
        # rel_dist from 0 - 1: 0 - 0 distance, 1 - max distnace on map
        pass
        # changing distance diode behaviour

    # methods to server

    def change_direction(self, orientation_change):
        # orientation change from 0-63
        pass

    def fire(self):
        # send to server information you fired
        pass

    def send_ping(self):
        # sending ping to enemy vessel
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
