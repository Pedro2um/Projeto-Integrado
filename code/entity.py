import pygame
import math

X_COLLISION = 1
Y_COLLISION = 2


class Entity(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)
        self.direction = pygame.math.Vector2()
        self.frame_index = 0
        self.animation_speed = 0.15
        
        ## tem que definir na classe filha
        self.hitbox: pygame.rect.Rect = None
        self.obstacle_sprites: pygame.sprite.Group = None
        self.rect: pygame.rect.Rect = None
        self.image: pygame.Surface() = None

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        
        old_x = self.hitbox.x
        old_y = self.hitbox.y
        
        self.hitbox.x += self.direction.x * speed
        self.collision(X_COLLISION)
        self.hitbox.y += self.direction.y * speed
        self.collision(Y_COLLISION)
        self.rect.x += self.hitbox.x - old_x
        self.rect.y += self.hitbox.y - old_y


    def collision(self, collision_type):
        
        if collision_type == X_COLLISION:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        elif collision_type == Y_COLLISION:
            
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
    
    def wave_value(self):
        value = math.sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

