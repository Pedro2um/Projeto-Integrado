# Eugor

## Introdução

Eugor é um jogo desenvolvido ao decorrer da disciplina Projeto Integrado ministrada pelo Doutor João Paulo Andrade Almeida. Tem por objetivo ser um **Roguelike**, ao moldes do jogo [Rogue](https://store.steampowered.com/app/1443430/Rogue/)  , incluindo mecânicas clássicas de sua inspiração, *permadeath* e *randomly generated maps* , assim como outras mecânicas mais modernas, como por exemplo gerenciamento de  stamina e vida para poder enfrentar inimigos. 
Ao eliminar todos inimigos um novo mapa (dungeon) é gerado, sua vida continua a mesma! Tente sobreviver, crie estratégias para derrotar seus inimigos!

![Image][enemy_not_angry_1] ![Image][enemy_not_angry_2] ![Image][enemy_not_angry_3] ![Image][enemy_not_angry_4] \
![Image][enemy_angry_1] ![Image][enemy_angry_2] ![Image][enemy_angry_3] ![Image][enemy_angry_4]

## Como jogar
Primeiro, baixe a *release* mais recente extraia o zip, na pasta gerada "Eugor", no seguite caminho: Eugor\Eugor\Eugor selecione e execute **Eugor.exe** \
As *arrow keys* (famosas "setinhas") controlam o personagem e a tecla de espaço ataca. Todo ataque possui um cooldown e um custo em *stamina*. Derrote inimigos do mapa para ganhar aprimoramento em velocidade do personagem e velocidade de recuperação de *stamina*. Ao derrotar todos os inimigos do mapa, um novo mapa diferente é gerado.
![Image][player_run1]![Image][player_run2]![Image][player_run3]![Image][player_run4]![Image][player_run5]![Image][player_run6]![Image][player_run7]![Image][player_run8]
## Tecnologias utilizadas
**Python3** **,** **Scipy**, **Numpy** **e** **Pygame**

![Image][pythonlogo]
![Image][scipylogo]
![Image][numpylogo]
![Image][pygamelogo]

## Bugs conhecidos
O *hitbox* do ataque é todo o corpo do personagem. Portanto ao atacar, um inimigo mesmo que esteja atacando suas costas, ainda vai receber dano.
Caso você descubra algum outro bug, envie um email para uma dos contatos.


## Contato
pedro2um1dois@gmail.com \
matheussaick@gmail.com


[player_run1]: graphics/player/new/run/run_1.png
[player_run2]: graphics/player/new/run/run_2.png
[player_run3]: graphics/player/new/run/run_3.png
[player_run4]: graphics/player/new/run/run_4.png
[player_run5]: graphics/player/new/run/run_5.png
[player_run6]: graphics/player/new/run/run_6.png
[player_run7]: graphics/player/new/run/run_7.png
[player_run8]: graphics/player/new/run/run_8.png

[enemy_angry_1]: graphics/monsters/spirit/move/0.png
[enemy_angry_2]: graphics/monsters/spirit/move/1.png
[enemy_angry_3]: graphics/monsters/spirit/move/2.png
[enemy_angry_4]: graphics/monsters/spirit/move/3.png

[enemy_not_angry_1]: graphics/monsters/spirit/idle/0.png
[enemy_not_angry_2]: graphics/monsters/spirit/idle/1.png
[enemy_not_angry_3]: graphics/monsters/spirit/idle/2.png
[enemy_not_angry_4]: graphics/monsters/spirit/idle/3.png

[pythonlogo]: PythonLogo.png
[scipylogo]: scipy.png
[numpylogo]: NumPylogo.png
[pygamelogo]: pygame_logo.png
