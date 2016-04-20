class Area:
    # Sizes
    SIZE_X = 1000.0
    SIZE_Y = 1000.0
    # Values for which the border warning should come up
    WARN_RATE = 0.125
    WARN_X0 = WARN_RATE*SIZE_X
    WARN_X1 = (1-WARN_RATE)*SIZE_X
    WARN_Y0 = WARN_RATE*SIZE_Y
    WARN_Y1 = (1-WARN_RATE)*SIZE_Y

    def __init__(self):
        pass
