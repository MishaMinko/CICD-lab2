import pygame

class Ship:
    def __init__(self, globals, name, img, pos, size, numGuns=0, gunPath=None, gunSize=None, gunCoords=None):
        self.globals = globals

        self.name = name
        self.pos = pos
        #vertical image
        self.vImage = self.globals['loadImage'](img, size)
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
        self.active = False
        #guns
        self.gunList = []
        if numGuns > 0:
            self.gunCoords = gunCoords
            for i in range(numGuns):
                self.gunList.append(Guns(gunPath, self.rect.center, (size[0] * gunSize[0], size[1] * gunSize[1]), self.gunCoords[i], self.globals['loadImage']))

    
    def selectShipAndMove(self, shiplist):
        while self.active == True:
            self.rect.center = pygame.mouse.get_pos()
            self.globals['updateGameScreen'](self.globals['GAMESCREEN'])
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.checkForCollisions(shiplist):
                        if event.button == 1:
                            self.hImageRect.center = self.vImageRect.center = self.rect.center
                            self.active = False

                    if event.button == 3:
                        self.rotateShip()
    

    def rotateShip(self, doRotation=False):
        if self.active or doRotation == True:
            if self.rotation == False:
                self.rotation = True
            else:
                self.rotation = False
            self.rotateImageAndRect()


    def rotateImageAndRect(self):
        if self.rotation == True:
            self.image = self.hImage
            self.rect = self.hImageRect
        else:
            self.image = self.vImage
            self.rect = self.vImageRect
        self.hImageRect.center = self.vImageRect.center = self.rect.center


    def checkForCollisions(self, shiplist):
        slist = shiplist.copy()
        slist.remove(self)
        for item in slist:
            if self.rect.colliderect(item.rect):
                return True
        return False


    def setDefaultPosition(self):
        if self.rotation == True:
            self.rotateShip(True)

        self.rect.topleft = self.pos
        self.hImageRect.center = self.vImageRect.center = self.rect.center


    def magnetToGridEdge(self, gridCoords, CELLSIZE):
        if self.rect.left > gridCoords[0][-1][0] + CELLSIZE or \
            self.rect.right < gridCoords[0][0][0] or \
            self.rect.top > gridCoords[-1][0][1] + CELLSIZE or \
            self.rect.bottom < gridCoords[0][0][1]:
            self.setDefaultPosition()

        elif self.rect.right > gridCoords[0][-1][0] + CELLSIZE:
            self.rect.right = gridCoords[0][-1][0] + CELLSIZE
        elif self.rect.left < gridCoords[0][0][0]:
            self.rect.left = gridCoords[0][0][0]
        elif self.rect.top < gridCoords[0][0][1]:
            self.rect.top = gridCoords[0][0][1]
        elif self.rect.bottom > gridCoords[-1][0][1] + CELLSIZE:
            self.rect.bottom = gridCoords[-1][0][1] + CELLSIZE
        self.vImageRect.center = self.hImageRect.center = self.rect.center


    def magnetToGrid(self, gridCoords, CELLSIZE):
        for rowX in gridCoords:
            for cell in rowX:
                if self.rect.left >= cell[0] and self.rect.left < cell[0] + CELLSIZE \
                    and self.rect.top >= cell[1] and self.rect.top < cell[1] + CELLSIZE:
                    if self.rotation == False:
                        self.rect.topleft = (cell[0] + (CELLSIZE - self.image.get_width())//2, cell[1])
                    else:
                        self.rect.topleft = (cell[0], cell[1] + (CELLSIZE - self.image.get_height())//2)

        self.hImageRect.center = self.vImageRect.center = self.rect.center 


    def draw(self, window):
        window.blit(self.image, self.rect)
        for guns in self.gunList:
            guns.draw(window, self)


class Guns:
    def __init__(self, imgPath, pos, size, offset, loadImage):
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