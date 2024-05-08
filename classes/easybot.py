import random
import pygame

class EasyComputer:
    def __init__(self):
        self.turn = False
        self.status = self.computerStatus('Thinking')
        self.name = 'Easy Computer'


    def computerStatus(self, msg):
        image = pygame.font.SysFont('Stencil', 22)
        message = image.render(msg, 1, (0, 0, 0))
        return message


    def makeAttack(self, gamelogic):
        COMPTURNTIMER = pygame.time.get_ticks()
        if COMPTURNTIMER - TURNTIMER >= 3000:
            validChoice = False
            while not validChoice:
                rowX = random.randint(0, 9)
                colX = random.randint(0, 9)

                if gamelogic[rowX][colX] == ' ' or gamelogic[rowX][colX] == 'O':
                    validChoice = True

            if gamelogic[rowX][colX] == 'O':
                TOKENS.append(Tokens(REDTOKEN, pGameGrid[rowX][colX], 'Hit', FIRETOKENIMAGELIST, EXPLOSIONIMAGELIST, None))
                gamelogic[rowX][colX] = 'T'
                SHOTSOUND.play()
                HITSOUND.play()
                self.turn = False
            else:
                gamelogic[rowX][colX] = 'X'
                TOKENS.append(Tokens(BLUETOKEN, pGameGrid[rowX][colX], 'Miss', None, None, None))
                SHOTSOUND.play()
                MISSSOUND.play()
                self.turn = False
        return self.turn


    def draw(self, window):
        if self.turn:
            window.blit(self.status, (cGameGrid[0][0][0] - CELLSIZE, cGameGrid[-1][-1][1] + CELLSIZE))