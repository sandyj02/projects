import pygame

#var
screen_width=1150
screen_height=350
game_display=pygame.display.set_mode((screen_width, screen_height))
pygame.font.init()
rubik=pygame.font.SysFont("rubikbold", 40, bold=True)
rubik60=pygame.font.SysFont("rubikbold", 60, bold=True)

#images
blue_tower=pygame.image.load('sprites/player2/building/tower.png')
blue_mine=pygame.image.load('sprites/player2/building/mine.png')
blue_barrack=pygame.image.load('sprites/player2/building/barracks.png')
blue_barrack=pygame.image.load('sprites/player2/building/barracks.png')
blue_wall=pygame.image.load('sprites/player2/building/wall.png')

red_tower=pygame.image.load('sprites/player1/building/tower.png')
red_barrack=pygame.image.load('sprites/player1/building/barracks.png')
red_mine=pygame.image.load('sprites/player1/building/mine.png')
red_wall=pygame.image.load('sprites/player1/building/wall.png')


#text var
paused_text=rubik.render("paused" , 1, (70,70,70))
castle_war=rubik60.render("castle war" , 1, (0,156,75))
RedWins=rubik.render("Red player wins!", 1, (210, 43, 43))
BlueWins=rubik.render("Blue player wins!", 1, (28, 125, 213))
draw_text=rubik.render("Draw", 1, (70,70,70))


def home_screen(play_text, load_text):
    pygame.draw.rect(game_display, (56,207,56), (0, 0, screen_width, 350))
    pygame.draw.rect(game_display, (151,230,151), (0, 0, screen_width, 300))
    pygame.draw.rect(game_display, (213,245,213), (0, 0, screen_width, 200))
    play_button = pygame.Rect(260, 230, 250, 50)
    load_button = pygame.Rect(640, 230, 250, 50)
    mouse_pos = pygame.mouse.get_pos()
    
    if play_button.collidepoint(mouse_pos):
        pygame.draw.rect(game_display,(175, 225, 175), play_button)

    else:
        pygame.draw.rect(game_display,(0,156,75), play_button)
        
    if load_button.collidepoint(mouse_pos):
        pygame.draw.rect(game_display,(175, 225, 175), load_button)
        
    else:
        pygame.draw.rect(game_display,(0,156,75), load_button)
        
    play_button_border= pygame.draw.rect(game_display, (70,70,70), play_button,3)
    load_button_border= pygame.draw.rect(game_display, (70,70,70), load_button,3)
    
    game_display.blit(play_text, (315, 240))
    game_display.blit(load_text, (690, 240))
    game_display.blit(castle_war, (390, 80))
    
    return play_button, load_button


def draw_background(red_turn, pause, save, red_players_keys, blue_players_keys):

    #background
    game_display.fill((255,255,255))
    if red_turn:
        red_rect = pygame.Rect(0, 0, screen_width//2, screen_height)
        pygame.draw.rect(game_display, (255,232,236), red_rect)

    else:
        blue_rect = pygame.Rect(screen_width//2, 0, screen_width//2, screen_height)
        pygame.draw.rect(game_display, (226, 220, 255), blue_rect)
        
    grass=pygame.Rect(0, 300, screen_width, 50)
    pygame.draw.rect(game_display, (80, 200, 120), grass)

    #red castle
    game_display.blit(red_mine, (10,263))
    game_display.blit(red_barrack, (92,250))
    game_display.blit(red_tower, (185,140))
    game_display.blit(red_wall, (180,220))
     
    #blue castle
    game_display.blit(blue_mine, (1082,263))
    game_display.blit(blue_barrack, (996,250))
    game_display.blit(blue_tower, (913,140))
    game_display.blit(blue_wall, (908,220))

    #keys
    game_display.blit(red_players_keys, (15, 308))
    game_display.blit(blue_players_keys, (15, 326))
    
    game_display.blit(pause, (440, 10))
    game_display.blit(save, (430, 32))
    

def showScores(red_init_res, blue_init_res, textfont):
     #red resources
     red_text=textfont.render("resources " + str(red_init_res), 1, (112,128,144))
     game_display.blit(red_text, (20,15))

     #blue resources
     blue_text=textfont.render("resources " + str(blue_init_res), 1, (112,128,144))
     game_display.blit(blue_text, (950,15))
     

def update():
     pygame.display.update()
     pygame.time.Clock().tick(10)

def draw_update_unit(group):
     group.draw(game_display)
     group.update()
     

def pause_game(resume):
    game_display.blit(paused_text, (475, 100))
    game_display.blit(resume, (430, 150))


def gameOver_text(winner, home_text, RedWorker_group, RedArcher_group, RedKnight_group, RedArcher_Arrows_group, RedTower_Arrows_group,
                  BlueWorker_group, BlueArcher_group, BlueKnight_group, BlueArcher_Arrows_group, BlueTower_Arrows_group):
    if winner=='red':
        game_display.blit(RedWins, (370, 100))
    if winner=='blue':
        game_display.blit(BlueWins, (370, 100))
    if not winner:
        game_display.blit(draw_text, (500, 100))
        
    button = pygame.Rect(500, 200, 130, 40)
    mouse_pos = pygame.mouse.get_pos()
    if button.collidepoint(mouse_pos):
        pygame.draw.rect(game_display,(100,100,100), button)
        
        RedWorker_group.empty()
        RedArcher_group.empty()
        RedKnight_group.empty()
        RedArcher_Arrows_group.empty()
        RedTower_Arrows_group.empty()

        BlueWorker_group.empty()
        BlueArcher_group.empty()
        BlueKnight_group.empty()
        BlueArcher_Arrows_group.empty()
        BlueTower_Arrows_group.empty()
    else:
        pygame.draw.rect(game_display,(50,50,50),button)
    game_display.blit(home_text, (535, 205))
    return button



def red_training_message(unit_turn_trained, unit_train, red_turn, training_unit_text, unit_training, y):
     if unit_turn_trained>0 and (unit_turn_trained < unit_train or (unit_turn_trained == unit_train and not red_turn)):
          game_display.blit(training_unit_text, (50,y))
          unit_training=True
     else:
          unit_training=False
     return unit_training

def blue_training_message(unit_turn_trained, unit_train, red_turn, training_unit_text, unit_training, y):
     if unit_turn_trained>0 and (unit_turn_trained < unit_train or (unit_turn_trained == unit_train and red_turn)):
          game_display.blit(training_unit_text, (998,y))
          unit_training=True
     else:
          unit_training=False
     return unit_training


    

        
