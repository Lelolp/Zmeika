import pygame
import random
import msvcrt
import time
import os


def if_control():
    global hp, pelmeni, xp, yp, xd, yd
    if xp == 0:
        hp -= 1
    if xp == widht - 1:
        hp -= 1
    if yp == 0:
        hp -= 1
    if yp == height - 1:
        hp -= 1
    if xp == xd and yp == yd:
        xd = random.randint(1, widht - 2)
        yd = random.randint(1, height - 2)
        pelmeni += 1


def ded_control():
    global xv, yv, xp, yp, hp
    if msvcrt.kbhit():
        ch = msvcrt.getch().decode('utf-8')
        if ch == "w":
            yv = -1
            xv = 0
        elif ch == "s":
            yv = 1
            xv = 0
        elif ch == "a":
            xv = -1
            yv = 0
        elif ch == "d":
            xv = 1
            yv = 0
        elif ch == "p":
            pause = True
            while pause:
                if msvcrt.kbhit():
                    pause = False
    xp += xv
    yp += yv
    # if hp >= 0:


def screen_control():
    global height, widht, yp, xp, xd, yd
    time.sleep(0.2)
    os.system("cls")

    for y in range(height):
        for x in range(widht):
            if x == 0 or x == widht - 1 or y == 0 or y == height - 1:
                print("🧱", end="")
            elif x == xp and y == yp:
                print("🐱", end="")
            elif x == xd and y == yd:
                print("🥟", end="")
            else:
                print("🟦", end="")

        print()


widht = 30
height = 15
xp = 10
yp = 10
xv = 0
yv = 0
hp = 1
pelmeni = 0
xd = random.randint(1, widht - 2)
yd = random.randint(1, height - 2)

pygame.init()
pygame.mixer.music.load("C:/Users\danik\PycharmPygame\SUPER ZMEIKA\zmeiground.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

while hp > 0:
    ded_control()

    if_control()

    screen_control()
