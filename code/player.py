import pygame
from entity import  Entity
from support import *

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.attacking = None
        self.animations = None
        self.image = pygame.image.load('../graphics/test/player.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.import_player_assets()
        self.status = 'down'
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.speed = self.stats['speed']
        
        ## problema com parede, a hitbox é menor entao ele entra um pouco nela
        ##self.hitbox = self.rect.inflate(0, -30)
        self.hitbox = self.rect
        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                           'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []}
        # because folders names are the same

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed

        # self.frame_index %= len(animation) #alternative

        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)  # maybe player will be shiffted, if not make this

    def input(self):
        keys = pygame.key.get_pressed()
        # movement input
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0
    
    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            # making player not able to attack and walk, change later
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
    
    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.move(self.speed)
