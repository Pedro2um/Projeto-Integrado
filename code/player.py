import pygame
from entity import  Entity
from support import *
import settings

BIG_ANIMATION_SIZE = 8

STATUS_RIGHT = 'right'
STATUS_LEFT = 'left'
STATUS_IDLE = 'idle'
STATUS_RUN = 'run'
STATUS_ATTACK = 'attack'





##hitbox informations 
RIGHT_X = 7
RIGHT_Y = 4
LEFT_X = 10
LEFT_Y = 4

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.attacking = None
        self.animations = None
        self.image: pygame.surface.Surface = pygame.image.load('../graphics/player/new/idle/idle_1.png').convert_alpha()
        
    
        self.status = [STATUS_RIGHT, STATUS_IDLE]
    
        ## multiplicar por 3
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
        
        self.test = self.image
        self.rect = self.image.get_rect(topleft=pos)
        
        self.import_player_assets()
        
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.speed = self.stats['speed']
        
        ## problema com parede, a hitbox é menor entao ele entra um pouco nela
        #self.hitbox = self.rect.inflate(0, -30)
        #hitbox_image = pygame.image.load('../graphics/player/new/hitbox/hitbox_image.png').convert_alpha()
        #hitbox_image = pygame.transform.scale(hitbox_image, (hitbox_image.get_width()*2, hitbox_image.get_height()*2))
        

        #self.hitbox = self.rect
        self.obstacle_sprites = obstacle_sprites
        
        x= self.rect.topleft[0] + 10*3
        y = self.rect.topleft[1] + 5*3
        
        self.animation_speed = 0.2
        self.hitbox = pygame.rect.Rect((x, y), (10*3, 27*3))
        

    def import_player_assets(self):
        character_path = '../graphics/player/new/'
        self.animations = {'idle': [], 'run': [], 'attack': []}
        # because folders names are the same
        self.animations_speeds = {'idle': self.animation_speed , 'run': self.animation_speed, 'attack': self.animation_speed}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
            size = len(self.animations[animation])
            for i in range(size):
                image = self.animations[animation][i]
                self.animations[animation][i] = pygame.transform.scale(image, (image.get_width()*3, image.get_height()*3))

            self.animations_speeds[animation] = (size/BIG_ANIMATION_SIZE)*self.animation_speed
        
        

    def animate(self):
        animation = self.animations[self.status[1]]

        # loop over the frame index
        animation_speed = self.animations_speeds[self.status[1]]
        self.frame_index += animation_speed

        # self.frame_index %= len(animation) #alternative

        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        old_x = self.rect.x
        old_y = self.rect.y
        #self.image = animation[int(self.frame_index)]
        self.image= animation[int(self.frame_index)]
        
        if self.status[0] == STATUS_LEFT:
            self.image = pygame.transform.flip(self.image, True, False)
        
        ## nao sei se vai evitar dar shift
        self.rect = self.image.get_rect(topleft = (old_x, old_y))
        #self.rect = self.image.get_rect(center=self.hitbox.center)  # maybe player will be shiffted, if not make this

    def input(self):
        keys = pygame.key.get_pressed()
        # movement input
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status[0] = STATUS_RIGHT
            
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status[0] = STATUS_LEFT
        else:
            self.direction.x = 0
    
    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            self.status[1] = STATUS_IDLE
        else:
            self.status[1] = STATUS_RUN
        if self.attacking:
            # making player not able to attack and walk, change later
            self.direction.x = 0
            self.direction.y = 0
            self.status[1] = STATUS_ATTACK
        else:
            if self.status[1] == STATUS_ATTACK:
                self.status[1] == STATUS_IDLE
    
    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.move(self.speed)
