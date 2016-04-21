class SerialStub:

    def __init__(self):
        ser = chr(0)

    def read(self):
        return input()
