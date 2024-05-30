import random
import pygame
from classes.tokens import Token


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
                self.globals['TOKENS'].append(Token(self.globals['REDTOKEN'], self.globals['pGameGrid'][rowX][colX], 'Hit'))
                gamelogic[rowX][colX] = 'T'
                self.turn = False
            else:
                gamelogic[rowX][colX] = 'X'
                self.globals['TOKENS'].append(Token(self.globals['BLUETOKEN'], self.globals['pGameGrid'][rowX][colX], 'Miss'))
                self.turn = False
        return self.turn

    def draw(self, window):
        if self.turn:
            window.blit(self.status, (self.globals['cGameGrid'][0][0][0] - self.globals['CELLSIZE'], self.globals['cGameGrid'][-1][-1][1] + self.globals['CELLSIZE']))
