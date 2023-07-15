import pygame
import sys
from settings import *
# from debug import debug
from level import Level

'''
Classe Game
Responsável por lidar com eventos de mais auto nível do jogo. 
Por exemplo, checar se o jogar fechou o jogo ou não, ou se vai entrar em modo full screen ou vai sair dele
'''

class Game:

    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('Eugor')
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('gray')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
