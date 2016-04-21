class ControllerUtil:

    def is_button_1_pressed(self, byte):
        return byte == 128+64+2+1

    def is_button_2_pressed(self, byte):
        return byte == 128+64+4+1

    def get_knob_position(self, byte):
        if byte >= 64 and byte < 128:
            return byte-64
        else:
            return None