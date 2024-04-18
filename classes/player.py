import pygame
from classes.tokens import Token

class Player:
    def __init__(self, globals):
        self.globals = globals
        self.turn = True
    
    def makeAttack(self, grid, logicgrid):
        posX, posY = pygame.mouse.get_pos()
        if posX >= grid[0][0][0] and posX <= grid[0][-1][0] + 50 and posY >= grid[0][0][1] and posY <= grid[-1][0][1] + 50:
            for i, rowX in enumerate(grid):
                for j, colX in enumerate(rowX):
                    if posX >= colX[0] and posX < colX[0] + 50 and posY >= colX[1] and posY <= colX[1] + 50:
                        if logicgrid[i][j] != ' ':
                            if logicgrid[i][j] == 'O':
                                self.globals['TOKENS'].append(Token(self.globals['REDTOKEN'], grid[i][j], 'Hit'))
                                logicgrid[i][j] = 'T'
                                self.turn = False
                        else:
                            self.globals['TOKENS'].append(Token(self.globals['GREENTOKEN'], grid[i][j], 'Hit'))
                            logicgrid[i][j] = 'X'
                            self.turn = False