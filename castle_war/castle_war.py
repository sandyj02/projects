import pygame
import json
import base64
from Background import *
from SpritesCode import *
from Attack import *
from Save_game import *
from variables import *

#initialization
pygame.init()
pygame.font.init()

#global variables
game_over=False
show_home=True
paused=False
load_game=False

textfont=pygame.font.SysFont("miriammonoclm", 17)
textfont2=pygame.font.SysFont("miriammonoclm", 10)
textfont3=pygame.font.SysFont("miriammonoclm", 13)
textfont4=pygame.font.SysFont("miriammonoclm", 25)

AltMessage_train=textfont3.render("This unit is already training choose another one" , 1, (255,114,118))
AltMessage_cost=textfont3.render("You don't have enough resources" , 1, (255,114,118))

home_text=textfont4.render("home" , 1, (255,255,255))
play_text=textfont4.render("NEW GAME" , 1, (255,255,255))
load_text=textfont4.render("LOAD GAME" , 1, (255,255,255))

#costs
worker_cost=25
archer_cost=35
sword_cost=50

red_minus_Cost_worker=textfont.render("-" + str(worker_cost), 1, (255,114,118))
red_minus_Cost_archer=textfont.render("-" + str(archer_cost), 1, (255,114,118))
red_minus_Cost_sword=textfont.render("-" + str(sword_cost), 1, (255,114,118))
blue_minus_Cost_worker=textfont.render("-" + str(worker_cost), 1, (255,114,118))
blue_minus_Cost_archer=textfont.render("-" + str(archer_cost), 1, (255,114,118))
blue_minus_Cost_sword=textfont.render("-" + str(sword_cost), 1, (255,114,118))


training_worker_text=textfont2.render("training worker", 1, (112,128,144))
training_archer_text=textfont2.render("training archer", 1, (112,128,144))
training_sword_text=textfont2.render("training swordman", 1, (112,128,144))

#training
worker_train=1
archer_train=3
sword_train=3

#range/prod
worker_prod=3
#hp
worker_repair=0.2

pause_text=textfont.render("press space bar to pause" , 1, (190,190,190))
save_text=textfont.render("press 'v' to save the game" , 1, (190,190,190))
red_players_keys=textfont3.render("P1 KEYS: -> q=worker(-25) w=knight(-45) e=archer(-35)  unleash: a=worker to mine s=worker to wall d=swordman f=archer g=all", 1, (61, 61, 61))
blue_players_keys=textfont3.render("P2 KEYS: -> p=worker(-25) o=knight(-45) i=archer(-35)  unleash: l=worker to mine k=worker to wall j=swordman h=archer g=all", 1, (61, 61, 61))
resume_text=textfont.render("press space bar to restart" , 1, (110,110,110))

#timer val
red_turn_start_time = 0
blue_turn_start_time = 0

red_turn_start_time2 = 0
blue_turn_start_time2 = 0

#sprites
RedWorker_group = pygame.sprite.Group()
RedArcher_group = pygame.sprite.Group()
RedKnight_group = pygame.sprite.Group()
RedArcher_Arrows_group = pygame.sprite.Group()
RedTower_Arrows_group = pygame.sprite.Group()

BlueWorker_group = pygame.sprite.Group()
BlueArcher_group = pygame.sprite.Group()
BlueKnight_group = pygame.sprite.Group()
BlueArcher_Arrows_group = pygame.sprite.Group()
BlueTower_Arrows_group = pygame.sprite.Group()

home_button=None
data={}

def getData_values(data):
     global red_init_resources, blue_init_resources, red_turn, num_redWorkers_toMine, num_blueWorkers_toMine, num_redWorkers_toWall, num_blueWorkers_toWall
     global red_worker_turn_trained, red_archer_turn_trained, red_sword_turn_trained, blue_worker_turn_trained, blue_archer_turn_trained, blue_sword_turn_trained, RedArcher_group
     global RedKnight_group, RedArcher_Arrows_group, RedTower_Arrows_group, BlueWorker_group, BlueArcher_group, BlueKnight_group, BlueArcher_Arrows_group, BlueTower_Arrows_group
     red_init_resources = data.get("red_init_resources")
     blue_init_resources = data.get("blue_init_resources")
     red_turn = data.get("red_turn")
     num_redWorkers_toMine = data.get("num_redWorkers_toMine")
     num_blueWorkers_toMine = data.get("num_blueWorkers_toMine")
     num_redWorkers_toWall = data.get("num_redWorkers_toWall")
     num_blueWorkers_toWall = data.get("num_blueWorkers_toWall")
     red_worker_turn_trained = data.get("red_worker_turn_trained")
     red_archer_turn_trained = data.get("red_archer_turn_trained")
     red_sword_turn_trained = data.get("red_sword_turn_trained")
     blue_worker_turn_trained = data.get("blue_worker_turn_trained")
     blue_archer_turn_trained = data.get("blue_archer_turn_trained")
     blue_sword_turn_trained = data.get("blue_sword_turn_trained")
     getData_values_spritesCode(data)
     getData_RedWorker_attributes(data, RedWorker_group)
     getData_BlueWorker_attributes(data, BlueWorker_group)
     getData_RedArcher_attributes(data, RedArcher_group)
     getData_BlueArcher_attributes(data, BlueArcher_group)
     getData_RedKnight_attributes(data, RedKnight_group)
     getData_BlueKnight_attributes(data, BlueKnight_group)     

def train_red_units(minus_Cost_unit, unit_cost, unit_turn_trained):
     global red_train_one_at_time, red_cost_message, minus_points_displayed, red_init_resources, minus_points_start_time, red_turn
     red_train_one_at_time=False
     red_cost_message=False
     minus_points_displayed = minus_Cost_unit
     red_init_resources-=unit_cost
     minus_points_start_time = pygame.time.get_ticks()
     unit_turn_trained+=1
     red_turn=False
     return unit_turn_trained

def train_blue_units(minus_Cost_unit, unit_cost, unit_turn_trained):
     global blue_train_one_at_time, blue_cost_message, minus_points_displayed, blue_init_resources, minus_points_start_time, red_turn
     blue_train_one_at_time=False
     blue_cost_message=False
     minus_points_displayed = minus_Cost_unit
     blue_init_resources-=unit_cost
     minus_points_start_time = pygame.time.get_ticks()
     unit_turn_trained+=1
     red_turn=True
     return unit_turn_trained

run=True
while run:
     #home screen
     if show_home:
          play_button, load_button=home_screen(play_text, load_text)
          (red_init_resources, blue_init_resources, red_turn, red_num_sec, blue_num_sec, minus_points_displayed,
               display_plus_points, minus_points_start_time, red_train_one_at_time, blue_train_one_at_time, red_cost_message, blue_cost_message, num_redWorkers_toMine,
               num_blueWorkers_toMine, num_redWorkers_toWall, num_blueWorkers_toWall, red_worker_turn_trained, red_archer_turn_trained, red_sword_turn_trained, blue_worker_turn_trained,
               blue_archer_turn_trained, blue_sword_turn_trained, red_plus_resources_added, blue_plus_resources_added, red_worker_ready, red_archer_ready,
               red_knight_ready, blue_worker_ready, blue_archer_ready, blue_knight_ready, red_worker_training, red_knight_training, red_archer_training, blue_worker_training,
               blue_knight_training, blue_archer_training, game_over)=init_var()

     if not show_home:
               
          if load_game:
              data=load_data()
              getData_values(data)

          redTower_hp = get_red_tower_health()
          blueTower_hp = get_blue_tower_health()


          if redTower_hp<=0 and blueTower_hp<=0:
               game_over=True
               winner=None

          elif redTower_hp<=0:
               game_over=True
               winner='blue'

          elif blueTower_hp<=0:
               game_over=True
               winner='red'

          #game over screen
          if game_over:
               home_button=gameOver_text(winner, home_text, RedWorker_group, RedArcher_group, RedKnight_group, RedArcher_Arrows_group, RedTower_Arrows_group,
                  BlueWorker_group, BlueArcher_group, BlueKnight_group, BlueArcher_Arrows_group, BlueTower_Arrows_group)

          #paused screen
          if paused:
               pause_game(resume_text)
               if red_turn:
                    pygame.draw.rect(game_display,(255,232,236), (425,17,150,20))
                    pygame.draw.rect(game_display,(255, 255, 255),(575,17,150,20))
               else:
                    pygame.draw.rect(game_display,(226, 220, 255), (575,17,150,20))
                    pygame.draw.rect(game_display,(255, 255, 255), (425,17,150,20))

          #game logic
          if not game_over and not paused:
               load_game=False
               draw_background(red_turn, pause_text, save_text, red_players_keys, blue_players_keys)
               showScores(red_init_resources, blue_init_resources, textfont)
               Red_TowerHealth()
               Blue_TowerHealth()

               #show cost
               if minus_points_displayed:
                    current_time = pygame.time.get_ticks()                    
                    time_passed = current_time - minus_points_start_time

                    if time_passed < 1000:
                         if minus_points_displayed==red_minus_Cost_worker or minus_points_displayed==red_minus_Cost_archer or minus_points_displayed==red_minus_Cost_sword:
                              game_display.blit(minus_points_displayed, (120,35))
                         if minus_points_displayed==blue_minus_Cost_worker or minus_points_displayed==blue_minus_Cost_archer or minus_points_displayed==blue_minus_Cost_sword:
                              game_display.blit(minus_points_displayed, (1052,35))   
                    else:
                         minus_points_displayed=None
                                   
               
               #show which unit is training
               red_worker_training=red_training_message(red_worker_turn_trained, worker_train, red_turn, training_worker_text, red_worker_training, 225)
               red_archer_training=red_training_message(red_archer_turn_trained, archer_train, red_turn, training_archer_text, red_archer_training, 210)
               red_knight_training=red_training_message(red_sword_turn_trained, sword_train, red_turn, training_sword_text, red_knight_training, 195)

               blue_worker_training=blue_training_message(blue_worker_turn_trained, worker_train, red_turn, training_worker_text,blue_worker_training, 225)
               blue_archer_training=blue_training_message(blue_archer_turn_trained, archer_train, red_turn, training_archer_text, blue_archer_training, 210)
               blue_knight_training=blue_training_message(blue_sword_turn_trained, sword_train, red_turn, training_sword_text, blue_knight_training, 195)


               #the units have finished training
               red_worker_turn_trained=add_red_unit(red_worker_turn_trained, worker_train, red_turn, RedWorker_group, RedWorker())
               red_archer_turn_trained=add_red_unit(red_archer_turn_trained, archer_train, red_turn, RedArcher_group, RedArcher())
               red_sword_turn_trained=add_red_unit(red_sword_turn_trained, sword_train, red_turn, RedKnight_group, RedKnight())

               blue_worker_turn_trained=add_blue_unit(blue_worker_turn_trained, worker_train, red_turn, BlueWorker_group, BlueWorker())
               blue_archer_turn_trained=add_blue_unit(blue_archer_turn_trained, archer_train, red_turn, BlueArcher_group, BlueArcher())
               blue_sword_turn_trained=add_blue_unit(blue_sword_turn_trained, sword_train, red_turn, BlueKnight_group, BlueKnight())
                         

               #message 
               if red_train_one_at_time:
                    game_display.blit(AltMessage_train, (20,40))
                    
               if blue_train_one_at_time:
                    game_display.blit(AltMessage_train, (742,40))

               if red_cost_message:
                    game_display.blit(AltMessage_cost, (20,50))

               if blue_cost_message:
                    game_display.blit(AltMessage_cost, (858,50))


               if red_turn:

                    #var
                    blue_turn_start_time=None
                    blue_turn_start_time2=None
                    blue_plus_resources_added = False
                    if not red_turn_start_time:
                         red_turn_start_time = pygame.time.get_ticks()
                    if not red_turn_start_time2:
                         red_turn_start_time2 = pygame.time.get_ticks()
                         red_num_sec=5
                         
                    #+resources
                    red_plus_resources_added, red_init_resources=show_added_resources(num_redWorkers_toMine, 'red', red_plus_resources_added, red_turn_start_time, red_init_resources,
                                                                                      worker_prod, textfont)

                    #countdown       
                    red_archer_turn_trained, red_sword_turn_trained, red_train_one_at_time, red_cost_message, red_num_sec, red_turn_start_time2, red_turn= countdown(
                         red_turn_start_time2, red_num_sec, red_archer_turn_trained, red_sword_turn_trained, red_train_one_at_time, red_cost_message, 'red', red_turn, textfont4)

               if not red_turn:
                    #var
                    red_turn_start_time=None
                    red_turn_start_time2=None
                    red_plus_resources_added = False
                    if not blue_turn_start_time:
                         blue_turn_start_time = pygame.time.get_ticks()
                    if not blue_turn_start_time2:
                         blue_turn_start_time2 = pygame.time.get_ticks()
                         blue_num_sec=5

                    #+resources
                    blue_plus_resources_added, blue_init_resources=show_added_resources(num_blueWorkers_toMine, 'blue', blue_plus_resources_added, blue_turn_start_time, blue_init_resources,
                                                                                        worker_prod, textfont)

                    #countdown      
                    blue_archer_turn_trained, blue_sword_turn_trained, blue_train_one_at_time, blue_cost_message, blue_num_sec, blue_turn_start_time2, red_turn=countdown(
                         blue_turn_start_time2, blue_num_sec, blue_archer_turn_trained, blue_sword_turn_trained, blue_train_one_at_time, blue_cost_message, 'blue', red_turn, textfont4)
                

               #+health
               if num_redWorkers_toWall>0:
                    Tower_getHealth('red', worker_repair*num_redWorkers_toWall)

               if num_blueWorkers_toWall>0:
                    Tower_getHealth('blue', worker_repair*num_blueWorkers_toWall)

               #units that finished training
               red_worker_ready=check_unit_ready(RedWorker_group, red_worker_ready)
               red_archer_ready=check_unit_ready(RedArcher_group, red_archer_ready)
               red_knight_ready=check_unit_ready(RedKnight_group, red_knight_ready)
               blue_worker_ready=check_unit_ready(BlueWorker_group, blue_worker_ready)
               blue_archer_ready=check_unit_ready(BlueArcher_group, blue_archer_ready)
               blue_knight_ready=check_unit_ready(BlueKnight_group, blue_knight_ready)
               
               draw_update_unit(RedWorker_group)
               draw_update_unit(RedKnight_group)
               draw_update_unit(RedArcher_group)
               draw_update_unit(RedArcher_Arrows_group)
               draw_update_unit(RedTower_Arrows_group)
               
               draw_update_unit(BlueWorker_group)
               draw_update_unit(BlueKnight_group)
               draw_update_unit(BlueArcher_group)
               draw_update_unit(BlueArcher_Arrows_group)
               draw_update_unit(BlueTower_Arrows_group)
               

               #attack
               RedKnight_attackMode(RedKnight_group, BlueArcher_group, BlueKnight_group)
               RedArcher_shootMode(RedArcher_group, BlueArcher_group, BlueKnight_group, RedArcher_Arrows_group)
               RedTower_shootMode(RedTower_Arrows_group, BlueArcher_group, BlueKnight_group)
               
               BlueKnight_attackMode(BlueKnight_group, RedArcher_group, RedKnight_group)
               BlueArcher_shootMode(BlueArcher_group, RedArcher_group, RedKnight_group, BlueArcher_Arrows_group)
               BlueTower_shootMode(BlueTower_Arrows_group, RedArcher_group, RedKnight_group)
               
     
     for event in pygame.event.get():

          if event.type == pygame.QUIT:
               run = False

          mouse_pos = pygame.mouse.get_pos()

          if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
               #checking if the buttons are being clicked
               if play_button.collidepoint(mouse_pos):
                    show_home = False

               if load_button.collidepoint(mouse_pos):
                    load_game = True
                    show_home = False
                    
               if home_button:
                    if home_button.collidepoint(mouse_pos):
                         show_home=True
                         game_over=False
                         home_button=None
          
          if event.type == pygame.KEYDOWN:
               
               if event.key == pygame.K_SPACE:
                    if paused:
                         paused = False
                    else:
                         paused = True
                         
               if event.key ==  pygame.K_v:
                    #store the data in a dictionary
                    store_data(data, red_init_resources, blue_init_resources, red_turn, num_redWorkers_toMine, num_blueWorkers_toMine, num_redWorkers_toWall, num_blueWorkers_toWall,
                    red_worker_turn_trained, red_archer_turn_trained, red_sword_turn_trained, blue_worker_turn_trained, blue_archer_turn_trained, blue_sword_turn_trained, RedWorker_group,
                    RedArcher_group, RedKnight_group, RedArcher_Arrows_group, RedTower_Arrows_group, BlueWorker_group, BlueArcher_group, BlueKnight_group, BlueArcher_Arrows_group,
                    BlueTower_Arrows_group)
                    
                    save_data(data)

               if red_turn:

                    if ((event.key == pygame.K_q and not red_worker_training and red_init_resources>worker_cost) or
                        (event.key == pygame.K_w and not red_knight_training and red_init_resources>sword_cost) or
                        (event.key == pygame.K_e and not red_archer_training and red_init_resources>archer_cost) or
                        (event.key == pygame.K_a and red_worker_ready) or
                        (event.key == pygame.K_s and red_worker_ready) or
                        (event.key == pygame.K_d and red_knight_ready) or
                        (event.key == pygame.K_f and red_archer_ready) or
                        (event.key == pygame.K_g and (red_worker_ready or blue_worker_ready or red_archer_ready or blue_archer_ready or red_knight_ready or blue_knight_ready))):
                         
                         if red_archer_turn_trained>0:
                              red_archer_turn_trained+=1
                         if red_sword_turn_trained>0:
                              red_sword_turn_trained+=1

                    #TRAINING RED UNITS
                    
                    if event.key == pygame.K_q:
                         if red_init_resources<worker_cost:
                              red_cost_message=True
          
                         elif red_worker_turn_trained>0 and red_worker_turn_trained<worker_train:
                              red_train_one_at_time=True
                              
                         else:
                              red_worker_turn_trained=train_red_units(red_minus_Cost_worker, worker_cost, red_worker_turn_trained)
                          
                    if event.key == pygame.K_w:
                         if red_init_resources<sword_cost:
                              red_cost_message=True
                              
                         elif red_sword_turn_trained>0 and red_sword_turn_trained<sword_train:
                              red_train_one_at_time=True
                              
                         else:
                              red_sword_turn_trained=train_red_units(red_minus_Cost_sword, sword_cost, red_sword_turn_trained)

                    if event.key == pygame.K_e:
                         if red_init_resources<archer_cost:
                              red_cost_message=True
                              
                         elif (red_archer_turn_trained>0 and red_archer_turn_trained<archer_train):
                              red_train_one_at_time=True
                              
                         else:
                              red_archer_turn_trained=train_red_units(red_minus_Cost_archer, archer_cost, red_archer_turn_trained)

                    #DISTPACH RED UNITS

                    if event.key == pygame.K_a:  
                         for worker in RedWorker_group:
                              if worker.sprite_ready:
                                   red_cost_message=False
                                   red_train_one_at_time=False
                                   worker.move_toMine=True
                                   worker.sprite_ready=False
                                   num_redWorkers_toMine+=1
                                   red_worker_ready=False
                                   red_turn=False

                    if event.key == pygame.K_s:
                         for worker in RedWorker_group:
                              if worker.sprite_ready:
                                   red_cost_message=False
                                   red_train_one_at_time=False
                                   worker.move_toWall=True
                                   worker.sprite_ready=False
                                   num_redWorkers_toWall+=1
                                   red_worker_ready=False
                                   red_turn=False
                                   

                    if event.key == pygame.K_d:
                         for knight in RedKnight_group:
                              if knight.sprite_ready:
                                   red_cost_message=False
                                   red_train_one_at_time=False
                                   knight.unleash=True
                                   knight.sprite_ready=False
                                   red_knight_ready=False
                                   red_turn=False
               
                    if event.key == pygame.K_f:
                         for archer in RedArcher_group:
                              if archer.sprite_ready:
                                   red_cost_message=False
                                   red_train_one_at_time=False
                                   archer.unleash=True
                                   archer.sprite_ready=False
                                   red_archer_ready=False
                                   red_turn=False
                                   
                         
               
 
               else: #it's blue player's turn

                    #TRAINING BLUE UNITS
                    if ((event.key == pygame.K_p and not blue_worker_training and blue_init_resources>worker_cost) or
                        (event.key == pygame.K_o and not blue_knight_training and blue_init_resources>sword_cost) or
                        (event.key == pygame.K_i and not blue_archer_training and blue_init_resources>archer_cost) or
                        (event.key == pygame.K_l and blue_worker_ready) or
                        (event.key == pygame.K_k and blue_worker_ready) or
                        (event.key == pygame.K_j and blue_knight_ready) or
                        (event.key == pygame.K_h and blue_archer_ready) or
                        (event.key == pygame.K_g and (red_worker_ready or blue_worker_ready or red_archer_ready or blue_archer_ready or red_knight_ready or blue_knight_ready))):

                         if blue_archer_turn_trained > 0:
                              blue_archer_turn_trained+=1

                         if blue_sword_turn_trained > 0:
                              blue_sword_turn_trained+=1
                    
                    if event.key == pygame.K_p:
                         if blue_init_resources<worker_cost:
                              blue_cost_message=True
                              
                         elif blue_worker_turn_trained>0 and blue_worker_turn_trained<worker_train:
                              blue_train_one_at_time=True
                              
                         else:
                              blue_worker_turn_trained=train_blue_units(blue_minus_Cost_worker, worker_cost, blue_worker_turn_trained)

                    if event.key == pygame.K_o:
                         if blue_init_resources<sword_cost:
                              blue_cost_message=True
                              
                         elif blue_sword_turn_trained>0 and blue_sword_turn_trained<sword_train:
                              blue_train_one_at_time=True
                         else:
                              blue_sword_turn_trained=train_blue_units(blue_minus_Cost_sword, sword_cost, blue_sword_turn_trained)

                    if event.key == pygame.K_i:
                         if blue_init_resources<archer_cost:
                              blue_cost_message=True
                              
                         elif blue_archer_turn_trained>0 and blue_archer_turn_trained<archer_train:
                              blue_train_one_at_time=True
                              
                         else:
                              blue_archer_turn_trained=train_blue_units(blue_minus_Cost_archer, archer_cost, blue_archer_turn_trained)


                    #DISTPATCH BLUE UNITS
                    if event.key == pygame.K_l:  
                         for worker in BlueWorker_group:
                              if worker.sprite_ready:
                                   blue_cost_message=False
                                   blue_train_one_at_time=False
                                   worker.move_toMine=True
                                   worker.sprite_ready=False
                                   num_blueWorkers_toMine+=1
                                   blue_worker_ready=False
                                   red_turn=True

                    if event.key == pygame.K_k:
                         for worker in BlueWorker_group:
                              if worker.sprite_ready:
                                   blue_cost_message=False
                                   blue_train_one_at_time=False
                                   worker.move_toWall=True
                                   worker.sprite_ready=False
                                   num_blueWorkers_toWall+=1
                                   blue_worker_ready=False
                                   red_turn=True

                    if event.key == pygame.K_j:
                         for knight in BlueKnight_group:
                              if knight.sprite_ready:
                                   blue_cost_message=False
                                   blue_train_one_at_time=False
                                   knight.unleash=True
                                   knight.sprite_ready=False
                                   blue_knight_ready=False
                                   red_turn=True

                    if event.key == pygame.K_h:
                         for archer in BlueArcher_group:
                              if archer.sprite_ready:
                                   blue_cost_message=False
                                   blue_train_one_at_time=False
                                   archer.unleash=True
                                   archer.sprite_ready=False
                                   blue_archer_ready=False
                                   red_turn=True
                         

               if event.key == pygame.K_g:

                    for red_worker in RedWorker_group:
                         if red_worker.sprite_ready:
                              red_worker.move_toWall=True
                              red_worker.sprite_ready=False
                                   
                    for red_knight in RedKnight_group:
                         if red_knight.sprite_ready:
                              red_knight.unleash=True
                              red_knight.sprite_ready=False
                    
                    for red_archer in RedArcher_group:
                         if red_archer.sprite_ready:
                              red_archer.unleash=True
                              red_archer.sprite_ready=False

                    for blue_worker in BlueWorker_group:
                         if blue_worker.sprite_ready:
                              blue_worker.move_toWall=True
                              blue_worker.sprite_ready=False
                    
                    for blue_knight in BlueKnight_group:
                         if blue_knight.sprite_ready:
                              blue_knight.unleash=True
                              blue_knight.sprite_ready=False
                    
                    for blue_archer in BlueArcher_group:
                         if  blue_archer.sprite_ready:
                              blue_archer.unleash=True
                              blue_archer.sprite_ready=False

                    if red_worker_ready or red_archer_ready or red_knight_ready or blue_worker_ready or blue_archer_ready or blue_knight_ready:
                         if red_turn:
                              red_turn=False
                         else:
                              red_turn=True
              
     update()
     pygame.event.pump()

pygame.quit()
