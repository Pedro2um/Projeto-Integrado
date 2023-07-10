import pygame
from settings import *
from entity import Entity
from support import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player):
        super().__init__(groups)

        self.sprite_type = 'enemy'
        self.animations = None
        self.monster_name = monster_name
        self.import_graphics(monster_name)
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

        # stats
        self.can_attack = True
        self.speed = 2
        self.health = ENEMY_HEALTH
        self.resistance = ENEMY_RESISTANCE
        self.attack_damage = ENEMY_DAMAGE
        self.attack_radius = ENEMY_ATTACK_RADIUS
        self.notice_radius = ENEMY_NOTICE_RADIUS
        self.attack_type = ENEMY_ATTACK_TYPE
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player

        self.obstacle_sprites = obstacle_sprites

        # invencibilidade temporária
        self.vulnerable = True
        self.hit_time = None
        self.invicibility_duration = 300

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'../graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.status == 'attack':
                self.can_attack = False

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldown(self):
        current_time = pygame.time.get_ticks()

        if not self.can_attack:

            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invicibility_duration:
                self.vulnerable = True

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'player':
                self.health -= player.get_attack_damage()
                print(self.health)
            else:
                pass
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self, player):
        if self.health <= 0:
            self.kill()
            player.exp += 1

    def update(self):
        self.animate()
        self.cooldown()

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':

            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def update_enemy(self, player):
        '''player_direction = pygame.math.Vector2(player.rect.center)
        enemy_direction = pygame.math.Vector2(self.rect.center)

        direction = (player_direction - enemy_direction)
        if (direction.magnitude() > 0):
            direction = direction.normalize()
        self.direction = direction'''
        self.get_status(player)
        self.actions(player)
        self.hit_reaction()
        self.move(self.speed)
        self.check_death(player)
