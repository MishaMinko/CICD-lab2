import pygame

class Button:
    def __init__(self, image, size, pos, msg):
        self.name = msg
        self.image = image
        self.imageLarger = self.image
        self.imageLarger = pygame.transform.scale(self.imageLarger, (size[0] + 10, size[1] + 10))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.active = False

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


    def draw(self, window):
        self.focusOnButton(window)
        window.blit(self.msg, self.msgRect)