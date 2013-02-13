import curses
import random
import numpy as np
from itertools import product

class Cell(object):

    x = None
    y = None
    is_alive = None

    _neighbors = None

    def __init__(self, x, y, world, initially_alive=False):
        self.x = x
        self.y = y

        self._world = world
        self._world.cells[x, y] = self

        self.is_alive = initially_alive

    def _find_neighbors(self):
        x = self.x
        y = self.y
        x_plus_one = x + 1 if x + 1 < self._world.max_x else 0
        x_minus_one = x - 1 if x - 1 >= 0 else self._world.max_x - 1
        y_plus_one = y + 1 if y + 1 < self._world.max_y else 0
        y_minus_one = y - 1 if y - 1 >= 0 else self._world.max_y - 1

        yield self._world.cells[x, y_plus_one]
        yield self._world.cells[x, y_minus_one]

        yield self._world.cells[x_plus_one, y]
        yield self._world.cells[x_minus_one, y]

        yield self._world.cells[x_plus_one, y_minus_one]
        yield self._world.cells[x_minus_one, y_plus_one]

        yield self._world.cells[x_plus_one, y_plus_one]
        yield self._world.cells[x_minus_one, y_minus_one]

    def get_neighbors(self):
        if not self._neighbors:
            self._neighbors = list(self._find_neighbors())

        return self._neighbors

    _next = None

    def next(self):
        if self._next is None:
            self._next = 0  # Catch all...
            live_neighbors = sum(1 for n in self.get_neighbors() if n.is_alive)

            if self.is_alive:
                if 2 > live_neighbors < 3:
                    self._next = 0

                if 1 < live_neighbors < 4:
                    self._next = 1
            else:
                if live_neighbors == 3:
                    self._next = 1

        return self._next

    def step(self):
        self.is_alive = self.next()
        self._next = None
        self.changed = None


class World(object):

    max_x = None
    max_y = None
    cells = state = None

    def __init__(self, size, auto_gen_cells=False):
        self.max_x = size[0]
        self.max_y = size[1]

        self.cells = self.state = np.empty((size[0], size[1],), dtype=Cell)

        if auto_gen_cells:

            for x,y in self.world_coordinates():
                Cell(x, y, self, initially_alive=(random.randint(0,10000) % 3 == 0))

    _world_coordinates = None
    def world_coordinates(self):
        if self._world_coordinates is None:
            self._world_coordinates = []
            map(lambda x: self._world_coordinates.append(x), product(xrange(self.max_x), xrange(self.max_y)))

        return self._world_coordinates

    def next(self):
        map(lambda a: self.cells[a].step(), self.world_coordinates())

        def _g():
            for x,y in self.world_coordinates():
                yield x,y, self.cells[x,y].next()

        return list(_g())


def main(stdscr):
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.nodelay(1)

    w = World((200, 50), auto_gen_cells=True)

    while 1:
        for x,y,c in w.next():
            input = stdscr.getch()

            if input == ord('q'):
                break

            try: stdscr.addch(y, x, '@' if c else ' ')
            except curses.error: pass

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)