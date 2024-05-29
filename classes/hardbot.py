import random
import pygame
from classes.easybot import EasyComputer
from classes.tokens import Token

class HardComputer(EasyComputer):
    def __init__(self, globals):
        super().__init__(globals)
        self.moves = []


    def makeAttack(self, gamelogic):
        if len(self.moves) == 0:
            COMPTURNTIMER = pygame.time.get_ticks()
            if COMPTURNTIMER - self.globals['TURNTIMER'] >= 3000:
                validChoice = False
                while not validChoice:
                    rowX = random.randint(0, 9)
                    rowY = random.randint(0, 9)

                    if gamelogic[rowX][rowY] == ' ' or gamelogic[rowX][rowY] == 'O':
                        validChoice = True

                if gamelogic[rowX][rowY] == 'O':
                    self.globals['TOKENS'].append(Token(self.globals['REDTOKEN'], self.globals['pGameGrid'][rowX][rowY], 'Hit'))
                    gamelogic[rowX][rowY] = 'T'
                    self.generateMoves((rowX, rowY), gamelogic)
                else:
                    gamelogic[rowX][rowY] = 'X'
                    self.globals['TOKENS'].append(Token(self.globals['BLUETOKEN'], self.globals['pGameGrid'][rowX][rowY], 'Miss'))
                self.turn = False

        elif len(self.moves) > 0:
            COMPTURNTIMER = pygame.time.get_ticks()
            if COMPTURNTIMER - self.globals['TURNTIMER'] >= 2000:
                rowX, rowY = self.moves[0]
                self.globals['TOKENS'].append(Token(self.globals['REDTOKEN'], self.globals['pGameGrid'][rowX][rowY], 'Hit'))
                gamelogic[rowX][rowY] = 'T'
                self.moves.remove((rowX, rowY))
                self.turn = False
        return self.turn


    def generateMoves(self, coords, grid, lstDir=None):
        x, y = coords
        nx, ny = 0, 0
        for direction in ['North', 'South', 'East', 'West']:
            if direction == 'North' and lstDir != 'North':
                nx = x - 1
                ny = y
                if not (nx > 9 or ny > 9 or nx < 0 or ny < 0):
                    if (nx, ny) not in self.moves and grid[nx][ny] == 'O':
                        self.moves.append((nx, ny))
                        self.generateMoves((nx, ny), grid, 'South')

            if direction == 'South' and lstDir != 'South':
                nx = x + 1
                ny = y
                if not (nx > 9 or ny > 9 or nx < 0 or ny < 0):
                    if (nx, ny) not in self.moves and grid[nx][ny] == 'O':
                        self.moves.append((nx, ny))
                        self.generateMoves((nx, ny), grid, 'North')

            if direction == 'East' and lstDir != 'East':
                nx = x
                ny = y + 1
                if not (nx > 9 or ny > 9 or nx < 0 or ny < 0):
                    if (nx, ny) not in self.moves and grid[nx][ny] == 'O':
                        self.moves.append((nx, ny))
                        self.generateMoves((nx, ny), grid, 'West')

            if direction == 'West' and lstDir != 'West':
                nx = x
                ny = y - 1
                if not (nx > 9 or ny > 9 or nx < 0 or ny < 0):
                    if (nx, ny) not in self.moves and grid[nx][ny] == 'O':
                        self.moves.append((nx, ny))
                        self.generateMoves((nx, ny), grid, 'East')