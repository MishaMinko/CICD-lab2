import random
import pygame

class EasyComputer:
    def __init__(self, globals):
        self.globals = globals
        self.turn = False
        self.status = self.computerStatus('Thinking')
        self.name = 'Easy Computer'


    def computerStatus(self, msg):
        image = pygame.font.SysFont('Stencil', 22)
        message = image.render(msg, 1, (0, 0, 0))
        return message


    def makeAttack(self, gamelogic):
        COMPTURNTIMER = pygame.time.get_ticks()
        if COMPTURNTIMER - self.globals['TURNTIMER'] >= 3000:
            validChoice = False
            while not validChoice:
                rowX = random.randint(0, 9)
                colX = random.randint(0, 9)

                if gamelogic[rowX][colX] == ' ' or gamelogic[rowX][colX] == 'O':
                    validChoice = True

            if gamelogic[rowX][colX] == 'O':
                self.globals['TOKENS'].append(self.globals['Tokens'](self.globals['REDTOKEN'], self.globals['pGameGrid'][rowX][colX], 'Hit', self.globals['FIRETOKENIMAGELIST'], self.globals['EXPLOSIONIMAGELIST'], None))
                gamelogic[rowX][colX] = 'T'
                self.globals['SHOTSOUND'].play()
                self.globals['HITSOUND'].play()
                self.turn = False
            else:
                gamelogic[rowX][colX] = 'X'
                self.globals['TOKENS'].append(self.globals['Tokens'](self.globals['BLUETOKEN'], self.globals['pGameGrid'][rowX][colX], 'Miss', None, None, None))
                self.globals['SHOTSOUND'].play()
                self.globals['MISSSOUND'].play()
                self.turn = False
        return self.turn


    def draw(self, window):
        if self.turn:
            window.blit(self.status, (self.globals['cGameGrid'][0][0][0] - self.globals['CELLSIZE'], self.globals['cGameGrid'][-1][-1][1] + self.globals['CELLSIZE']))
