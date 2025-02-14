import pygame as pg

from usefulClasses import *
from resources.datapack import SPRITES
from UI import *
import pygame_widgets
import functools

NAME = "Space Routuine V0.1"
startingLV = "---"


def MainGameUpdate(screen):
    global updateState, widgets, page
    page = "GAME"
    widgets = []
    updateState = True
    pygame.font.init()
    pg.display.flip()
    pg.display.set_caption(NAME)
    clock = pg.time.Clock()
    while True:
        pg.display.set_caption(NAME + " " + str(round(clock.get_fps(), 1)))
        eventCheck(pg.event.get())
        if page.isdigit():
            menu(screen)
        else:
            updateGame(screen)
        pg.display.flip()
        clock.tick(60)


def eventCheck(events):
    global running
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN and page.isdigit():
            if event.key == pg.K_ESCAPE:
                ret("0")
        if not page.isdigit():
            pg.key.set_repeat(True)
            data = pg.key.get_pressed()
            global player, mapGame
            if player:
                player.move(data, mapGame)

    pygame_widgets.update(events)


def updateGame(screen):
    global updateState, page, mapGame, player
    screen.fill([0] * 3)
    if updateState:
        updateState = False
        mapGame = Map(LEVEL)
        player = Player(pos=[1, 1])
    mapGame.show(screen)
    player.drawPlayer(screen)


def menu(screen):
    global updateState, widgets, page, LEVEL
    if updateState:
        updateState = False
        screen.blit(pg.transform.scale(SPRITES["background"].get(), SCREEN_SIZE), (0, 0))
        widgets.clear()
        if page == "0":
            widgets = mainMenu(screen)
            [widgets[a].setOnClick(functools.partial(lambda x: ret(x), str(a + 1))) for a in range(0, 3)]
        elif page == "1":
            ret("GAME")
        elif page == "2":
            widgets = saves(screen)
            widgets[0].setOnClick(lambda: ret("0"))
            if len(widgets) > 1:
                [a.setOnClick(
                    functools.partial(lambda x: loadMap(x.string), a)) if a.string != "Пустое сохранение" else None for
                 a in widgets[1].buttons]
        elif page == "3":
            widgets = settings(screen)
            widgets[0].setOnClick(lambda: ret("0"))
    list(map(lambda x: x.draw(), widgets))


def loadMap(name):
    print(f"Nothing happend. Just check {name} map.")
    # map = Map()
    #
    # #map.importObject((0, 0), FLOOR)
    # player = Player()
    # if map.map == None:
    #     print("Map import ERROR")
    #     exit(0)


def ret(newPage):
    global page, updateState
    page = newPage
    updateState = True


if __name__ == "__main__":
    clock = pg.time.Clock()
    pg.init()
    player = None
    LEVEL = startingLV
    visitCard = "~DELETED~"
    MainGameUpdate(pg.display.set_mode(SCREEN_SIZE))
pg.init()
