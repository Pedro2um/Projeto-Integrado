import pygame
from support import *
from settings import *
from tile import Tile
from player import Player
from enemy import Enemy
from random import choice


class Level(pygame.sprite.Sprite):
    def __init__(self):
        self.player = None
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()  # tem que fazer algo no run
        self.obstacle_sprites = pygame.sprite.Group()

        self.new_map()

    def new_map(self):
        # no momento, utilizando apenas um único csv para todos
        layouts = {
            'map': import_csv_layout('../map/map.csv')
        }
        graphics = {
            'grass': import_folder('../graphics/Grass'),
            'objects': import_folder('../graphics/objects')
        }
        for row_index, row in enumerate(layouts['map']):
            for col_index, col in enumerate(row):
                if col != FLOOR_ID:
                    x = col_index * TILESIZE
                    y = col_index * TILESIZE

                    if col == BOUNDARY_ID:
                        Tile((x, y), tuple([self.obstacle_sprites]), 'invisible')
                    elif col == PLAYER_ID:
                        self.player = Player((9, 10), tuple([self.visible_sprites]), self.obstacle_sprites)
                    elif col in ENEMY_ID_NAME.keys():
                        Enemy(ENEMY_ID_NAME[col], (x, y), tuple([self.visible_sprites]), self.obstacle_sprites)
                    elif col in GRASS_ID:
                        random_grass_image = choice(graphics['grass'])
                        Tile((x, y), tuple([self.visible_sprites, self.obstacle_sprites]), 'grass', random_grass_image)
                    elif col in OBJECT_ID:
                        surf = graphics['objects'][int(col)]
                        Tile((x, y), tuple([self.visible_sprites, self.obstacle_sprites]), 'object', surf)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2  # self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_height() // 2  # self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        # creating the floor
        self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # geometry
        self.offset.x = self.offset.x + round(((player.rect.centerx - self.half_width) - self.offset.x) / 30)
        self.offset.y = self.offset.y + round(((player.rect.centery - self.half_height) - self.offset.y) / 30)
        # self.offset.x = player.rect.centerx - self.half_width
        # self.offset.y = player.rect.centery - self.half_height
        # drawing floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)