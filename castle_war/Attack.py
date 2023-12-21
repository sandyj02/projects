import pygame
import random
from SpritesCode import RedArcher_Arrows, BlueArcher_Arrows, RedTower_Arrows, BlueTower_Arrows, Tower_getDamage

#var
red_wall_x=235
blue_wall_x=900

knight_damage=1.7
archer_damage=0.8
tower_damage=0.6

knight_range=28
archer_range=160
tower_range=240

knight_rest=600
archer_rest=400
tower_rest=1300

dest_x=0
dest_y=0

red_knight_previous_time=0
blue_knight_previous_time=0
red_archer_previous_time=0
blue_archer_previous_time=0
red_tower_previous_time=0
blue_tower_previous_time=0

red_knight_resting=False
blue_knight_resting=False
red_archer_resting=False
blue_archer_resting=False
red_tower_resting=False
blue_tower_resting=False

red_num_arrows=0
blue_num_arrows=0

blueArrow_archer_collision=False
blueArrow_knight_collision=False
redArrow_archer_collision=False
redArrow_knight_collision=False

def compute_min_distance(aSprite, min_distance,  enemy_group, closest_enemy):
     for enemy in enemy_group:
          distance = abs(enemy.rect.x - aSprite.rect.x)
          if distance < min_distance:
               min_distance=distance
               closest_enemy=enemy
     return min_distance, closest_enemy

def get_enemy_position(wall_x, enemy, tower_min_distance, closest_enemy, dest_x, dest_y):
     tower_enemy_distance = abs(wall_x - enemy.rect.x)
     if tower_enemy_distance < tower_min_distance:
          tower_min_distance=tower_enemy_distance
          closest_enemy=enemy
          dest_x=enemy.rect.x
          dest_y=enemy.rect.y
     return tower_min_distance, dest_x, dest_y, closest_enemy

def compute_tower_min_distance(wall_x, aSprite, sprite_min_distance, closest_enemy):
     tower_distance=abs(wall_x - aSprite.rect.x)
     if tower_distance < sprite_min_distance:
          sprite_min_distance=tower_distance
          closest_enemy=None
	  
     return sprite_min_distance, tower_distance, closest_enemy

def actions(unitType, min_distance, aSprite, closest_enemy, damage, attack_range, tower_distance, TowerColour):
     attacking=False
     shooting=False
     if min_distance <= attack_range and not aSprite.sprite_ready:
          if unitType=='knight':
               aSprite.attacking=True
               attacking=True
          if unitType=='archer':
               aSprite.shooting=True
               shooting=True
          aSprite.unleash = False

          if min_distance==tower_distance:
               Tower_getDamage(TowerColour, damage)
     else:
          attacking=False
          shooting=False

     if closest_enemy and (shooting or attacking):
          closest_enemy.get_damage(damage)
          
     if  min_distance > attack_range and not aSprite.sprite_ready:
          if unitType=='knight':
               aSprite.attacking = False
          if unitType=='archer':
               aSprite.shooting = False
          aSprite.unleash = True

     if aSprite.current_health<=0:
          if unitType=='knight':
               aSprite.attacking = False
          if unitType=='archer':
               aSprite.shooting = False
          aSprite.unleash = False
          aSprite.falling=True

def enable_resting_knight(aSprite, sprite_resting, previous_time):
     if aSprite.attacking:
          if aSprite.index >= len(aSprite.attack):
               sprite_resting=True
               previous_time=pygame.time.get_ticks()
     return sprite_resting, previous_time

def enable_resting_tower(num_arrows, tower_resting, tower_previous_time):
     if num_arrows>=10:
          num_arrows=0
          tower_resting=True
          tower_previous_time=pygame.time.get_ticks()
     return num_arrows, tower_resting, tower_previous_time

def resting(group, unitType, previous_time, sprite_resting, sprite_rest_time):
     for aSprite in group:
          if unitType=='knight':
               aSprite.attacking=False
          if unitType=='archer':
               aSprite.shooting=False
     current_time = pygame.time.get_ticks()
     if current_time-previous_time >= sprite_rest_time:
          sprite_resting = False
     return sprite_resting

def towerResting(previous_time, tower_resting):
     current_time = pygame.time.get_ticks()
     if current_time - previous_time >= tower_rest:
          tower_resting = False
     return tower_resting

def ArcherArrows(arrows_group, enemy_group, archer_colour):
     for arrows in arrows_group:
          arrows_enemy_collision = pygame.sprite.spritecollide(arrows, enemy_group, False)
          if arrows_enemy_collision:
               arrows.kill()
               for enemy in arrows_enemy_collision:
                    enemy.get_damage(archer_damage)

          if archer_colour=='red':
               if arrows.rect.x >= blue_wall_x:
                    arrows.kill()
          if archer_colour=='blue':
               if arrows.rect.x <= red_wall_x:
                    arrows.kill()

def TowerArrows(arrows, archer_group, knight_group, closest_enemy, num_arrows):
     arrow_archer_collision = pygame.sprite.spritecollideany(arrows, archer_group)
     arrow_knight_collision = pygame.sprite.spritecollideany(arrows, knight_group)
               
     if arrow_archer_collision or arrow_knight_collision:
          closest_enemy.get_damage(tower_damage)
          num_arrows+=1
     return num_arrows



def RedKnight_attackMode(RedKnight_group, BlueArcher_group, BlueKnight_group):
     global red_knight_resting, red_knight_previous_time
     red_knight_tower_distance=float('inf')

     if 'red_knight_resting' not in globals():
        red_knight_resting = False
     
     if not red_knight_resting:
     
          for red_knight in RedKnight_group:
               closest_enemy=None
               red_knight_min_distance=float('inf')
               
               red_knight_min_distance, closest_enemy = compute_min_distance(red_knight, red_knight_min_distance, BlueArcher_group, closest_enemy)
               red_knight_min_distance, closest_enemy = compute_min_distance(red_knight, red_knight_min_distance, BlueKnight_group, closest_enemy)
               red_knight_min_distance, red_knight_tower_distance, closest_enemy=compute_tower_min_distance(blue_wall_x, red_knight, red_knight_min_distance, closest_enemy)

               actions('knight', red_knight_min_distance, red_knight, closest_enemy,knight_damage, knight_range, red_knight_tower_distance, 'blue')

               red_knight_resting, red_knight_previous_time=enable_resting_knight(red_knight, red_knight_resting, red_knight_previous_time)
                         
     else:#resting
          red_knight_resting=resting(RedKnight_group, 'knight', red_knight_previous_time, red_knight_resting, knight_rest)


def BlueKnight_attackMode(BlueKnight_group, RedArcher_group, RedKnight_group):
     global blue_knight_resting, blue_knight_previous_time
     blue_knight_tower_distance=float('inf')

     if 'blue_knight_resting' not in globals():
             blue_knight_resting = False

     if not blue_knight_resting:
          
          for blue_knight in BlueKnight_group:
               blue_knight_min_distance=float('inf')
               closest_enemy=None

               blue_knight_min_distance, closest_enemy = compute_min_distance(blue_knight, blue_knight_min_distance, RedArcher_group, closest_enemy)
               blue_knight_min_distance, closest_enemy = compute_min_distance(blue_knight, blue_knight_min_distance, RedKnight_group, closest_enemy)
               blue_knight_min_distance, blue_knight_tower_distance, closest_enemy=compute_tower_min_distance(red_wall_x, blue_knight, blue_knight_min_distance, closest_enemy)

               actions('knight', blue_knight_min_distance, blue_knight, closest_enemy, knight_damage, knight_range, blue_knight_tower_distance, 'red')

               blue_knight_resting, blue_knight_previous_time=enable_resting_knight(blue_knight, blue_knight_resting, blue_knight_previous_time)

     else:#resting
          blue_knight_resting=resting(BlueKnight_group, 'knight', blue_knight_previous_time, blue_knight_resting, knight_rest)

               
def RedArcher_shootMode(RedArcher_group, BlueArcher_group, BlueKnight_group, RedArrows_group):
     global red_archer_resting, red_archer_previous_time
     red_archer_archer_distance = float('inf')
     red_archer_knight_distance = float('inf')
     
     if 'red_archer_resting' not in globals():
         red_archer_resting = False

     if not red_archer_resting:
          for red_archer in RedArcher_group:
               closest_enemy=None
               red_archer_min_distance = float('inf')

               red_archer_min_distance, closest_enemy = compute_min_distance(red_archer, red_archer_min_distance, BlueKnight_group, closest_enemy)
               red_archer_min_distance, closest_enemy = compute_min_distance(red_archer, red_archer_min_distance, BlueArcher_group, closest_enemy)
               red_archer_min_distance, red_archer_tower_distance, closest_enemy=compute_tower_min_distance(blue_wall_x, red_archer, red_archer_min_distance, closest_enemy)

               actions('archer', red_archer_min_distance, red_archer, closest_enemy, archer_damage, archer_range, red_archer_tower_distance, 'blue')

               if red_archer.shooting:
                    RedArrows_group.add(RedArcher_Arrows(red_archer.rect.x + 17, red_archer.rect.y + 5))
                    if red_archer.index >= len(red_archer.shoot):
                         red_archer_resting = True
                         red_archer_previous_time = pygame.time.get_ticks()               

     else:#resting
          red_archer_resting=resting(RedArcher_group, 'archer', red_archer_previous_time, red_archer_resting, archer_rest)

     ArcherArrows(RedArrows_group, BlueArcher_group, 'red')
     ArcherArrows(RedArrows_group, BlueKnight_group, 'red')
          

def BlueArcher_shootMode(BlueArcher_group, RedArcher_group, RedKnight_group, BlueArrows_group):
     global blue_archer_resting, blue_archer_previous_time
     blue_archer_archer_distance = float('inf')
     blue_archer_knight_distance = float('inf')

     if 'blue_archer_resting' not in globals():
          blue_archer_resting = False

     if not blue_archer_resting:
          for blue_archer in BlueArcher_group:
               blue_archer_min_distance = float('inf')
               closest_enemy = None

               blue_archer_min_distance, closest_enemy = compute_min_distance(blue_archer, blue_archer_min_distance, RedKnight_group,  closest_enemy)
               blue_archer_min_distance, closest_enemy = compute_min_distance(blue_archer, blue_archer_min_distance, RedArcher_group,  closest_enemy)
               blue_archer_min_distance, blue_archer_tower_distance, closest_enemy=compute_tower_min_distance(red_wall_x, blue_archer, blue_archer_min_distance, closest_enemy)

               actions('archer', blue_archer_min_distance, blue_archer, closest_enemy, archer_damage, archer_range, blue_archer_tower_distance, 'red')

               if blue_archer.shooting:
                    BlueArrows_group.add(BlueArcher_Arrows(blue_archer.rect.x - 17, blue_archer.rect.y + 9))
                    if blue_archer.index >= len(blue_archer.shoot):
                         blue_archer_resting = True
                         blue_archer_previous_time = pygame.time.get_ticks()

     else:#resting
          blue_archer_resting=resting(BlueArcher_group, 'archer', blue_archer_previous_time, blue_archer_resting, archer_rest)

     ArcherArrows(BlueArrows_group, RedArcher_group, 'blue')
     ArcherArrows(BlueArrows_group, RedKnight_group, 'blue')
     

def RedTower_shootMode(RedArrows_group, BlueArcher_group, BlueKnight_group):
     red_tower_min_distance=float('inf')
     closest_enemy=None
     global dest_x, dest_y, red_tower_resting, red_num_arrows, red_tower_previous_time, redArrow_archer_collision ,redArrow_knight_collision

     if 'red_tower_resting' not in globals():
          red_tower_resting = False

     if not red_tower_resting:

          for blue_archer in BlueArcher_group:
               red_tower_min_distance, dest_x, dest_y, closest_enemy=get_enemy_position(red_wall_x, blue_archer, red_tower_min_distance, closest_enemy, dest_x, dest_y)
               
          for blue_knight in BlueKnight_group:
               red_tower_min_distance, dest_x, dest_y, closest_enemy=get_enemy_position(red_wall_x, blue_knight, red_tower_min_distance, closest_enemy, dest_x, dest_y)
          
          if red_tower_min_distance<=tower_range:
               RedArrows_group.add(RedTower_Arrows(dest_x, dest_y))

          red_num_arrows, red_tower_resting, red_tower_previous_time=enable_resting_tower(red_num_arrows, red_tower_resting, red_tower_previous_time)

          for arrows in RedArrows_group:
               if dest_x>=(red_wall_x+5):
                    arrows.diagonal=True
                    arrows.vertiacl=False
               else:
                    arrows.diagonal=False 
                    arrows.vertical=True
               red_num_arrows=TowerArrows(arrows, BlueArcher_group, BlueKnight_group, closest_enemy, red_num_arrows)


     else:#resting
          red_tower_resting=towerResting(red_tower_previous_time, red_tower_resting)

     for arrows in RedArrows_group:
          if redArrow_archer_collision or redArrow_knight_collision:
               arrows.kill()
          if arrows.rect.y>=280:
               arrows.kill()



def BlueTower_shootMode(BlueArrows_group, RedArcher_group, RedKnight_group):
     
     blue_tower_min_distance=float('inf')
     closest_enemy=None
     global dest_x, dest_y, blue_num_arrows, blue_tower_previous_time, blue_tower_resting, blueArrow_archer_collision ,blueArrow_knight_collision

     if 'blue_tower_resting' not in globals():
          blue_tower_resting = False

     if not blue_tower_resting:
          
          for red_archer in RedArcher_group:
               blue_tower_min_distance, dest_x, dest_y, closest_enemy=get_enemy_position(blue_wall_x, red_archer, blue_tower_min_distance, closest_enemy, dest_x, dest_y)
               
          for red_knight in RedKnight_group:
               blue_tower_min_distance, dest_x, dest_y, closest_enemy=get_enemy_position(blue_wall_x, red_knight, blue_tower_min_distance, closest_enemy, dest_x, dest_y)
          
          if blue_tower_min_distance<=tower_range:
               BlueArrows_group.add(BlueTower_Arrows(dest_x, dest_y))

          blue_num_arrows, blue_tower_resting, blue_tower_previous_time=enable_resting_tower(blue_num_arrows, blue_tower_resting, blue_tower_previous_time)

          for arrows in BlueArrows_group:
               if dest_x<=(blue_wall_x-5):
                    arrows.diagonal=True
                    arrows.vertiacl=False
               else:
                    arrows.diagonal=False 
                    arrows.vertical=True
               blue_num_arrows=TowerArrows(arrows, RedArcher_group, RedKnight_group, closest_enemy, blue_num_arrows)

     else:#resting
          blue_tower_resting=towerResting(blue_tower_previous_time, blue_tower_resting)

     for arrows in BlueArrows_group:
          if blueArrow_archer_collision or blueArrow_knight_collision:
               arrows.kill()
          if arrows.rect.y>=280:
               arrows.kill()

    
