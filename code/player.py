import pygame
from entity import Entity
from support import *
from settings import *

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

        # gráficos
        self.sprite_type = 'player'
        self.animations = None
        self.import_player_assets()
        self.image: pygame.surface.Surface = pygame.image.load('../graphics/player/new/idle/idle_1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 3, self.image.get_height() * 3))

        self.status = [STATUS_RIGHT, STATUS_IDLE]

        self.rect = self.image.get_rect(topleft=pos)

        # stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'attack_cost': 10, 'magic': 4, 'speed': 10}
        # recuperar 1 de vida e 5 de energia por segundo
        self.speed = self.stats['speed']
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.attack_cost = self.stats['attack_cost']
        self.exp = 0
        self.recovery_tax = 0

        ## problema com parede, a hitbox é menor entao ele entra um pouco nela
        # self.hitbox = self.rect.inflate(0, -30)
        # hitbox_image = pygame.image.load('../graphics/player/new/hitbox/hitbox_image.png').convert_alpha()
        # hitbox_image = pygame.transform.scale(hitbox_image, (hitbox_image.get_width()*2, hitbox_image.get_height()*2))

        # self.hitbox = self.rect

        # movimentação
        self.attacking = False
        self.attack_time = None
        self.attack_cooldown = 500

        self.vunerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        self.animation_speed = 0.2
        x = self.rect.topleft[0] + 10 * 3
        y = self.rect.topleft[1] + 5 * 3
        self.hitbox = pygame.rect.Rect((x, y), (10 * 3, 27 * 3))

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = '../graphics/player/new/'
        self.animations = {'idle': [], 'run': [], 'attack': []}
        # because folders names are the same
        self.animations_speeds = {'idle': self.animation_speed, 'run': self.animation_speed,
                                  'attack': self.animation_speed}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
            size = len(self.animations[animation])
            for i in range(size):
                image = self.animations[animation][i]
                self.animations[animation][i] = pygame.transform.scale(image,
                                                                       (image.get_width() * 3, image.get_height() * 3))

            self.animations_speeds[animation] = (size / BIG_ANIMATION_SIZE) * self.animation_speed

    def animate(self):
        animation = self.animations[self.status[1]]

        # loop over the frame index
        animation_speed = self.animations_speeds[self.status[1]]
        self.frame_index += animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        old_x = self.rect.x
        old_y = self.rect.y
        self.image = animation[int(self.frame_index)]

        if self.status[0] == STATUS_LEFT:
            self.image = pygame.transform.flip(self.image, True, False)

        ## nao sei se vai evitar dar shift
        self.rect = self.image.get_rect(topleft=(old_x, old_y))
        # self.rect = self.image.get_rect(center=self.hitbox.center)  # maybe player will be shiffted, if not make this

        # reação a ataque

        if not self.vunerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    def set_obstacle(self, obstacle_sprites):
        self.obstacle_sprites = obstacle_sprites

    def set_position(self, x, y):
        dx = x - self.rect.x
        dy = y - self.rect.y
        self.rect.x += dx
        self.rect.y += dy

        self.hitbox.x += dx
        self.hitbox.y += dy

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

        if keys[pygame.K_SPACE] and not self.attacking and self.energy >= self.attack_cost:
            self.energy -= self.attack_cost
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('attack')

    def cooldown(self):
        curr_time = pygame.time.get_ticks()
        if self.attacking:
            if curr_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

        if not self.vunerable and curr_time - self.hurt_time >= self.invulnerability_duration:
            self.vunerable = True

    def check_death(self):
        if self.health <= 0:
            # fazer animação de morte
            return True

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
                self.status[1] = STATUS_IDLE

    def get_attack_damage(self):
        return self.stats['attack']

    def reset_exp(self):
        self.exp = 0

    def recovery(self):
        if self.energy <= self.stats['energy']:
            self.energy += PLAYER_ENERGY_RECOVERY + self.recovery_tax
            if self.energy > self.stats['energy']:
                self.energy = self.stats['energy']
        # caso queira recuperar vida
        # if self.health <= self.stats['health']:
        #    self.health += PLAYER_HEALTH_RECOVERY

    def update(self):
        self.check_death()
        self.recovery()
        self.input()
        self.cooldown()
        self.get_status()
        self.animate()
        self.move(self.speed)
