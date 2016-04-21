class ControllerUtil:

    @staticmethod
    def is_button_1_pressed(byte):
        return byte == 128+64+2+1
    @staticmethod
    def is_button_2_pressed(byte):
        return byte == 128+64+4+1
    @staticmethod
    def get_knob_position(byte):
        if byte >= 64 and byte < 128:
            return byte-64
        else:
            return None