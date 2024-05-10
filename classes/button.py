import pygame

class Button:
    def __init__(self, image, size, pos, msg):
        self.name = msg
        self.image = image
        self.imageLarger = self.image
        self.imageLarger = pygame.transform.scale(self.imageLarger, (size[0] + 10, size[1] + 10))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.msg = self.addText(msg)
        self.msgRect = self.msg.get_rect(center=self.rect.center)

    
    def addText(self, msg):
        font = pygame.font.SysFont('Stencil', 22)
        message = font.render(msg, 1, (255, 255, 255))
        return message
    

    def focusOnButton(self, window):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            window.blit(self.imageLarger, (self.rect[0] - 5, self.rect[1] - 5, self.rect[2], self.rect[3]))
        else:
            window.blit(self.image, self.rect)

    
    def updateButtons(self, gameStatus):
        if self.name == 'Deploy' and gameStatus == False:
            self.name = 'Quit'
        elif self.name == 'Quit' and gameStatus == True:
            self.name = 'Deploy'
        if self.name == 'Randomize' and gameStatus == False:
            self.name = 'Redeploy'
        elif self.name == 'Redeploy' and gameStatus == True:
            self.name = 'Randomize'
        self.msg = self.addText(self.name)
        self.msgRect = self.msg.get_rect(center=self.rect.center)


    def draw(self, window, DEPLOYMENT):
        if self.name == 'Reset' and DEPLOYMENT == False:
            return

        self.updateButtons(DEPLOYMENT)
        self.focusOnButton(window)
        window.blit(self.msg, self.msgRect)