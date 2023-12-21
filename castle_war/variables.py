from Background import game_display
#from Attack import store_data_attack
from SpritesCode import store_data_spritesCode, init_var_spritesCode
from Save_game import *


def init_var():

     red_init_resources=250
     blue_init_resources=250
     red_turn=True

     #seconds
     red_num_sec=5
     blue_num_sec=5

     #subtracted points
     minus_points_displayed = None
     display_plus_points=False

     #timer variables
     minus_points_start_time = 0

     #message
     red_train_one_at_time=False
     blue_train_one_at_time=False

     red_cost_message=False
     blue_cost_message=False

     #UNITS VARIABLES4
     num_redWorkers_toMine=0
     num_blueWorkers_toMine=0

     num_redWorkers_toWall=0
     num_blueWorkers_toWall=0

     red_worker_turn_trained=0
     red_archer_turn_trained=0
     red_sword_turn_trained=0

     blue_worker_turn_trained=0
     blue_archer_turn_trained=0
     blue_sword_turn_trained=0

     #adding additional resources

     red_plus_resources_added = False
     blue_plus_resources_added = False

     #ready units
     red_worker_ready=False
     red_archer_ready=False
     red_knight_ready=False
     blue_worker_ready=False
     blue_archer_ready=False
     blue_knight_ready=False

     #training units
     red_worker_training=False
     red_knight_training=False
     red_archer_training=False

     blue_worker_training=False
     blue_knight_training=False
     blue_archer_training=False

     #sprites
     #nit_var_attack()
     init_var_spritesCode()


     game_over=False

     return (red_init_resources, blue_init_resources, red_turn, red_num_sec, blue_num_sec, minus_points_displayed,
     display_plus_points, minus_points_start_time, red_train_one_at_time, blue_train_one_at_time, red_cost_message, blue_cost_message, num_redWorkers_toMine,
     num_blueWorkers_toMine, num_redWorkers_toWall, num_blueWorkers_toWall, red_worker_turn_trained, red_archer_turn_trained, red_sword_turn_trained, blue_worker_turn_trained,
     blue_archer_turn_trained, blue_sword_turn_trained, red_plus_resources_added,
     blue_plus_resources_added, red_worker_ready, red_archer_ready, red_knight_ready, blue_worker_ready, blue_archer_ready, blue_knight_ready, red_worker_training,
     red_knight_training, red_archer_training, blue_worker_training, blue_knight_training, blue_archer_training, game_over)


def store_data(data, red_init_resources, blue_init_resources, red_turn, num_redWorkers_toMine, num_blueWorkers_toMine, num_redWorkers_toWall, num_blueWorkers_toWall,
     red_worker_turn_trained, red_archer_turn_trained, red_sword_turn_trained, blue_worker_turn_trained, blue_archer_turn_trained, blue_sword_turn_trained, RedWorker_group,
     RedArcher_group, RedKnight_group, RedArcher_Arrows_group, RedTower_Arrows_group, BlueWorker_group, BlueArcher_group, BlueKnight_group, BlueArcher_Arrows_group, BlueTower_Arrows_group):
     data["red_init_resources"] = red_init_resources
     data["blue_init_resources"] = blue_init_resources
     data["red_turn"] = red_turn
     data["num_redWorkers_toMine"] = num_redWorkers_toMine
     data["num_blueWorkers_toMine"] = num_blueWorkers_toMine
     data["num_redWorkers_toWall"] = num_redWorkers_toWall
     data["num_blueWorkers_toWall"] = num_blueWorkers_toWall
     data["red_worker_turn_trained"] = red_worker_turn_trained
     data["red_archer_turn_trained"] = red_archer_turn_trained
     data["red_sword_turn_trained"] = red_sword_turn_trained
     data["blue_worker_turn_trained"] = blue_worker_turn_trained
     data["blue_archer_turn_trained"] = blue_archer_turn_trained
     data["blue_sword_turn_trained"] = blue_sword_turn_trained
     data["RedWorker_group"] =  store_Workers_attributes(RedWorker_group)
     data["RedArcher_group"] =  store_Archer_attributes(RedArcher_group)
     data["RedKnight_group"] =  store_Knight_attributes(RedKnight_group)
     data["BlueWorker_group"] = store_Workers_attributes(BlueWorker_group)
     data["BlueArcher_group"] = store_Archer_attributes(BlueArcher_group)
     data["BlueKnight_group"] = store_Knight_attributes(BlueKnight_group)
     store_data_spritesCode(data)

def add_red_unit(unit_turn_trained, unit_train, red_turn, group, unit_class):
     if (unit_turn_trained >= unit_train) and red_turn:
          unit_turn_trained=0
          group.add(unit_class)
     return unit_turn_trained

def add_blue_unit(unit_turn_trained, unit_train, red_turn, group, unit_class):
     if (unit_turn_trained >= unit_train) and not red_turn:
          unit_turn_trained=0
          group.add(unit_class)
     return unit_turn_trained

def check_unit_ready(group, unit_ready):
     for unit in group:
          if unit.sprite_ready:
               unit_ready=True
     return unit_ready

def show_added_resources(num_Workers_toMine, colour, plus_resources_added, turn_start_time, init_resources, worker_prod, textfont):
     if num_Workers_toMine>0:
          plus_resources=num_Workers_toMine*worker_prod
          text_plus_resources=textfont.render("+" + str(plus_resources), 1, (80, 200, 120))
          if pygame.time.get_ticks() - turn_start_time < 1500:
               if colour=='red':
                    game_display.blit(text_plus_resources, (165,15))
               if colour=='blue':
                    game_display.blit(text_plus_resources, (1095,15))
          if not plus_resources_added:
               init_resources += plus_resources
               plus_resources_added = True
     return plus_resources_added, init_resources


def countdown(turn_start_time2, num_sec, archer_turn_trained, sword_turn_trained, train_one_at_time, cost_message, colour, red_turn, textfont4):
     if pygame.time.get_ticks() - turn_start_time2 >= 1000:
          num_sec-=1
          turn_start_time2 = pygame.time.get_ticks()
          
     if num_sec>=0:
          if colour=='red':
               seconds=textfont4.render(str(num_sec) +"s", 1, (255,114,118))
               game_display.blit(seconds, (500,50))
          if colour=='blue':
               seconds=textfont4.render(str(num_sec) +"s", 1, (28, 125, 213))
               game_display.blit(seconds, (630,50))
     else:
          if colour=='red':
               red_turn=False
          if colour=='blue':
               red_turn=True
          if archer_turn_trained>0:
               archer_turn_trained+=1
          if sword_turn_trained>0:
               sword_turn_trained+=1
          train_one_at_time=False
          cost_message=False

     return  archer_turn_trained, sword_turn_trained, train_one_at_time, cost_message, num_sec, turn_start_time2, red_turn






