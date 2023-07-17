# Eugor


## Introdução

Eugor é um jogo desenvolvido para **windows 10/11** ao decorrer da disciplina Projeto Integrado ministrada pelo Doutor João Paulo Andrade Almeida. Tem por objetivo ser um **Roguelike**, ao moldes do jogo [Rogue](https://store.steampowered.com/app/1443430/Rogue/)  , incluindo mecânicas clássicas de sua inspiração, *permadeath* e *randomly generated maps* , assim como outras mecânicas mais modernas, como por exemplo gerenciamento de  stamina e vida para poder enfrentar inimigos. 
Ao eliminar todos inimigos um novo mapa (**Dungeon**) é gerado, sua vida continua a mesma! Tente sobreviver, crie estratégias para derrotar seus inimigos!

![Image][enemy_not_angry_1] ![Image][enemy_not_angry_2] ![Image][enemy_not_angry_3] ![Image][enemy_not_angry_4] ![Image][enemy_not_angry_gif] \
![Image][enemy_angry_1] ![Image][enemy_angry_2] ![Image][enemy_angry_3] ![Image][enemy_angry_4]  ![Image][enemy_angry_gif]

## ![Image][player_run_small_gif] Como jogar
Primeiramente, baixe a *release* mais recente e extraia o zip no local de sua preferência. Na pasta gerada "Eugor", no seguite caminho: Eugor\Eugor selecione e execute **Eugor.exe** para inicializar o jogo. Agora é só se divertir!!\
\
![Image][comojogar]

As *arrow keys* (famosas "setinhas") controlam o personagem e a tecla de espaço ataca. Todo ataque possui um cooldown e um custo em *stamina*. Derrote inimigos do mapa para ganhar aprimoramento em velocidade do personagem e velocidade de recuperação de *stamina*. Ao derrotar todos os inimigos do mapa, um novo mapa diferente é gerado.

## Tecnologias utilizadas
* **Python3** 
* **Scipy**
* **Numpy**
* **Pygame**

<!--
![Image][pythonlogo]
![Image][scipylogo]
![Image][numpylogo]
![Image][pygamelogo]
-->

| ![Image][pythonlogo] |![Image][scipylogo] | 
|:---:|:---:|
| **Python** | **Scipy** |
| ![Image][numpylogo]| ![Image][pygamelogo] |
| **Numpy** | **Pygame** |

 

## Bugs conhecidos
* O *hitbox* do ataque é todo o corpo do personagem. Portanto ao atacar, um inimigo mesmo que esteja atacando suas costas, ainda vai receber dano.
* Caso você se depare com algum outro bug, envie um email para uma dos contatos dos desenvolvedores com o título **BUG** que iremos providenciar correções nas próximas versões 👻.

## Histórico de Lançamentos 

* **v1.0.0-beta**
    * Pré-lançamento, primeira versão estável.
* **v1.1.0**
    * Melhoria significativa no spawn dos inimigos pelo mapa.

---
## Contato

Segue abaixo os nomes e emails para contato dos contribuidores desse projeto:
* Pedro Igor Gomes de Morais: pedro2um1dois@gmail.com 
* Matheus Saick De Martin: matheussaick@gmail.com

[comojogar]: readmefile/comojogar.jpg

[player_run1]: graphics/player/new/run/run_1.png
[player_run2]: graphics/player/new/run/run_2.png
[player_run3]: graphics/player/new/run/run_3.png
[player_run4]: graphics/player/new/run/run_4.png
[player_run5]: graphics/player/new/run/run_5.png
[player_run6]: graphics/player/new/run/run_6.png
[player_run7]: graphics/player/new/run/run_7.png
[player_run8]: graphics/player/new/run/run_8.png

[player_run_gif]: readmefile/player_run.gif
[player_run_small_gif]: readmefile/player_run_small.gif

[enemy_angry_1]: graphics/monsters/spirit/move/0.png
[enemy_angry_2]: graphics/monsters/spirit/move/1.png
[enemy_angry_3]: graphics/monsters/spirit/move/2.png
[enemy_angry_4]: graphics/monsters/spirit/move/3.png

[enemy_not_angry_1]: graphics/monsters/spirit/idle/0.png
[enemy_not_angry_2]: graphics/monsters/spirit/idle/1.png
[enemy_not_angry_3]: graphics/monsters/spirit/idle/2.png
[enemy_not_angry_4]: graphics/monsters/spirit/idle/3.png

[enemy_not_angry_gif]: readmefile/fantasma_blue_idle.gif
[enemy_angry_gif]: readmefile/fantasma_red_move.gif

[pythonlogo]: readmefile/PythonLogo.png
[scipylogo]: readmefile/scipy.png
[numpylogo]: readmefile/NumPylogo.png
[pygamelogo]: readmefile/pygame_logo.png

<!--- ![Image][player_run1]![Image][player_run2]![Image][player_run3]![Image][player_run4]![Image][player_run5]![Image][player_run6]![Image][player_run7]![Image][player_run8] ![Image][player_run_gif] -->
