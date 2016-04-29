class Message:

    def __init__(self):
        pass

    # client -> broker
    def get_sonarout_msg(self, nick):
        return str(nick) + ":" + "ping"

    def get_fire_msg(self, nick):
        return str(nick) + ":" + "fire"

    def get_direction_msg(self, value, nick):
        return str(nick) + ":" + str(value)

    # broker -> client
    def get_warning_msg(self, value, id):
        # value is from 0-31 indicating how long vessel is in warning area
        return str(id) + ":" + str(value)

    def get_life_msg(self, lives, id):
        return str(id) + ":" + str(lives)

    def get_gamestate_msg(self, id):
        # id of who has won
        return str(id)

    def get_sonarin_msg(self, id):
        return str(id)