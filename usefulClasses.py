import json, pygame as pg
from resources.datapack import SPRITES
from classes import *

SCREEN_SIZE = (800, 500)


class Map:
    def __init__(self, level="CUSTOM", size=[0, 0]):
        self.mapSprites = pg.sprite.Group()
        if level != "CUSTOM":
            with open("./resources/levels/" + level + ".json") as f:
                level = json.load(f)

                self.background = [[[] for _ in range(level["size"][1])] for _ in range(level["size"][0])]
                for layers in level["levelBackground"]:
                    for x in range(layers[0][0], layers[1][0]):
                        for y in range(layers[0][1], layers[1][1]):
                            self.background[x][y].append(SPRITES[layers[2]].getNew())

                self.map = [[[] for _ in range(level["size"][1])] for _ in range(level["size"][0])]
                for level, mapBlocks in level["level"].items():
                    for pos, blocks in mapBlocks.items():
                        x, y = list(map(int, pos.split("/")))
                        for block in blocks:
                            block, rotation = block
                            self.map[x][y].append(SPRITES[block.upper()].getNew(rotation))
        else:
            if 0 not in size:
                self.map = [[None for _ in range(size[1])] for _ in range(size[0])]
            else:
                self.map = None

    def importObject(self, pos, object):
        self.map[pos[0]][pos[1]] = object

    def show(self, screen):
        for x, data in enumerate(self.background):
            for y, blocks in enumerate(data):
                if blocks:
                    for block in blocks:
                        pass
                        #screen.blit(block.get(), (x * size, y * size))
        for x, data in enumerate(self.map):
            for y, blocks in enumerate(data):
                if blocks:
                    for block in blocks:
                        screen.blit(block.getMask().to_surface(), (x * size, y * size))
                        #screen.blit(block.get(), (x * size, y * size))

    def getColides(self, posPlayer):
        """Возвращает список прямоугольников для всех блоков на карте."""
        sprites = []
        for x, row in enumerate(self.map):
            for y, blocks in enumerate(row):
                for block in blocks:
                    sprites.append([block.getMask(), (abs((x * size) - posPlayer[0]), abs((y * size) - posPlayer[1]))])
        return sprites


class Player:
    def __init__(self, pos=[0, 0], rotation=0, health=100, oxygen=0, inventory=[], costume=None):
        self.pos, self.health, self.oxygen, self.inventory, self.rotation = list(map(lambda x: x * size, pos)), health, oxygen, inventory, rotation
        self.costumeUsing = costume
        self.count = 0
        self.player = SPRITES["PLAYER"].getNew(self.rotation)


    def updateOxygen(self):
        if self.count >= 30:
            if not self.costumeUsing:
                self.oxygen -= 1
            elif self.costumeUsing:
                self.oxygen += 1
            self.count = 0
        if self.costumeUsing != None:
            self.count += 1

    def drawPlayer(self, screen):
        screen.blit(self.player.get(), (self.pos[0], self.pos[1]))

    def move(self, data, map):
        """Перемещает игрока с учетом коллизий."""
        new_pos = self.pos[:]  # Создаем копию текущей позиции
        speed = 0.5
        if data[pg.K_w] or data[pg.K_UP]:
            new_pos[1] -= speed
        if data[pg.K_s] or data[pg.K_DOWN]:
            new_pos[1] += speed
        if data[pg.K_a] or data[pg.K_LEFT]:
            new_pos[0] -= speed
        if data[pg.K_d] or data[pg.K_RIGHT]:
            new_pos[0] += speed
        if not any([self.player.getMask().overlap(*data) for data in map.getColides(new_pos)]):
            self.pos = new_pos


    def update(self):
        self.updateOxygen()