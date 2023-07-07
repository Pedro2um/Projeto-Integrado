import pygame
from settings import *
from entity import Entity
from support import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.status = 'idle'
        self.animations = None

        self.monster_name = monster_name
        self.import_graphics(monster_name)
        self.image = self.animations[self.status][self.frame_index]

        ##stats
        self.speed= 2
        
        
        self.rect = self.image.get_rect(topleft=pos)
        
        self.hitbox = self.rect.inflate(0, -10)
        
        self.obstacle_sprites = obstacle_sprites

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'../graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation) and self.status == 'attack':
            self.can_attack = False
        self.frame_index %= len(animation)
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

   
    def update_enemy(self, player):
        player_direction = pygame.math.Vector2(player.rect.center)
        enemy_direction = pygame.math.Vector2(self.rect.center)
        
        direction  = (player_direction - enemy_direction)
        if(direction.magnitude() > 0 ):
            direction = direction.normalize()
        self.direction = direction
        self.move(self.speed)