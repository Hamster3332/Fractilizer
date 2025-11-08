import random

from grid import *
import math

pg.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
FPS = 180

window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

clock = pg.time.Clock()

def main_loop():
    frame = 1
    pattern = [[1, 1, 1],
               [1, 0, 1],
               [1, 1, 1]]

    grid = Grid(pattern, WINDOW_WIDTH, WINDOW_HEIGHT)
    running = True
    color = pg.Color(random.randint(20, 255), random.randint(20, 255), random.randint(20, 255))
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        window.fill('black')

        if frame >= FPS:
            frame = 0
            if grid.iterations < 7:
                grid.iterate()

        grid.draw(window, color, easeInCubic(frame / FPS))
        pg.display.flip()
        frame += 1
        clock.tick(FPS)

if __name__ == "__main__":
    main_loop()