import paho.mqtt.client as mqtt
import sys
import random
from threading import Thread

from enum import Enum

from Area import Area
from Visualiser import Visualiser
from time import sleep
from Sub import *
from client.Message import Message
from client.Topics import Topics, main_topic

class GameState(Enum):
    waiting = "waiting"
    running = "running"
    victory = "victory"


class Main:
    MAX_GAME_LENGTH = 1000000
    SLEEP_LENGTH = 0.1

    PLAYER_MAX = 2

    def __init__(self):
        self.message = Message()
        self.game_on = True
        self.client = mqtt.Client()
        print("Server created")
        self.handle_methods()
        self.client.connect("127.0.0.1")
        self.subscribe_on_topics()

        self.state = GameState.waiting
        self.id_to_sub = {}
        self.area = Area()
        self.vis = Visualiser(self.area)

        # thread logic
        thread = Thread(target=self.game_loop, args=())
        thread.start()

        self.client.loop_forever()

    def game_loop(self):
        for i in range(Main.MAX_GAME_LENGTH):
            # TODO: Refactor
            if self.state == GameState.victory:
                break
            sleep(Main.SLEEP_LENGTH)
            if self.state == GameState.running:
                for sub in self.area.vessels:
                    sub.move()
                self.vis.step()
            self.mind_game_state()

    def mind_game_state(self):
        if self.state == GameState.waiting and len(self.area.vessels) >= self.PLAYER_MAX:
            print "--- Game started with %s players ---" % (len(self.area.vessels))
            self.state = GameState.running
        elif self.state == GameState.running and len(self.area.vessels) == 1:
            self.state = GameState.victory
            self.announce_victor(self.area.vessels[0])

    def announce_victor(self, victor):
        self.client.publish(main_topic + "/" + Topics.game_state, str(victor.id))

    def handle_methods(self):
        self.client.on_message = self.on_message
        self.client.message_callback_add(main_topic + "/" + Topics.sonar_in, self.on_message_sonar_in)
        self.client.message_callback_add(main_topic + "/" + Topics.direction, self.on_message_direction)
        self.client.message_callback_add(main_topic + "/" + Topics.weapon, self.on_message_weapon)
        self.client.message_callback_add(main_topic + "/" + Topics.registering, self.on_message_register)

    def subscribe_on_topics(self):
        self.client.subscribe(main_topic + "/+", 0)

    def on_message(self, client, obj, msg):
        # if no other handler serviced that message
        print("Should not have got message from that topic: " + msg.topic)

    def on_message_register(self, server, userdata, msg):
        if msg and len(msg.payload) > 0:
            id = int(msg.payload)
            if self.state == GameState.waiting and len(self.area.vessels) < self.PLAYER_MAX:
                sub = Sub(self.area, name=id)
                # TODO unique
                self.id_to_sub[id] = sub
                self.area.vessels.append(sub)
                print "New user: %s" % (id)
            else:
                print "User with id: %s tried to register but game is running" % (id)
        else:
            print "Failed to register, no msg"

    def on_message_sonar_in(self):
        pass

    def on_message_direction(self, server, userdata, message):
        l = str.split(message.payload, ":")
        id = int(l[0])
        value = int(l[1])
        if self.id_to_sub.has_key(id):
            sub = self.id_to_sub[id]
            print "Boat %s changing direction to %s" % (id, value)
            sub.change_orientation(value)
        else:
            print "No boat by name %s" % (id)

    def on_message_weapon(self, server, userdata, message):
        l = str.split(message.payload, ":")
        id = int(l[0])
        if self.id_to_sub.has_key(id):
            sub = self.id_to_sub[id]
            print "Boat %s firing!!!" % (id)
            hit = sub.fire()
            if len(hit) > 0:
                self.destroy_boats(hit)
            else:
                print "Boat %s missed" % (id)
        else:
            print "No boat by name %s" % (id)

    def on_connect(self, client, userdata, flags, rc):
        print("Server connected")

    def on_publish(self, client, obj, mid):
        pass

    def on_subscribe(self, client, obj, mid, granted_ops):
        pass

    def destroy_boats(self, boats):
        if isinstance(boats, list):
            for boat in boats:
                self.destroy_boat(boat)

    def destroy_boat(self, hit):
        found_id = None
        for id, sub in self.id_to_sub.iteritems():
            if sub is hit:
                found_id = id
                break
        if found_id:
            print "Sub with id %s has been hit" % (found_id)
            self.inform_that_hit(found_id)
            self.id_to_sub.pop(found_id)
            self.area.vessels.remove(hit)
        else:
            print ("ERROR: Unregistered sub has been hit")

    def inform_that_hit(self, id):
        self.client.publish(main_topic + "/" + Topics.life, str(id))


main = Main()
