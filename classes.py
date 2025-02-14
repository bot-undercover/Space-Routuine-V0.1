import pygame as pg

size = 60


def checkRotation(angle):
    if type(angle) == int:
        return angle
    else:
        if angle.isdigit():
            return int(angle)
        else:
            if angle.lower() == "top":
                return -90
            elif angle.lower() == "left":
                return 180
            elif angle.lower() == "down":
                return 90
            else:
                return 0


class Sprite:
    def __init__(self, image, rot=0, mask=None):
        self.image = pg.transform.scale(image, (size, size))
        self.rotation = checkRotation(rot)
        if mask:
            self.mask = mask

    def getNew(self, angle=0):
        return Sprite(self.image, checkRotation(angle), True)

    def get(self, angle=None):
        if angle:
            return pg.transform.rotate(self.image, checkRotation(angle))
        else:
            return pg.transform.rotate(self.image, checkRotation(self.rotation))

    def getMask(self, angle=None):
        if self.mask is True:
            self.mask = pg.mask.from_surface(self.get())
            print(self.rotation)
        return self.mask


class Sprites:
    def __init__(self, paths):
        self.sprites = [pg.image.load(path) for path in paths]
        self.count = 0

    def get(self, angle=0):
        self.count += 1
        if self.count >= len(self.sprites):
            self.count = 0
        return list(map(lambda x: pg.transform.rotate(x, checkRotation(angle)), self.sprites))[self.count - 1]
