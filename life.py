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

        return [
            self._world.cells[x, y_plus_one],
            self._world.cells[x, y_minus_one],
            self._world.cells[x_plus_one, y],
            self._world.cells[x_minus_one, y],
            self._world.cells[x_plus_one, y_minus_one],
            self._world.cells[x_minus_one, y_plus_one],
            self._world.cells[x_plus_one, y_plus_one],
            self._world.cells[x_minus_one, y_minus_one]
        ]

    def get_neighbors(self):
        if self._neighbors is None:
            self._neighbors = self._find_neighbors()

        return self._neighbors

    _next = None

    def next(self):
        if self._next is None:
            self._next = 0  # Catch all...
            live_neighbors = sum(int(n.is_alive) for n in self.get_neighbors())

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


class World(object):

    max_x = None
    max_y = None
    cells = state = None
    cell_list = []

    def __init__(self, size=(100,100), auto_gen_cells=True):
        self.max_x = size[0]
        self.max_y = size[1]

        self.cells = self.state = np.empty((size[0], size[1],), dtype=Cell)

        if auto_gen_cells:

            for x,y in self.world_coordinates():
                c = Cell(x, y, self, initially_alive=(random.randint(0,10000) % 3 == 0))
                self.cell_list.append(c)

    _world_coordinates = None
    def world_coordinates(self):
        if self._world_coordinates is None:
            self._world_coordinates = []
            map(lambda x: self._world_coordinates.append(x), product(xrange(self.max_x), xrange(self.max_y)))

        return self._world_coordinates

    def next(self):
        map(lambda x: x.step(), self.cell_list)
        return ((c.x, c.y, c.next()) for c in self.cell_list if c.next() != c.is_alive)


def main(stdscr):
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.nodelay(1)

    w = World((50, 50), auto_gen_cells=True)

    while 1:
        living_cells = ((x, y, z) for x, y, z in w.next() if z)
        dead_cells = ((c.x, c.y) for c in w.cell_list if not c.next() and c.is_alive)
        for x,y,c in living_cells:
            input = stdscr.getch()

            if input == ord('q'):
                break

            try: stdscr.addch(y, x, '@')
            except curses.error: pass

        for x,y in dead_cells:
            try: stdscr.addch(y, x, ' ')
            except curses.error: pass

        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
