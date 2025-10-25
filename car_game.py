
import math
import numpy as np


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from random import randint
from threading import Thread
from time import sleep
from pynput.keyboard import Controller

#circle

class MidpointCircle:
    def __init__(self):
        self.__midpoint_points = []


    def convert_to_other_zone(self, x1, y1, zone):
        if zone == 0:
            return x1, y1
        elif zone == 1:
            return y1, x1
        elif zone == 2:
            return -y1, x1
        elif zone == 3:
            return -x1, y1
        elif zone == 4:
            return -x1, -y1
        elif zone == 5:
            return -y1, -x1
        elif zone == 6:
            return y1, -x1
        elif zone == 7:
            return x1, -y1

    def midpoint_circle_algorithm(self, radius, center_x=0.0, center_y=0.0, y=0):
        glBegin(GL_POINTS)

        d = 1 - radius

        x = radius
        glVertex2f(x + center_x, y + center_y)

        for i in range(8):
            x_other, y_other = self.convert_to_other_zone(x, y, i)
            glVertex2f(x_other + center_x, y_other + center_y)

        while x > y:
            if d < 0:
                y = y + 1
                d = d + 2 * y + 3
            else:
                x = x - 1
                y = y + 1
                d = d + 2 * y - 2 * x + 5

            self.__midpoint_points.append((x, y))

            glVertex2f(x + center_x, y + center_y)

            for i in range(8):
                x_other, y_other = self.convert_to_other_zone(x, y, i)
                self.__midpoint_points.append((x_other, y_other))
                glVertex2f(x_other + center_x, y_other + center_y)

        glEnd()

    def filled_circle(self, radius, center_x=0, center_y=0):
        for i in range(radius):
            self.midpoint_circle_algorithm(i, center_x, center_y)


#digit


class Digits:
    def __init__(self):
        self.__midpoint_points = []

    def find_zone(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1

        if abs(dx) > abs(dy):
            if dx >= 0 and dy >= 0:
                return 0
            elif dx <= 0 and dy >= 0:
                return 3
            elif dx <= 0 and dy <= 0:
                return 4
            elif dx >= 0 and dy <= 0:
                return 7
        else:
            if dx >= 0 and dy >= 0:
                return 1
            elif dx <= 0 and dy >= 0:
                return 2
            elif dx <= 0 and dy <= 0:
                return 5
            elif dx >= 0 and dy <= 0:
                return 6

    def convert_to_zone0(self, x1, y1, zone):
        if zone == 0:
            return x1, y1
        elif zone == 1:
            return y1, x1
        elif zone == 2:
            return y1, -x1
        elif zone == 3:
            return -x1, y1
        elif zone == 4:
            return -x1, -y1
        elif zone == 5:
            return -y1, -x1
        elif zone == 6:
            return -y1, x1
        elif zone == 7:
            return x1, -y1

    def convert_to_original_zone(self, x1, y1, zone):
        if zone == 0:
            return x1, y1
        elif zone == 1:
            return y1, x1
        elif zone == 2:
            return -y1, x1
        elif zone == 3:
            return -x1, y1
        elif zone == 4:
            return -x1, -y1
        elif zone == 5:
            return -y1, -x1
        elif zone == 6:
            return y1, -x1
        elif zone == 7:
            return x1, -y1

    def midpoint(self, x1, y1, x2, y2):
        glBegin(GL_POINTS)

        zone = self.find_zone(x1, y1, x2, y2)

        x1_to_z0, y1_to_z0 = self.convert_to_zone0(x1, y1, zone)
        x2_to_z0, y2_to_z0 = self.convert_to_zone0(x2, y2, zone)

        dy = y2_to_z0 - y1_to_z0
        dx = x2_to_z0 - x1_to_z0
        d = 2 * dy - dx
        d_E = 2 * dy
        d_NE = 2 * (dy - dx)

        x = x1_to_z0
        y = y1_to_z0

        original_x, original_y = self.convert_to_original_zone(x, y, zone)
        glVertex2f(original_x, original_y)

        while x <= x2_to_z0:
            self.__midpoint_points.append((original_x, original_y))

            if d < 0:
                x = x + 1
                d = d + d_E
            else:
                x = x + 1
                y = y + 1
                d = d + d_NE

            original_x, original_y = self.convert_to_original_zone(x, y, zone)
            glVertex2f(original_x, original_y)

        glEnd()

    def draw_digit(self, digit, offset_x=0, offset_y=0, digit_position_x=0):

        digit_lights = {
            0: [self.l_t, self.l_b, self.b, self.r_b, self.r_t, self.t],
            1: [self.r_b, self.r_t],
            2: [self.l_b, self.b, self.r_t, self.t, self.m],
            3: [self.b, self.r_b, self.r_t, self.t, self.m],
            4: [self.l_t, self.r_b, self.r_t, self.m],
            5: [self.l_t, self.b, self.r_b, self.t, self.m],
            6: [self.l_t, self.l_b, self.b, self.r_b, self.t, self.m],
            7: [self.r_b, self.r_t, self.t],
            8: [self.l_t, self.l_b, self.b, self.r_b, self.t, self.r_t, self.m],
            9: [self.l_t, self.b, self.r_b, self.t, self.r_t, self.m]
        }

       
        show_digits = digit

        first_digit = int(show_digits[0])
        if int(digit) > 9:
            second_digit = int(show_digits[1])

        if int(digit) <= 9:
            first_digit = 0
            second_digit = int(show_digits[0])

        for i in digit_lights[first_digit]:
            i(x=digit_position_x + offset_x, y=250 + offset_y)

        for i in digit_lights[second_digit]:
            i(x=digit_position_x + offset_x, y=250 + offset_y, adjust=250)

    def get_midpoint_points(self):
        return self.__midpoint_points

    def r_t(self, adjust=0, x=0, y=0):
        self.midpoint(400 + adjust + x, 400 + y, 400 + adjust + x, 600 + y)

    def r_b(self, adjust=0, x=0, y=0):
        self.midpoint(400 + adjust + x, 200 + y, 400 + adjust + x, 400 + y)

    def l_t(self, adjust=0, x=0, y=0):
        self.midpoint(200 + adjust + x, 400 + y, 200 + adjust + x, 600 + y)

    def l_b(self, adjust=0, x=0, y=0):
        self.midpoint(200 + adjust + x, 200 + y, 200 + adjust + x, 400 + y)

    def b(self, adjust=0, x=0, y=0):
        self.midpoint(200 + adjust + x, 200 + y, 400 + adjust + x, 200 + y)

    def t(self, adjust=0, x=0, y=0):
        self.midpoint(200 + adjust + x, 600 + y, 400 + adjust + x, 600 + y)

    def m(self, adjust=0, x=0, y=0):
        self.midpoint(200 + adjust + x, 400 + y, 400 + adjust + x, 400 + y)


#line


class MidpointLine:
    def __init__(self):
        self.__midpoint_points = []

    def find_zone(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1

        if abs(dx) > abs(dy):
            if dx >= 0 and dy >= 0:
                return 0
            elif dx <= 0 and dy >= 0:
                return 3
            elif dx <= 0 and dy <= 0:
                return 4
            elif dx >= 0 and dy <= 0:
                return 7
        else:
            if dx >= 0 and dy >= 0:
                return 1
            elif dx <= 0 and dy >= 0:
                return 2
            elif dx <= 0 and dy <= 0:
                return 5
            elif dx >= 0 and dy <= 0:
                return 6

    def convert_to_zone0(self, x1, y1, zone):
        if zone == 0:
            return x1, y1
        elif zone == 1:
            return y1, x1
        elif zone == 2:
            return y1, -x1
        elif zone == 3:
            return -x1, y1
        elif zone == 4:
            return -x1, -y1
        elif zone == 5:
            return -y1, -x1
        elif zone == 6:
            return -y1, x1
        elif zone == 7:
            return x1, -y1

    def convert_to_original_zone(self, x1, y1, zone):
        if zone == 0:
            return x1, y1
        elif zone == 1:
            return y1, x1
        elif zone == 2:
            return -y1, x1
        elif zone == 3:
            return -x1, y1
        elif zone == 4:
            return -x1, -y1
        elif zone == 5:
            return -y1, -x1
        elif zone == 6:
            return y1, -x1
        elif zone == 7:
            return x1, -y1

    def midpoint(self, x1, y1, x2, y2):
        glBegin(GL_POINTS)

        zone = self.find_zone(x1, y1, x2, y2)

        x1_to_z0, y1_to_z0 = self.convert_to_zone0(x1, y1, zone)
        x2_to_z0, y2_to_z0 = self.convert_to_zone0(x2, y2, zone)

        dy = y2_to_z0 - y1_to_z0
        dx = x2_to_z0 - x1_to_z0
        d = 2 * dy - dx
        d_E = 2 * dy
        d_NE = 2 * (dy - dx)

        x = x1_to_z0
        y = y1_to_z0

        original_x, original_y = self.convert_to_original_zone(x, y, zone)
        glVertex2f(original_x, original_y)

        while x <= x2_to_z0:
            self.__midpoint_points.append((original_x, original_y))

            if d < 0:
                x = x + 1
                d = d + d_E
            else:
                x = x + 1
                y = y + 1
                d = d + d_NE

            original_x, original_y = self.convert_to_original_zone(x, y, zone)
            glVertex2f(original_x, original_y)

        glEnd()

#menu



line = MidpointLine()
circle = MidpointCircle()


class Menu:
    def __init__(self, win_size_x=500, win_size_y=500, win_pos_x=0, win_pos_y=0,
                 pixel_size=1):
        self.win_size_x = win_size_x
        self.win_size_y = win_size_y
        self.win_pos_x = win_pos_x
        self.win_pos_y = win_pos_y
        self.pixel_size = pixel_size

    def initialize(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(self.win_size_x, self.win_size_y)
        glutInitWindowPosition(self.win_size_x // 2 - self.win_size_x, 0)
        glutCreateWindow(self.title)
        glClearColor(0, 0, 0, 0),
        glutDisplayFunc(self.show_screen)

        glViewport(0, 0, self.win_size_x, self.win_size_y)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.win_size_x, self.win_size_x, -self.win_size_y, self.win_size_y, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glPointSize(self.pixel_size)
        glLoadIdentity()

    def show_screen(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glColor3f(0, 0, 0)

        self.text()

        glutSwapBuffers()

    def start_main_loop(self):
        glutMainLoop()

    def game_over_text(self, x=0, y=0):
        for i in range(10, 50, 1):
            self.g(adjust=0, x=i + x, y=i + y)
            self.a(adjust=150, x=i + x, y=i + y)
            self.m(adjust=300, x=i + x, y=i + y)
            self.e(adjust=450, x=i + x, y=i + y)
            self.o(adjust=750, x=i + x, y=i + y)
            self.v(adjust=900, x=i + x, y=i + y)
            self.e(adjust=1050, x=i + x, y=i + y)
            self.r(adjust=1200, x=i + x, y=i + y)

    def score_text(self, x=0, y=0):
        for i in range(10, 40, 1):
            self.s(adjust=0, x=i + x, y=i + y)
            self.c(adjust=150, x=i + x, y=i + y)
            self.o(adjust=300, x=i + x, y=i + y)
            self.r(adjust=450, x=i + x, y=i + y)
            self.e(adjust=600, x=i + x, y=i + y)

    def text(self):
        for i in range(0, 10, 2):
            circle.midpoint_circle_algorithm(700 - i, 0, 0)

        for i in range(0, 100, 10):
            circle.midpoint_circle_algorithm(700 - i, 0, 0)

        left_x1, left_y1 = -700, -900
        offset = -50

        line.midpoint(left_x1 + offset, left_y1, left_x1 + offset, 900)
        line.midpoint(-left_x1 - offset, left_y1, -left_x1 - offset, 900)

        for i in range(10):
            line.midpoint(left_x1 + offset + i, left_y1, left_x1 + offset + i + i * 10, 900)
            line.midpoint(-left_x1 - offset - i, left_y1, -left_x1 - offset - i - i * 10, 900)

        score_text = Digits()
        digit_position = 900
        SCORE = 00

        for i in range(5, 20, 10):
            score_text.draw_digit(f"{SCORE}", offset_x=i, offset_y=i, digit_position_x=digit_position)



    def a(self, x=0, y=0, adjust=0):
        line.midpoint(x + 0 + adjust, y + 0, x + 0 + adjust, y + 70)  
        line.midpoint(x + 0 + adjust, y + 80, x + 0 + adjust, y + 150)  
        line.midpoint(x + 10 + adjust, y + 150, x + 70 + adjust, y + 150)  
        line.midpoint(x + 80 + adjust, y + 80, x + 80 + adjust, y + 150) 
        line.midpoint(x + 80 + adjust, y + 0, x + 80 + adjust, y + 70)  
        line.midpoint(x + 10 + adjust, y + 70, x + 70 + adjust, y + 70)  

    def g(self, x=0, y=0, adjust=0):
        line.midpoint(x + 0 + adjust, y + 0, x + 0 + adjust, y + 70)  
        line.midpoint(x + 0 + adjust, y + 80, x + 0 + adjust, y + 150)  
        line.midpoint(x + 10 + adjust, y + 150, x + 70 + adjust, y + 150)  
        line.midpoint(x + 80 + adjust, y + 0, x + 80 + adjust, y + 70) 
        line.midpoint(x + 10 + adjust, y + 0, x + 70 + adjust, y + 0)  
        line.midpoint(x + 10 + adjust, y + 70, x + 70 + adjust, y + 70)  

    def m(self, x=0, y=0, adjust=0):
        line.midpoint(x + 0 + adjust, y + 0, x + 0 + adjust, y + 70)  
        line.midpoint(x + 0 + adjust, y + 80, x + 0 + adjust, y + 150)  
        line.midpoint(x + 80 + adjust, y + 80, x + 80 + adjust, y + 150)  
        line.midpoint(x + 80 + adjust, y + 0, x + 80 + adjust, y + 70)  

        line.midpoint(x + 45 + adjust, y + 10 + 80, x + 70 + adjust, y + 60 + 80)
        line.midpoint(x + 40 + adjust, y + 10 + 80, x + 10 + adjust, y + 60 + 80)

    def e(self, x=0, y=0, adjust=0):
        line.midpoint(x + 0 + adjust, y + 0, x + 0 + adjust, y + 70)  
        line.midpoint(x + 0 + adjust, y + 80, x + 0 + adjust, y + 150) 
        line.midpoint(x + 10 + adjust, y + 150, x + 70 + adjust, y + 150)  
        line.midpoint(x + 10 + adjust, y + 0, x + 70 + adjust, y + 0) 
        line.midpoint(x + 10 + adjust, y + 70, x + 70 + adjust, y + 70)  

    def o(self,  x=0, y=0, adjust=0):
        line.midpoint(x + 0 + adjust, y + 0, x + 0 + adjust, y + 70)  
        line.midpoint(x + 0 + adjust, y + 80, x + 0 + adjust, y + 150)  
        line.midpoint(x + 10 + adjust, y + 150, x + 70 + adjust, y + 150) 
        line.midpoint(x + 80 + adjust, y + 80, x + 80 + adjust, y + 150) 
        line.midpoint(x + 80 + adjust, y + 0, x + 80 + adjust, y + 70)  
        line.midpoint(x + 10 + adjust, y + 0, x + 70 + adjust, y + 0)  

    def v(self, x=0, y=0, adjust=0):
        line.midpoint(x + 0 + adjust, y + 80, x + 0 + adjust, y + 150)  
        line.midpoint(x + 80 + adjust, y + 80, x + 80 + adjust, y + 150)  

        line.midpoint(x + 45 + adjust, y + 0, x + 80 + adjust, y + 60) 
        line.midpoint(x + 35 + adjust, y + 0, x + 0 + adjust, y + 60)  

    def r(self, x=0, y=0, adjust=0):
        line.midpoint(x + 0 + adjust, y + 0, x + 0 + adjust, y + 70)  
        line.midpoint(x + 0 + adjust, y + 80, x + 0 + adjust, y + 150)  
        line.midpoint(x + 10 + adjust, y + 150, x + 70 + adjust, y + 150)  
        line.midpoint(x + 80 + adjust, y + 80, x + 80 + adjust, y + 150)  
        line.midpoint(x + 10 + adjust, y + 70, x + 70 + adjust, y + 70)  

        line.midpoint(x + 80 + adjust, y + 0, x + 10 + adjust, y + 60)  


    def s(self, x=0, y=0, adjust=0):
        line.midpoint(x + 0 + adjust, y + 80, x + 0 + adjust, y + 150)  
        line.midpoint(x + 10 + adjust, y + 150, x + 70 + adjust, y + 150)  
        line.midpoint(x + 80 + adjust, y + 0, x + 80 + adjust, y + 70)  
        line.midpoint(x + 10 + adjust, y + 0, x + 70 + adjust, y + 0)  
        line.midpoint(x + 10 + adjust, y + 70, x + 70 + adjust, y + 70)  

    def c(self, x=0, y=0, adjust=0):
        line.midpoint(x + 0 + adjust, y + 0, x + 0 + adjust, y + 70)  
        line.midpoint(x + 0 + adjust, y + 80, x + 0 + adjust, y + 150)  
        line.midpoint(x + 10 + adjust, y + 150, x + 70 + adjust, y + 150)  
        line.midpoint(x + 10 + adjust, y + 0, x + 70 + adjust, y + 0) 

#rock
class Rock:
    def __init__(self, x, y, speed, radius):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius


# Globals

colors = 0, 0, 0

SCORE = 0

X_MAX_GLOBAL = 700
X_MIN_GLOBAL = -700
Y_MAX_GLOBAL = 900
Y_MIN_GLOBAL = -900
ROAD_LENGTH = 900

ROCKS = []
num_rocks = 7
for i in range(num_rocks):
    rock = Rock(randint(X_MIN_GLOBAL, X_MAX_GLOBAL), Y_MAX_GLOBAL, randint(10, 15), randint(20, 50))
    ROCKS.append(rock)

SPEED_MULTIPLIER = 4

MOVE_DISPLACEMENT = 50

auto_key_press = Controller()

line = MidpointLine()
circle = MidpointCircle()
menu = Menu()

CAR_X = 0
CAR_Y = Y_MIN_GLOBAL + 100
CAR_WIDTH = 80

GAME_OVER = False


def update():
    global ROAD_LENGTH, colors, \
        CAR_Y, \
        CAR_X, \
        SPEED_MULTIPLIER, \
        GAME_OVER

    while True:
        SPEED_MULTIPLIER += 0.001

        auto_key_press.press(",")
        sleep(0.1)

        if GAME_OVER:
            break

        ROAD_LENGTH -= 20
        if ROAD_LENGTH <= -900:
            ROAD_LENGTH = 900

        colors = 1, 1, 0

        for i in range(num_rocks):
            ROCKS[i].y -= ROCKS[i].speed * SPEED_MULTIPLIER
            if ROCKS[i].y < Y_MIN_GLOBAL:
                ROCKS[i].y = 900
                ROCKS[i].x = randint(X_MIN_GLOBAL, X_MAX_GLOBAL)

        glutPostRedisplay()


def score_increment():
    global SCORE
    while True:
        sleep(1)
        glutPostRedisplay()
        SCORE += 1
        if GAME_OVER:
            break


class Race:
    def __init__(self, win_size_x=500, win_size_y=500, win_pos_x=0, win_pos_y=0,
                 pixel_size=1):
        self.win_size_x = win_size_x
        self.win_size_y = win_size_y
        self.win_pos_x = win_pos_x
        self.win_pos_y = win_pos_y
        self.pixel_size = pixel_size

        self.player1_radius = 40
        self.player1_move_x = 0
        self.player1_move_y = 0
        self.score = 10

        self.player2_radius = 20
        self.player_move_x = 0
        self.player_move_y = 0

    def initialize(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(self.win_size_x, self.win_size_y)
        glutInitWindowPosition(self.win_size_x // 2 - self.win_size_x, 0)
        glutCreateWindow(b"Race Game")
        glClearColor(0, 0, 0, 0),
        glutDisplayFunc(self.show_screen)
        glutKeyboardFunc(self.buttons)

        animation_thread = Thread(target=update)
        animation_thread.start()

        global score_thread
        score_thread = Thread(target=score_increment)
        score_thread.start()

        glViewport(0, 0, self.win_size_x, self.win_size_y)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.win_size_x, self.win_size_x, -
        self.win_size_y, self.win_size_y, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glPointSize(self.pixel_size)
        glLoadIdentity()
       

    def buttons(self, key, x, y):
        global CAR_Y, \
            CAR_X, \
            CAR_WIDTH, \
            GAME_OVER, \
            SCORE

        if key == b"w" and CAR_Y < Y_MAX_GLOBAL:
            CAR_Y += MOVE_DISPLACEMENT
        if key == b"a" and CAR_X > X_MIN_GLOBAL:
            CAR_X -= MOVE_DISPLACEMENT
        if key == b"s" and CAR_Y > Y_MIN_GLOBAL:
            CAR_Y -= MOVE_DISPLACEMENT
        if key == b"d" and CAR_X < X_MAX_GLOBAL:
            CAR_X += MOVE_DISPLACEMENT

        if CAR_Y < - self.win_size_y:
            CAR_Y = self.win_size_y

        if CAR_X < - self.win_size_x:
            CAR_X = self.win_size_x

        if CAR_Y > self.win_size_y:
            CAR_Y = - self.win_size_y

        if CAR_X > self.win_size_x:
            CAR_X = - self.win_size_x

        for i in range(num_rocks):
            if CAR_Y <= ROCKS[i].y <= CAR_Y + CAR_WIDTH and CAR_X - CAR_WIDTH <= ROCKS[i].x <= CAR_X + CAR_WIDTH:
                GAME_OVER = True

        glutPostRedisplay()

    def show_screen(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glColor3f(1, 1, 0)

        self.road()
        menu.score_text(950, 200)

        glColor3f(1, 0, 0)
        glPointSize(1)

        for i in range(num_rocks):  self.create_rock(ROCKS[i])

        glPointSize(1)

        score_text = Digits()
        digit_position = 900
        glColor3f(colors[0], colors[1], colors[2])

        for i in range(10, 50, 4):
            score_text.draw_digit(
                f"{SCORE}", offset_x=i, offset_y=i, digit_position_x=digit_position)

        glColor3f(colors[2], colors[1], colors[0])

        def transform():
            a = math.cos(math.radians(45))
            b = math.sin(math.radians(45))

            r = np.array([[a, -b],
                          [b, a]])

            v1 = np.array([[CAR_X + 90],[CAR_Y -10]])
            v2 = np.array([[CAR_X - 10],[CAR_Y -10]])
            v3 = np.array([[CAR_X - 10],[CAR_Y + 160]])
            v4 = np.array([[CAR_X + 90],[CAR_Y + 160]])

            # rotation
            
            v11 = np.matmul(r,v1)
            v22 = np.matmul(r,v2)
            v33 = np.matmul(r,v3)
            v44 = np.matmul(r,v4)

            glColor3f(0, 1, 0)
            glBegin(GL_QUADS)
            glVertex2f(v11[0][0], v11[1][0])
            glVertex2f(v22[0][0], v22[1][0])
            glVertex2f(v33[0][0], v33[1][0])
            glVertex2f(v44[0][0], v44[1][0])
            glEnd()
            # left bottom
            glColor3f(0, 1, 1)
            circle.filled_circle(20, v11[0][0], v11[1][0])
            # right bottom
            glColor3f(0, 1, 1)
            circle.filled_circle(20, v22[0][0], v22[1][0])
            # left top
            glColor3f(0, 1, 1)
            circle.filled_circle(20, v33[0][0], v33[1][0])
            # right top
            glColor3f(0, 1, 1)
            circle.filled_circle(20, v44[0][0], v44[1][0])

        # Car Design
        if GAME_OVER:
            glColor3f(0, 0, 1)
            glColor3f(1, 0, 0)
            menu.game_over_text(-650, 0)
      
            transform()
        else:
            glBegin(GL_QUADS)
            glColor3f(0, 1, 0)
            glVertex2f(CAR_X + 90, CAR_Y -10)
            glVertex2f(CAR_X - 10, CAR_Y -10)
            glVertex2f(CAR_X - 10, CAR_Y + 160)
            glVertex2f(CAR_X + 90, CAR_Y + 160)

            glEnd()
            # left bottom
            glColor3f(0, 1, 1)
            circle.filled_circle(20, CAR_X - 10, CAR_Y + 30)
            # right bottom
            glColor3f(0, 1, 1)
            circle.filled_circle(20, CAR_X + 90, CAR_Y + 30)
            # left top
            glColor3f(0, 1, 1)
            circle.filled_circle(20, CAR_X - 10, CAR_Y + 120)
            # right top
            glColor3f(0, 1, 1)
            circle.filled_circle(20, CAR_X + 90, CAR_Y + 120)

        glutSwapBuffers()
        glutMainLoop()

    def start(self):
        glutMainLoop()

    def road(self):
        left_x1, left_y1 = X_MIN_GLOBAL, Y_MIN_GLOBAL
        offset = -50

        line.midpoint(left_x1 + offset, left_y1, left_x1 + offset, Y_MAX_GLOBAL)
        line.midpoint(-left_x1 - offset, left_y1, -left_x1 - offset, Y_MAX_GLOBAL)

        for i in range(3):
            line.midpoint(left_x1 + offset + i, left_y1,
                          left_x1 + offset + i, Y_MAX_GLOBAL)
            line.midpoint(-left_x1 - offset - i, left_y1, -
            left_x1 - offset - i, Y_MAX_GLOBAL)

    def create_rock(self, rock):
        circle.midpoint_circle_algorithm(rock.radius, rock.x, rock.y)
        circle.filled_circle(rock.radius, rock.x, rock.y)


race = Race(win_size_x=1920, win_size_y=900, pixel_size=1)

race.initialize()
race.start()
