
'''
Arquivo de variáveis "globais" comuns e importantes para todo o jogo.
Como o nome já informa, é um arquivo de configuração.
'''
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

# user interface
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = 'black'

HEALTH_COLOR = 'red'
ENERGY_COLOR = 'green'
UI_BORDER_COLOR_ACTIVE = 'gold'


HITBOX_OFFSET = {
    'wall' : 0
}

BOUNDARY_ID = {395, 7, 5}
PLAYER_ID = (394)
GRASS_ID = {'8', '9', '10'}
OBJECT_ID = {'13', '14', '20'}

FLOOR_ID = {-1, 2, 8}

VOID_ID = 0

PLAYER_ENERGY_RECOVERY = 0.05
PLAYER_HEALTH_RECOVERY = 0.01



MAX_ENEMIES = 2
ENEMY_ID_NAME = {391: 'spirit'}
ENEMIES_IDS = [391]
ENEMY_HEALTH = 40
ENEMY_RESISTANCE = 3
ENEMY_ATTACK_RADIUS = 60
ENEMY_ATTACK_TYPE = 'thunder'
ENEMY_NOTICE_RADIUS = 350
ENEMY_DAMAGE = 5

