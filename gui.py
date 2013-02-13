import sys
import numpy as np
import pyglet
import life

game = None
grid_w = None
grid_h = None
fps_display = pyglet.clock.ClockDisplay()
batch = pyglet.graphics.Batch()
window = pyglet.window.Window(resizable=True)


@window.event
def on_key_press(symbol, modifiers):
    global grid_w
    global grid_h
    if symbol == pyglet.window.key.Q:
        window.close()

    if symbol == pyglet.window.key.F:
        window.set_fullscreen(not (modifiers & pyglet.window.key.MOD_SHIFT))
        grid_w = float(window.width) / game.state.shape[0]
        grid_h = float(window.height) / game.state.shape[1]


@window.event
def on_resize(width, height):
    global grid_w
    global grid_h
    grid_w = float(width) / game.state.shape[0]
    grid_h = float(height) / game.state.shape[1]


def draw(state):

    for x,y,v in state:

        top_left = (grid_w * x, grid_h * y)
        top_right = (grid_w * (x + 1), grid_h * y)
        bottom_left = (grid_w * x, grid_h * (y + 1))
        bottom_right = (grid_w * (x + 1), grid_h * (y + 1))

        batch.add(4, pyglet.gl.GL_QUADS,
            None,
            ('v2f', top_left + bottom_left + bottom_right + top_right),
            ('c3f', (v, v, v) * 4)
        )


@window.event
def on_draw():
    window.clear()
    frame = game.next()
    draw(frame)
    batch.draw()
    fps_display.draw()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        size = (sys.argv[1], sys.argv[2])
    else:
        size = None
    global game
    global grid_w
    global grid_h
    game = life.World(map(int,size), auto_gen_cells=True)
    grid_w = float(window.width) / game.state.shape[0]
    grid_h = float(window.height) / game.state.shape[1]

    pyglet.app.run()
