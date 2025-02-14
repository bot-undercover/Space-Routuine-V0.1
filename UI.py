from pygame_widgets.button import *
import os


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
        texts=[os.listdir("./saves/")[a] if len(os.listdir("./saves/")) > a else "Пустое сохранение" for a in range(8)]
        ))
    else:
        font = pygame.font.SysFont('Comic Sans MS', 30)
        surf = font.render('Сохранения отсутствуют', False, [255] * 3)
        screen.blit(surf, (210, 200))
    return widgets