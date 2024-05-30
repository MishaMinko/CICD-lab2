
class Token:
    def __init__(self, image, pos, action):
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = self.pos
        self.action = action

    def draw(self, window):
        window.blit(self.image, self.rect)
