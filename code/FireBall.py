

import entity
from player import Player
import pygame
import math


class FireBall(entity.Entity):
    
    HEIGHT = 9
    WIDTH = 68
    SPEED = 5
    
    def __init__(self, pos , groups):
        
        super().__init__(groups)
        
        self.animation = []
        self.import_fireball_assets()
        
        self.image = self.animation[0]
        self.rect = self.image.get_rect(topleft = pos)
        
        pass
    
    
    def set_direction(self, player : Player):
        
        
        player_direction = pygame.math.Vector2(player.hitbox.center)  
        my_direction = pygame.math.Vector2(self.rect.center)
        
        direction = player_direction - my_direction
        if direction.magnitude() > 0 :
            direction = direction.normalize()
        
        self.direction = direction
        
        angle_radians = math.atan2(direction.y, direction.x)
        angle_degrees= math.degrees(angle_radians) - 180 ## o fogo ta virado pra direita, entao nosso zero é 180 graus
        
        
            
        N = len(self.animation)
        for i in range(N):
            self.animation[i] = pygame.transform.rotate(self.animation[i] , angle_degrees)
                
        
    
    def import_fireball_assets(self):
        path = '../graphics/fireball/Fireball_68x9.png'
        
        sheet = pygame.image.load(path).convert_alpha()
        

        
        for x in range(0 , sheet.get_width(), FireBall.WIDTH):
            for y in range(0, sheet.get_height(), FireBall.HEIGHT):
                frame = sheet.subsurface((x, y, FireBall.WIDTH, FireBall.HEIGHT))
                self.animation.append(frame)
                
    
    def move(self):
        pass
        
