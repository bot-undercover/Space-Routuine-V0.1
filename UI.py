from pygame_widgets.button import *
import os
from pygame_widgets.slider import Slider


def mainMenu(screen):
    widgets = []
    widgets.append(Button(
        screen,
        100,
        30,
        200,
        80,
        text='Новая игра',
        fontSize=30,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3,
        radius=20
    ))
    widgets.append(Button(
        screen,
        100,
        150,
        200,
        80,
        text='Сохранения',
        fontSize=30,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3,
        radius=20
    ))
    widgets.append(Button(
        screen,
        100,
        270,
        200,
        80,
        text='Настройки',
        fontSize=30,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3,
        radius=20
    ))
    widgets.append(Button(
        screen,
        100,
        390,
        200,
        80,
        text='Выход',
        fontSize=30,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3,
        radius=20,
        onClick=lambda: exit(0)
    ))
    return widgets


def settings(screen):
    widgets = []
    widgets.append(Button(
        screen,
        0,
        0,
        100,
        40,
        text='Назад',
        fontSize=30,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3,
        radius=20
    ))
    return widgets


def saves(screen):
    widgets = []
    widgets.append(Button(
        screen,
        0,
        0,
        100,
        40,
        text='Назад',
        fontSize=30,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3,
        radius=20
    ))
    if os.listdir("./saves/") != []:
        widgets.append(ButtonArray(
            screen, 0, 50, 800, 200, (4, 2), border=10,
            texts=[os.listdir("./saves/")[a] if len(os.listdir("./saves/")) > a else "Пустое сохранение" for a in
                   range(8)]
        ))
    else:
        font = pygame.font.SysFont('Comic Sans MS', 30)
        surf = font.render('Сохранения отсутствуют', False, [255] * 3)
        screen.blit(surf, (210, 200))
    return widgets


SCREEN_SIZE = [1200, 750]


def InGameSettings(screen):
    widgets = []
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] - 110,
        10,
        100,
        40,
        text='Сохранить',
        fontSize=20,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3,
        radius=20
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 60,
        35,
        30,
        30,
        text='/\\',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 92,
        35,
        30,
        30,
        text='/\\',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 124,
        35,
        30,
        30,
        text='/\\',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 156,
        35,
        30,
        30,
        text='/\\',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 188,
        35,
        30,
        30,
        text='/\\',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 220,
        35,
        30,
        30,
        text='/\\',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 60,
        90,
        30,
        30,
        text='\\/',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 92,
        90,
        30,
        30,
        text='\\/',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 124,
        90,
        30,
        30,
        text='\\/',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 156,
        90,
        30,
        30,
        text='\\/',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 188,
        90,
        30,
        30,
        text='\\/',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 220,
        90,
        30,
        30,
        text='\\/',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 60,
        125,
        30,
        30,
        text='/\\',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 92,
        125,
        30,
        30,
        text='/\\',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 124,
        125,
        30,
        30,
        text='/\\',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 156,
        125,
        30,
        30,
        text='/\\',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 188,
        125,
        30,
        30,
        text='/\\',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 220,
        125,
        30,
        30,
        text='/\\',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 60,
        180,
        30,
        30,
        text='\\/',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 92,
        180,
        30,
        30,
        text='\\/',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 124,
        180,
        30,
        30,
        text='\\/',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 156,
        180,
        30,
        30,
        text='\\/',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 188,
        180,
        30,
        30,
        text='\\/',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Button(
        screen,
        SCREEN_SIZE[0] * 0.6 + 220,
        180,
        30,
        30,
        text='\\/',
        fontSize=15,
        margin=20,
        inactiveColour=[128] * 3,
        hoverColour=[100] * 3,
        pressedColour=[80] * 3
    ))
    widgets.append(Slider(screen, SCREEN_SIZE[0] * 0.6 + 80, 250, 350, 20, min=2, max=33, step=1))
    widgets.append(Slider(screen, SCREEN_SIZE[0] * 0.6 + 80, 310, 350, 20, min=0, max=999, step=1))
    return widgets
