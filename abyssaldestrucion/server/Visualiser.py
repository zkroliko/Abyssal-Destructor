import threading
from Tkinter import Tk, Canvas, mainloop

import time

from server.Area import Area
from server.Sub import Sub


class Visualiser(threading.Thread):
    FRAMES_PER_STEP = 20

    # It can work with given scale or given sizes
    SCALE = 0.5

    DYNAMIC_SCALE = True
    SIZE_X = 700
    SIZE_Y = 700

    # Vessel size
    VESSEL_X = 16
    VESSEL_Y = 16

    def __init__(self, area):
        super(Visualiser, self).__init__()
        self.area = area

        # Steps
        self.steps = 0

        # Synchronization
        self.lock = threading.Lock()
        self.lock.acquire()

        self.subs = []

        self.master = Tk()
        self.w = Canvas(self.master, width=sx(Area.SIZE_X), height=sy(Area.SIZE_Y))
        self.w.config(borderwidth=sx(10))
        self.w.pack()

        self.__draw_warning_areas()

    def run(self):
        self.animate()

    def animate(self):
        self.__draw_one_frame()
        #self.master.after(120, self.animate())

    def step(self):
        self.step +=1

    def draw(self):
        # Code to check steps
        self.lock.release()

    def __draw_one_frame(self):
        # Lock
        self.lock.acquire()
        # ------ SECTION START
        self.__clear_ships()
        s = Sub(self.area)
        self.__draw_ships()
        # ------ SECTION END
        # Unclock

    def __draw_ships(self):
        for s in self.area.vessels:
            self.__draw_ship(s)

    def __draw_ship(self, target):
        # Just for dimensions
        ship_start = scale_ship_start(target.x, target.y)
        ship_end = scale_ship_end(target.x, target.y)
        ship = self.w.create_oval(ship_start[0], ship_start[1], ship_end[0], ship_end[1])
        self.subs.append(ship)

    def __clear_ships(self):
        for s in self.subs:
            self.w.delete(s)

    def __draw_warning_areas(self):
        self.__draw_warning_area(0, 0, Area.WARN_X0, Area.SIZE_Y)
        self.__draw_warning_area(0, 0, Area.SIZE_Y, Area.WARN_Y0)
        self.__draw_warning_area(Area.WARN_X1, 0, Area.SIZE_X, Area.SIZE_Y)
        self.__draw_warning_area(0, Area.WARN_Y1, Area.SIZE_X, Area.SIZE_Y)

    def __draw_warning_area(self, start_x, start_y, end_x, end_y):
        self.w.create_rectangle(sx(start_x), sy(start_y), sx(end_x), sy(end_y), fill="orange", outline="orange")


def scale_ship_start(x, y):
    return sx(x - Visualiser.VESSEL_X / 2), sy(y - Visualiser.VESSEL_Y / 2)


def scale_ship_end(x, y):
    return sx(x + Visualiser.VESSEL_X / 2), sy(y + Visualiser.VESSEL_Y / 2),


def sx(x):
    if Visualiser.DYNAMIC_SCALE:
        return int(x * Visualiser.SIZE_X / Area.SIZE_X)
    else:
        return int(x * Visualiser.SCALE)


def sy(y):
    if Visualiser.DYNAMIC_SCALE:
        return int(y * Visualiser.SIZE_Y / Area.SIZE_Y)
    else:
        return int(y * Visualiser.SCALE)
