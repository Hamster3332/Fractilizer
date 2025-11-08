import pygame as pg
from mathicopter import *

def copy_rect(rec: pg.Rect):
    return pg.Rect(rec)

class Grid:
    def __init__(self, pattern: list, gridPWidth, gridPHeight):
        self.width: int = len(pattern[0])
        self.height: int = len(pattern)
        self.orig_width: int = self.width
        self.orig_height: int = self.height
        self.grid_p_width: float = gridPWidth
        self.grid_p_height: float = gridPHeight
        self.rect_width: float = gridPWidth / self.width
        self.rect_height: float = gridPHeight / self.height
        self.retangles: list[pg.Rect] = []
        self.anim_rects: list[pg.Rect] = []
        self.prev_rects: list[pg.Rect] = []
        self.pattern = pattern
        self.iterations = 0

        for x in range(self.width):
            for y in range(self.height):
                if self.pattern[y][x] != 0:
                    self.retangles.append(pg.Rect(x * self.rect_width,
                                                  y * self.rect_height,
                                                  self.rect_width,
                                                  self.rect_height))

    def iterate(self):
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

        if lerp_val >= 1.0 or self.iterations > 3:
            for r in self.retangles:
                pg.draw.rect(window, color, r)
        else:
            for i in range(len(self.anim_rects)):
                self.anim_rects[i].width = lerp(self.prev_rects[i].width, self.retangles[i].width, lerp_val)
                self.anim_rects[i].height = lerp(self.prev_rects[i].height, self.retangles[i].height, lerp_val)

                self.anim_rects[i].x = lerp(self.prev_rects[i].x, self.retangles[i].x, lerp_val)
                self.anim_rects[i].y = lerp(self.prev_rects[i].y, self.retangles[i].y, lerp_val)

                pg.draw.rect(window, color, self.anim_rects[i])



