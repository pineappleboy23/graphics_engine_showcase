import pygame as pg
import random
import math
import time
from itertools import permutations

pg.init()

clock = pg.time.Clock()

sw = 1440
sh = 720
sc = (sw / 2, sh / 2)
screen_color = (48, 141, 240)

pg.display.set_caption("3D")
win = pg.display.set_mode((sw, sh))
win.fill(screen_color)


def pythag(vec_in):
    total = 0
    for i in vec_in:
        total += i*i

    return math.sqrt(total)

def contains(vec_in, item_to_check_for):
    for i in vec_in:
        if i == item_to_check_for:
            return True

    return False


class Cube(object):
    def __init__(self):
        self.center = (-251,-250,700)
        self.side = 100
        self.color = (103,73,200)
        #  frock i haven't figured out 3d angles
        self.get_3d_positions()
        self.get_2d_positions()



    def get_3d_positions(self):
        self.corner1_3d = (
        self.center[0] - self.side / 2, self.center[1] - self.side / 2, self.center[2] + self.side / 2)

        self.corner2_3d = (
        self.center[0] - self.side / 2, self.center[1] + self.side / 2, self.center[2] + self.side / 2)

        self.corner3_3d = (
        self.center[0] + self.side / 2, self.center[1] - self.side / 2, self.center[2] + self.side / 2)

        self.corner4_3d = (
        self.center[0] + self.side / 2, self.center[1] + self.side / 2, self.center[2] + self.side / 2)

        self.corner5_3d = (
        self.center[0] - self.side / 2, self.center[1] - self.side / 2, self.center[2] - self.side / 2)

        self.corner6_3d = (
        self.center[0] - self.side / 2, self.center[1] + self.side / 2, self.center[2] - self.side / 2)

        self.corner7_3d = (
        self.center[0] + self.side / 2, self.center[1] - self.side / 2, self.center[2] - self.side / 2)

        self.corner8_3d = (
        self.center[0] + self.side / 2, self.center[1] + self.side / 2, self.center[2] - self.side / 2)

        self.three_d_poss = [self.corner1_3d, self.corner2_3d, self.corner3_3d, self.corner4_3d, self.corner5_3d,
                           self.corner6_3d, self.corner7_3d, self.corner8_3d]


    def get_2d_positions(self):
        self.two_d_poss = []
        for i in self.three_d_poss:
            self.two_d_poss.append(self.get_2d_from_3d(i))



    def get_2d_from_3d(self, vec_3d):
        x, y, z = vec_3d
        angle = (180*math.atan( (pythag((x, y)))/(z) ))/math.pi
        if x==0:
            m = 0
        else:
            m = y/x  # slope
        x_new = (angle) / math.sqrt(1 + m * m)
        if x < 0:
            x_new *= -1

        x_new *= 30  # field of view changer

        return (x_new, x_new * m)


    def get_closest_corner(self):
        closest_corner = 1
        corner_distance = pythag(self.three_d_poss[0])
        counter = 1
        for i in self.three_d_poss:
            math_stfz = pythag(i)
            if math_stfz <= corner_distance:
                closest_corner = counter
                corner_distance = math_stfz
            counter += 1
        return closest_corner


    def middle_center_to_edge_center(self, vec_in):
        return_vec = []
        for i in vec_in:
            return_vec.append((i[0]+720,i[1]+360))

        return return_vec

    def draw(self, win):

        close_corner = self.get_closest_corner()

        for i in [(1,3,4,2),(5,7,8,6),(1,5,7,3),(6,2,4,8),(5,6,2,1),(4,3,7,8)]:
            if contains(i, close_corner):
                points_2d = ((self.two_d_poss[i[0]-1]), (self.two_d_poss[i[1]-1]), (self.two_d_poss[i[2]-1]), (self.two_d_poss[i[3]-1]))

                pg.draw.polygon(win, self.color, self.middle_center_to_edge_center(points_2d), False)
                pg.draw.polygon(win, (0,0,0), self.middle_center_to_edge_center(points_2d), True)



def redraw_game_window():
    win.fill(screen_color)

    cube.draw(win)

    m_a = .98  # move amount
    cube.center = (cube.center[0] + m_a, cube.center[1] + m_a, cube.center[2])

    cube.get_3d_positions()
    cube.get_2d_positions()

    pg.draw.circle(win, (6,6,6),(720, 360), 4)

    pg.display.update()



cube = Cube()


running = True
while running:

    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    redraw_game_window()
