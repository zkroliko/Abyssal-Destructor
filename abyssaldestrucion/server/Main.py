import paho.mqtt.client as mqtt
import sys
import random
from threading import Thread
from Message import Message
from Topics import main_topic
from Area import Area
from Visualiser import Visualiser
from time import sleep
from Topics import *
from Sub import *


class Main:

    MAX_GAME_LENGTH = 1000000
    SLEEP_LENGTH = 0.1

    def __init__(self):
        self.message = Message()
        self.game_on = True
        self.server = mqtt.Client()
        print("Server created")
        self.handle_methods()
        self.server.connect("127.0.0.1")
        self.subscribe_on_topics()

        self.id_to_sub = {}
        self.area = Area()
        self.vis = Visualiser(self.area)

        # thread logic
        thread = Thread(target=self.game_loop, args=())
        thread.start()

        self.server.loop_forever()

    def game_loop(self):
        for i in range(Main.MAX_GAME_LENGTH):
            sleep(Main.SLEEP_LENGTH)
            for sub in self.area.vessels:
                sub.move()
            self.vis.step()


    def handle_methods(self):
        self.server.on_message = self.on_message
        self.server.message_callback_add(main_topic+"/"+Topics.sonar_in, self.on_message_sonar_in)
        self.server.message_callback_add(main_topic+"/"+Topics.direction, self.on_message_direction)
        self.server.message_callback_add(main_topic+"/"+Topics.weapon, self.on_message_weapon)
        self.server.message_callback_add(main_topic+"/"+Topics.registering, self.on_message_register)


    def subscribe_on_topics(self):
        self.server.subscribe(main_topic + "/+", 0)

    def on_message(self, client, obj, msg):
        # if no other handler serviced that message
        print("Should not have got message from that topic: " + msg.topic)

    def on_message_register(self, server, userdata, msg):
        if msg and len(msg.payload) > 0:
            id = int(msg.payload)
            sub = Sub(self.area)
            #TODO unique
            self.id_to_sub[id] = sub
            self.area.vessels.append(sub)
            print "New user: %s" % (id)
        else:
            print "Failed to register, no msg"


    def on_message_sonar_in(self):
        pass

    def on_message_direction(self, server, userdata, message):
        l = str.split(message.payload, ":")
        id = int(l[0])
        value = int(l[1])
        sub = self.id_to_sub[id]
        if sub:
            print "Boat %s changing direction to %s" % (id, value)
            sub.change_direction(value)
        else:
            print "No boat by name %s" % (id)

    def on_message_weapon(self):
        pass

    def on_connect(self, client, userdata, flags, rc):
        print("Server connected")

    def on_publish(self, client, obj, mid):
        pass

    def on_subscribe(self, client, obj, mid, granted_ops):
        pass

main = Main()