import paho.mqtt.client as mqtt
import sys
import random
from ControllerUtil import ControllerUtil
from Topics import Topics, main_topic
from SerialStub import *
from threading import Thread


class Client:

    def on_message(self, client, obj, msg):
        # if no other handler serviced that message
        print("Should not have got message from that topic: " + msg.topic)

    def on_message_sonar_in(self):
        pass

    def on_message_game_state(self):
        pass

    def on_message_warning(self):
        pass

    def on_message_life(self):
        pass



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

    def warning(self, value):
        # warning has value from 0-31 depending on time spent in restricted area
        pass

    # methods to server

    def change_direction(self, orientation_change):
        # orientation change from 0-63
        print("Changed direction to " + orientation_change)

    def fire(self):
        # send to server information you fired
        print("Fired!")

    def send_ping(self):
        # sending ping to enemy vessel
        print("Ping sent!")


    # def on_log(self, ):
    #     pass

    def subscribe_on_topics(self, client):
        client.subscribe(main_topic + "/+", 0)

    def handle_methods(self, client):
        client.on_message = self.on_message
        client.message_callback_add(main_topic + "/" + Topics.life, self.on_message_life)
        client.message_callback_add(main_topic + "/" + Topics.warning, self.on_message_warning)
        client.message_callback_add(main_topic + "/" + Topics.game_state, self.on_message_game_state)
        client.message_callback_add(main_topic + "/" + Topics.sonar_in, self.on_message_sonar_in)
        client.on_connect = self.on_connect
        client.on_publish = self.on_publish
        client.on_subscribe = self.on_subscribe


    def controller_loop(self):
        ser_stub = SerialStub()
        print "start"
        while True:
            cc = chr(ser_stub.read())
            if len(cc) > 0:
                ch = ord(cc)
                print ch

                # logic reading input from controller
                if ControllerUtil.is_button_1_pressed(ch):
                    self.fire()
                if ControllerUtil.is_button_2_pressed(ch):
                    self.send_ping()
                if ControllerUtil.get_knob_position(ch) is not None:
                    self.change_direction(ControllerUtil.get_knob_position())


    def __init__(self):
        self.id = random.randrange(0, 1000, 1)
        print("debug2")
        client = mqtt.Client(str(self.id))
        print("debug")
#        client.on_log = self.on_log
        self.handle_methods(client)
        client.connect("127.0.0.1")
        self.subscribe_on_topics(client)
        thread = Thread(target=self.controller_loop(), args=())
        thread.start()
        client.loop_forever()
        thread.join()

client = Client()
