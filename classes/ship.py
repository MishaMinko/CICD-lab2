import pygame

class Ship:
    def __init__(self, name, img, pos, size, numGuns=0, gunPath=None, gunSize=None, gunCoords=None):
        self.name = name
        #vertical image
        self.vImage = loadImage(img, size)
        self.vImageWidth = self.vImage.get_width()
        self.vImageHeight = self.vImage.get_height()
        self.vImageRect = self.vImage.get_rect()
        self.vImageRect.topleft = pos
        #horizontal image
        self.hImage = pygame.transform.rotate(self.vImage, -90)
        self.hImageWidth = self.hImage.get_width()
        self.hImageHeight = self.hImage.get_height()
        self.hImageRect = self.hImage.get_rect()
        self.hImageRect.topleft = pos
        #image
        self.image = self.vImage
        self.rect = self.vImageRect
        self.rotation = False
        #guns
        self.gunList = []
        if numGuns > 0:
            self.gunCoords = gunCoords
            for i in range(numGuns):
                self.gunList.append(Guns(gunPath, self.rect.center, (size[0] * gunSize[0], size[1] * gunSize[1]), self.gunCoords[i]))

    
    def draw(self, window):
        window.blit(self.image, self.rect)
        for guns in self.gunList:
            guns.draw(window, self)


class Guns:
    def __init__(self, imgPath, pos, size, offset):
        self.orig_image = loadImage(imgPath, size, True)
        self.image = self.orig_image
        self.offset = offset
        self.rect = self.image.get_rect(center=pos)


    def update(self, ship):
        if ship.rotation == False:
            self.rect.center = (ship.rect.centerx, ship.rect.centery + (ship.image.get_height()//2 * self.offset))
            self.image = pygame.transform.rotate(self.orig_image, -270)
        else:
            self.rect.center = (ship.rect.centerx + (ship.image.get_width()//2 * -self.offset), ship.rect.centery)
            self.image = pygame.transform.rotate(self.orig_image, -0)
        self.rect = self.image.get_rect(center=self.rect.center)


    def draw(self, window, ship):
        self.update(ship)
        window.blit(self.image, self.rect)



#functions to work
def loadImage(path, size, rotate=False):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    if rotate == True:
        img = pygame.transform.rotate(img, -90)
    return img