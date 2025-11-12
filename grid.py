import math

import pygame as pg
from mathicopter import *
from shapeEnum import *

def copy_rect(rec: pg.Rect):
    return pg.Rect(rec)

class Grid:
    def __init__(self, pattern: list, gridPWidth, gridPHeight, shape: int = Shape.rectangle):
        self.width: int = len(pattern[0])
        self.height: int = len(pattern)
        self.orig_width: int = self.width
        self.orig_height: int = self.height
        self.grid_p_width: float = gridPWidth
        self.grid_p_height: float = gridPHeight
        self.pattern = pattern
        self.iterations = 0
        self.shape = shape

        if shape == Shape.rectangle:
            self.rect_width: float = gridPWidth / self.width
            self.rect_height: float = gridPHeight / self.height
            self.retangles: list[pg.Rect] = []
            self.anim_rects: list[pg.Rect] = []
            self.prev_rects: list[pg.Rect] = []

            for x in range(self.width):
                for y in range(self.height):
                    if self.pattern[y][x] != 0:
                        self.retangles.append(pg.Rect(x * self.rect_width,
                                                      y * self.rect_height,
                                                      self.rect_width,
                                                      self.rect_height))

            self.anim_rects = self.retangles
            self.prev_rects = self.retangles

        elif shape == Shape.hexagon:
            if self.width / self.height != gridPWidth / gridPHeight:
                raise ValueError("Wrong Aspect ratio of the window for that pattern!")

            self.precalc_points = []
            for degree_i in range(6):  # 6 because hexagon, for each point
                self.precalc_points.append((math.cos(degree_i / 6 * math.pi * 2),
                               math.sin(degree_i / 6 * math.pi * 2)))
            #print(self.precalc_points)
            self.hex_ratio2 = math.tan(math.radians(30)) # multiply by self.hex_height / 2


            self.hex_height: float = gridPHeight / (self.height + 0.5) # The shortest straight line passing through the center
            self.hex_width: float = 2 * math.sqrt(math.pow(self.hex_height / 2, 2) + pow(math.tan(math.radians(30)) * (self.hex_height / 2), 2))
            self.hex_ratio: float = self.hex_width / self.hex_height
            self.hexagons = [] # A list of positions and the points [(center_x, center_y, [(x, y), (x, y), ...]), ...]
            self.hex_margin: float = 3

            for x in range(self.width):
                for y in range(self.height):
                    if self.pattern[y][x] != 0:
                        hex_y = self.hex_height / 2 + y * self.hex_height
                        if x % 2 != 0:
                            hex_y += self.hex_height / 2
                        hex_x = self.hex_width / 2 + x * (self.hex_width - self.hex_ratio2 * self.hex_height / 2)

                        points = []
                        for degree_i in range(6):  # 6 because hexagon, for each point
                            points.append((round(self.precalc_points[degree_i][0] * (self.hex_width / 2 - self.hex_margin) + hex_x),
                                           round(self.precalc_points[degree_i][1] * (self.hex_width / 2 - self.hex_margin) + hex_y)))

                        self.hexagons.append((hex_x, hex_y, points))

    def iterate(self):
        if self.shape == Shape.rectangle:
            self.width *= self.orig_width
            self.height *= self.orig_height
            self.rect_width = self.grid_p_width / self.width
            self.rect_height = self.grid_p_height / self.height
            self.rect_width = max(self.rect_width, 1)
            self.rect_height = max(self.rect_height, 1)

            new_rects = []
            self.anim_rects = []
            for rec in self.retangles:
                for x in range(self.orig_width):
                    for y in range(self.orig_height):
                        if self.pattern[y][x] != 0:
                            self.anim_rects.append(copy_rect(rec))
                            new_rec = pg.Rect(rec.x + x * self.rect_width,
                                              rec.y + y * self.rect_height,
                                              self.rect_width,
                                              self.rect_height)
                            new_rects.append(new_rec)

            self.prev_rects = self.anim_rects
            self.retangles = new_rects
            self.iterations += 1
            """
            print("length prev_rects: " + str(len(self.prev_rects)))
            print("length rects: " + str(len(self.retangles)))
            print("length anim_rects: " + str(len(self.anim_rects)))
            """

    def draw(self, window: pg.Surface, color: pg.Color, lerp_val: float):

        if lerp_val >= 1.0 or self.iterations > 3 or True:
            if self.shape == Shape.rectangle:
                for r in self.retangles:
                    pg.draw.rect(window, color, r)

            elif self.shape == Shape.hexagon:
                for h in self.hexagons:
                    pg.draw.polygon(window, color, h[2])

        else:
            if self.shape == Shape.rectangle:
                for i in range(len(self.anim_rects)):
                    self.anim_rects[i].width = lerp(self.prev_rects[i].width, self.retangles[i].width, lerp_val)
                    self.anim_rects[i].height = lerp(self.prev_rects[i].height, self.retangles[i].height, lerp_val)

                    self.anim_rects[i].x = lerp(self.prev_rects[i].x, self.retangles[i].x, lerp_val)
                    self.anim_rects[i].y = lerp(self.prev_rects[i].y, self.retangles[i].y, lerp_val)

                    pg.draw.rect(window, color, self.anim_rects[i])


