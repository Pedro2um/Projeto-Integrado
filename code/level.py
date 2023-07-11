import random

import pygame
from support import *
from settings import *
from tile import Tile
from player import Player
from enemy import Enemy
from entity import Entity
from random import choice
from ui import UI
from map_gen import generate_map


class Level(pygame.sprite.Sprite):
    def __init__(self):
        self.player = None
        self.display_surface = pygame.display.get_surface()

        self.player_group = pygame.sprite.Group()
        self.visible_sprites = Camera()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.total_enemies_of_level = 0
        self.total_enemies_of_game = 0

        self.new_map()

        self.ui = UI()

    def new_map(self):
        # no momento, utilizando apenas um único csv para todos
        layouts = {
            'map': import_csv_layout('map.csv')
        }
        graphics = {
            'floor': import_folder('../graphics/floor'),
            'wall': import_folder('../graphics/wall')
        }
        print('antes do for')
        flag_position_player = False
        for row_index, row in enumerate(layouts['map']):
            # print('row', row)
            for col_index, col in enumerate(row):

                # print('col = ',col)

                x = col_index * TILESIZE
                y = row_index * TILESIZE

                if col not in BOUNDARY_ID and col != VOID_ID:
                    # colocando chão
                    surf = choice(graphics['floor'])
                    surf = pygame.transform.scale(surf, (TILESIZE, TILESIZE))
                    Tile((x, y), tuple([self.visible_sprites.floor_wall_group]), surf)

                    if random.randint(1, 100) == 1 and self.player is None:
                        self.player = Player((x, y),
                                             tuple([self.visible_sprites, self.attack_sprites, self.player_group]),
                                             self.obstacle_sprites)
                    elif self.player is not None and flag_position_player == False:
                        self.visible_sprites.add(self.player)
                        self.attack_sprites.add(self.player)
                        flag_position_player = True
                        self.player.set_position(x, y)
                        self.player.set_obstacle(self.obstacle_sprites)
                    elif random.randint(1, 10) == 1 and self.total_enemies_of_level < 5:
                        self.total_enemies_of_level += 1
                        Enemy(ENEMY_ID_NAME['391'], (x, y), tuple([self.visible_sprites, self.attackable_sprites]),
                              self.obstacle_sprites, self.damage_player)

                    '''elif self.player is not None and flag_position_player == False:
                        flag_position_player = True
                        self.player.set_position(x, y)'''

                elif col != VOID_ID:
                    # opcional, se tiver parede "interna" bora fazer algumas que podem ser destruídas
                    ## parede
                    surf = (graphics['wall'])[0]  ## so tem uma parede
                    ## transform poroque é 16x16 em vez de tilesize
                    surf = pygame.transform.scale(surf, (TILESIZE, TILESIZE))
                    aux = Tile((x, y), tuple([self.visible_sprites.floor_wall_group, self.obstacle_sprites]), surf)
                    self.obstacle_sprites.add(aux)
                if col == PLAYER_ID:

                    self.visible_sprites.set_cam_position(x, y)

                elif col in ENEMY_ID_NAME.keys():
                    self.total_enemies_of_level += 1
                    Enemy(ENEMY_ID_NAME[col], (x, y), tuple([self.visible_sprites, self.attackable_sprites]),
                          self.obstacle_sprites, self.damage_player)

        ## por enquanto colcoar chão em tudo

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if hasattr(target_sprite, 'sprite_type'):
                            if target_sprite.sprite_type is not None and target_sprite.sprite_type == 'enemy':
                                if self.player.attacking:
                                    target_sprite.get_damage(self.player, attack_sprite.sprite_type)
                        '''
                        if self.player.attacking:
                            if target_sprite is Enemy:
                                print('sim')
                                target_sprite.kill()'''

    def damage_player(self, amount, attack_type):
        if self.player.vunerable:
            self.player.health -= amount
            self.player.vunerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def end_of_level(self):
        if self.player is not None and self.total_enemies_of_level == self.player.exp:
            self.player.exp = 0
            return True
        else:
            return False

    def reset(self, next_level):

        self.visible_sprites.empty()
        self.visible_sprites = Camera()

        self.obstacle_sprites.empty()
        self.obstacle_sprites = pygame.sprite.Group()

        self.attack_sprites.empty()
        self.attack_sprites = pygame.sprite.Group()

        self.attackable_sprites.empty()
        self.attackable_sprites = pygame.sprite.Group()
        self.total_enemies_of_level = 0

        if not next_level:
            self.player = None
            self.player_group.empty()
            self.player_group = pygame.sprite.Group()
        else:
            self.new_map()
            pass

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update_enemies(self.player)
        self.visible_sprites.update()
        self.player_attack_logic()
        self.ui.display(self.player)
        if self.end_of_level():
            #  1 - Criar novo mapa pelo gerador de mapas, 2 - chamar new_map (manter score)
            self.reset(True)
            self.new_map()

        if self.player.health <= 0:
            # mensagem na tela
            self.reset(False)
            generate_map()
            self.new_map()


class Camera(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()

        self.floor_wall_group = pygame.sprite.Group()

        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2  # self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_height() // 2  # self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        # creating the floor
        self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # geometry
        if player is not None:
            self.offset.x = self.offset.x + round(((player.rect.centerx - self.half_width) - self.offset.x) / 30)
            self.offset.y = self.offset.y + round(((player.rect.centery - self.half_height) - self.offset.y) / 30)

        # self.offset.x = player.rect.centerx - self.half_width
        # self.offset.y = player.rect.centery - self.half_height
        # drawing floor

        ## imagem gigantesca do mapa 
        # floor_offset_pos = self.floor_rect.topleft - self.offset
        # self.display_surface.blit(self.floor_surf, floor_offset_pos)
        # i = 0
        # print(len(self.sprites()))
        # print(len(self.floor_wall_group.sprites()))
        for sprite in sorted(self.floor_wall_group, key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        '''
        pos = (player.hitbox.topleft - self.offset)    
        rec = pygame.rect.Rect(pos, (player.hitbox.width, player.hitbox.height))
        pygame.draw.rect(self.display_surface, (255, 0, 0 ), rec)
        '''

    def set_cam_position(self, x, y):
        self.floor_rect.x = x
        self.floor_rect.y = y

    def update_enemies(self, player):
        enemy: Enemy = filter(lambda sprite: type(sprite) == Enemy, self.sprites())
        for e in sorted(enemy, key=lambda sprite: sprite.rect.centery):
            e.update_enemy(player)

