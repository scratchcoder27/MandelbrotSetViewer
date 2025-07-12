# SPDX-License-Identifier: MIT
"""
MANDELBROT SET RENDERER
A simple Mandelbrot set renderer using Pygame.

MIT License

Copyright (c) 2025 scratchcoder27

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell    
copies of the Software, and to permit persons to whom the Software is        
furnished to do so, subject to the following conditions:                     

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.                               

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
"""




import pygame
import colorsys
import threading
import sys
from time import time
from tkinter.messagebox import showerror
from traceback import format_tb
from decimal import Decimal, getcontext
from os import path, makedirs

getcontext().prec = 50

def get_exe_path():
    if getattr(sys, 'frozen', False):
        # Running as compiled .exe
        return path.dirname(sys.executable)
    else:
        # Running as script
        return path.dirname(path.abspath(__file__))


WIDTH, HEIGHT = 800, 600
RES = 1
ITERATIONS = 40
LIMIT = 2
COLOR = 36
DECIMALMODE = 0  # Set to True for higher precision calculations
stop_rendering = False

drawn = False
drawing = False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("The Mandelbrot Set")

try:
    font = pygame.font.SysFont("Agency FB", 16)
except Exception:
    font = pygame.font.Font(None, 16)

try:
    icon = pygame.image.load("Icon.ico")
    pygame.display.set_icon(icon)
except Exception as e:
    print(f"Failed to load window icon: {e}")

clock = pygame.time.Clock()

mWIDTh, mHEIGHT = int(800/RES), int(600/RES)
mSurface = pygame.Surface((mWIDTh, mHEIGHT))


center_x, center_y = -0.5, 0.0
zoom = 1.0

def get_real_imaginary(x, y):
    global mWIDTh, mHEIGHT
    scale_x = 3.5 / zoom
    scale_y = 3.0 / zoom
    real = center_x + (x / mWIDTh - 0.5) * scale_x
    imag = center_y + (y / mHEIGHT - 0.5) * scale_y

    return real, imag

def calculate(x, y) -> tuple:
    global mWIDTh, mHEIGHT, LIMIT, ITERATIONS, zoom


    fz = complex(0, 0)

    real, imag = get_real_imaginary(x, y)

    c = complex(real, imag)

    i = 0
    for i in range(ITERATIONS):
        if abs(fz) > LIMIT:
            return (True, i)
        
        fz = fz * fz + c
    
    return (False, i-1)

def decimal_calculate(x, y) -> tuple:
    global mWIDTh, mHEIGHT, LIMIT, ITERATIONS, zoom, center_x, center_y

    fz_real = Decimal(0)
    fz_imag = Decimal(0)

    scale_x = Decimal('3.5') / Decimal(zoom)
    scale_y = Decimal('3.0') / Decimal(zoom)
    real = Decimal(center_x) + (Decimal(x) / Decimal(mWIDTh) - Decimal('0.5')) * scale_x
    imag = Decimal(center_y) + (Decimal(y) / Decimal(mHEIGHT) - Decimal('0.5')) * scale_y

    c_real = real
    c_imag = imag

    i = 0
    while i < ITERATIONS:
        # |fz|^2 = real^2 + imag^2
        mag_squared = fz_real * fz_real + fz_imag * fz_imag
        if mag_squared > Decimal(LIMIT) * Decimal(LIMIT):
            return (True, i)
        
        # fz = fz^2 + c
        temp_real = fz_real * fz_real - fz_imag * fz_imag + c_real
        temp_imag = Decimal(2) * fz_real * fz_imag + c_imag
        fz_real = temp_real
        fz_imag = temp_imag

        i += 1

    return (False, i - 1)

def clamp(value, min_value, max_value):
    try:
        return max(min_value, min(value, max_value))
    except TypeError:
        return (min_value)

def scale_color(iter: int, escape : bool) -> tuple:

    # hue = iter / ITERATIONS  # Normalized [0.0, 1.0]
    hue = (((iter + COLOR) * 4) % 256) / 256

    saturation = 1.0
    value = ((iter) / ITERATIONS) ** 0.5
    # value = (iter / ITERATIONS)
    value = clamp(value, 0, 1)

    if not escape:
        value = 0


    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return (int(r * 255), int(g * 255), int(b * 255))



def update():
    global drawn, drawing, stop_rendering

    if not drawn:
        drawing = True
        for y in range(mHEIGHT):
            for x in range(mWIDTh):
                if stop_rendering:
                    drawing = False
                    return

                if DECIMALMODE:
                    color, iter = decimal_calculate(x, y)
                else:
                    color, iter = calculate(x, y)
                mSurface.set_at((x, y), scale_color(iter, color))

        # print("Drawing done", end=" ")
        drawing = False
        drawn = True
            

def draw():
    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.scale(mSurface, (WIDTH, HEIGHT)), (0, 0))
    
    screen.blit(font.render(f"Position: {tuple(map((lambda q : (int(q*10000)/10000)), get_real_imaginary(mWIDTh // 2, mHEIGHT // 2)))}", True, (255, 255, 255)), (10, 10))

def set_res(res):
    global RES, mWIDTh, mHEIGHT, mSurface
    if res < 0.01:
        res = 0.01
    RES = res
    mWIDTh, mHEIGHT = int(800/RES), int(600/RES)
    mSurface = pygame.transform.scale(mSurface, (mWIDTh, mHEIGHT))

keyboard_timer = 0
def interact():
    global center_x, center_y, zoom, drawn, RES, mWIDTh, mHEIGHT, mSurface, COLOR, ITERATIONS, RES, keyboard_timer, DECIMALMODE
    keys = pygame.key.get_pressed()

    if keyboard_timer > 0:
        keyboard_timer -= 1

    move_speed = 0.1 / zoom  # Move less when zoomed in

    if keys[pygame.K_w]: center_y -= move_speed
    if keys[pygame.K_s] and not (keys[pygame.K_LCTRL]): center_y += move_speed
    if keys[pygame.K_a]: center_x -= move_speed
    if keys[pygame.K_d]: center_x += move_speed

    if keys[pygame.K_q]: zoom *= 1.1
    if keys[pygame.K_e]: zoom /= 1.1

    if keys[pygame.K_n]: COLOR += 1
    if keys[pygame.K_m]: COLOR -= 1

    if keys[pygame.K_UP]: ITERATIONS += 1
    if (keys[pygame.K_DOWN] and ITERATIONS >= 3): ITERATIONS -= 1
    if keys[pygame.K_LEFT]: set_res(RES - 0.01)
    if keys[pygame.K_RIGHT]: set_res(RES + 0.01)
    
    if keys[pygame.K_r]: center_x, center_y, zoom = -0.5, 0.0, 1.0
    if keys[pygame.K_i]:set_res(5)
    if keys[pygame.K_SPACE]:set_res(0.5)
    if (keys[pygame.K_0] and keyboard_timer <= 0):
        DECIMALMODE = not DECIMALMODE
        keyboard_timer = 10

    # When the viewport changes, re-trigger drawing
    if any(keys): # Not save
        drawn = False

    if keys[pygame.K_LCTRL] and keys[pygame.K_s]:
        base_path = get_exe_path()
        save_dir = path.join(base_path, "saves")

        # Ensure the folder exists
        makedirs(save_dir, exist_ok=True)

        with open(f"saves\\{int(time())}.png", "wb") as f:
            pygame.image.save(screen, f, "PNG")

        print("Saved mandelbrot.png")
        pygame.time.delay(1000)

event_thread = threading.Thread(target=update)
while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_rendering = True
                if event_thread.is_alive():
                    event_thread.join()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        if not drawn and not drawing and not event_thread.is_alive():
            stop_rendering = False
            event_thread = threading.Thread(target=update)
            event_thread.start()

        interact()
        draw()

        pygame.display.flip()
        clock.tick(60)
    
    except Exception as e:
        showerror("Error", f"Data(For developers):\n Error: {e} \nTraceback:\n{"".join(format_tb(e.__traceback__))}")
        print(f"Data(For developers):\n Error: {e} \nTraceback:\n{"".join(format_tb(e.__traceback__))}")
        pygame.quit()
        sys.exit()