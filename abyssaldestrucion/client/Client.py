import paho.mqtt.client as mqtt
import sys
import random
from ControllerUtil import ControllerUtil
from Topics import Topics, main_topic
from SerialStub import *
from threading import Thread
import Message
import thread
import time
import serial


class Client:

    def on_message(self, client, obj, msg):
        # if no other handler serviced that message
        pass

    def on_message_sonar_in(self, client, userdata, message):
        print("Received sonar_in " + message.payload)
        l = str.split(message.payload, ":")
        id = int(l[0])
        distance = float(l[1])
        if self.id == id:
            self.ping_received(distance)

    def on_message_game_state(self, client, userdata, message):
        who_won = int(message.payload)
        if who_won == self.id: self.game_over(True)
        else: self.game_over(False)

    def on_message_warning(self, client, userdata, message):
        l = str.split(message.payload, ":")
        id = int(l[0])
        value = int(l[1])
        print("Got warning with value " + str(value))

        if (value >= 0 and value <= 31 and id == self.id):

            self.ser.write(chr(value))
            self.warning(value)

    def on_message_life(self, client, userdata, message):
        l = str.split(message.payload, ":")
        id = int(l[0])
        lives = int(l[1])
        print l
        if (lives == 1 or lives == 2) and id == self.id:
            self.vessel_hit(lives)


    def on_connect(self, client, userdata, flags, rc):
        print("Client connected")
        if len(userdata) > 0: print("Client has user data: " + userdata)
        sys.stdout.flush()

    def on_publish(self, client, obj, mid):
        pass

    def on_subscribe(self, client, obj, mid, granted_ops):
        pass

    # methods from server

    def game_over(self, game_won):
        if game_won:
            print("Game over! You won!")
            # output for winning
            self.ser.write(chr(64+8+4))
            self.ser.write(chr(32+1))

        else:
            print("Game over! You lost!")
            # output for lost
            self.ser.write(chr(64+32+16))
            self.ser.write(chr(32+1))

        self.game_on = False
        self.client.loop_stop()
        self.client.disconnect()

    def vessel_hit(self, lives):
        if lives == 2:
            print("Two lifes left")
            self.ser.write(chr(64+8+4))
        elif lives == 1:
            self.ser.write(chr(64+2+1))
            print("One life left!")
        else:
            self.ser.write(chr(64+32+16))

    def ping_received(self, rel_dist):
        # rel_dist from 0 - 1: 0 - 0 distance, 1 - max distnace on map
        # changing distance diode behaviour
        print("ping received " + str(rel_dist))
        t = rel_dist/2.0
        for i in xrange(10):
            self.ser.write(chr(32+1))
            time.sleep(t)
            self.ser.write(chr(32))
            time.sleep(t)


    def warning(self, value):
        # warning has value from 0-31 depending on time spent in restricted area
        pass

    # methods to server

    def change_direction(self, orientation_change):
        # orientation change from 0-63
        print("Changed direction to " + str(orientation_change))
        self.client.publish(main_topic + "/" + Topics.direction, self.message.get_direction_msg(orientation_change, self.id))

    def fire(self):
        # send to server information you fired
        print("Fired!")
        self.client.publish(main_topic + "/" + Topics.weapon, self.message.get_fire_msg(self.id))

    def send_ping(self):
        # sending ping to enemy vessel
        print("Ping sent!")
        self.client.publish(main_topic + "/" + Topics.sonar_out, self.message.get_sonarout_msg(self.id))

    def subscribe_on_topics(self):
        self.client.subscribe(main_topic + "/+", 0)

    def handle_methods(self):
        self.client.on_message = self.on_message
        self.client.message_callback_add(main_topic + "/" + Topics.life, self.on_message_life)
        self.client.message_callback_add(main_topic + "/" + Topics.warning, self.on_message_warning)
        self.client.message_callback_add(main_topic + "/" + Topics.game_state, self.on_message_game_state)
        self.client.message_callback_add(main_topic + "/" + Topics.sonar_in, self.on_message_sonar_in)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe


    def controller_loop(self):
        self.ser.write(chr(128+32+16+8+4))
        print "start"
        while self.game_on:
            cc = self.ser.read(1)
            if len(cc) > 0:
                ch = ord(cc)
                print ch

                # logic reading input from controller
                if ControllerUtil.is_button_1_pressed(ch):
                    self.fire()
                if ControllerUtil.is_button_2_pressed(ch):
                    self.send_ping()
                if ControllerUtil.get_knob_position(ch) is not None:
                    self.change_direction(ControllerUtil.get_knob_position(ch))

    #def sonar_loop(self):
    #    while self.game_on


    def __init__(self):
        self.id = random.randrange(0, 1000, 1)
        self.message = Message.Message()
        self.ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)
        self.game_on = True
        self.client = mqtt.Client(str(self.id), userdata=str(self.id))
        self.distance = 1
        print("Client created")

        self.handle_methods()
        self.client.connect("192.168.17.52")
        self.subscribe_on_topics()
        self.client.publish(main_topic+"/"+Topics.registering, str(self.id))

        thread = Thread(target=self.controller_loop, args=())
        thread.start()

        print("debug")
        sys.stdout.flush()
        self.client.loop_forever()
        thread.join()

client = Client()