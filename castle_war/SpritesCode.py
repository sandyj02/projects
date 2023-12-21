import pygame
import random
import math
from Background import game_display

class Worker(pygame.sprite.Sprite):
     def __init__(self, initial_pos, colour):
          super().__init__()
          self.index = 0
          self.image=self.ready
          self.rect=self.image.get_rect()
          self.speed = 5
          self.rect.x, self.rect.y=initial_pos
          self.move_toMine=False
          self.move_toWall=False
          self.digging=False
          self.repairing=False
          self.sprite_ready=True

     def update(self):
          
          if self.move_toMine:
               if self.index >= len(self.run):
                    self.index = 0
               
               self.image = pygame.transform.flip(self.run[self.index], True, False)
               self.index += 1
               if self.colour=='red':
                    if self.rect.x<=random.randint(25,50):
                         self.digging=True
                         self.move_toMine=False
                    self.rect.x -= self.speed
                    
               if self.colour=='blue':
                    if self.rect.x>=random.randint(1092,1117):
                         self.digging=True
                         self.move_toMine=False
                    self.rect.x += self.speed                    
               

          elif self.digging:
               if self.index >= len(self.dig):
                    self.index = 0
               self.image = self.dig[self.index]
               self.index += 1        

          elif self.move_toWall:
               if self.index >= len(self.run):
                    self.index = 0
               self.image = self.run[self.index]
               self.index += 1
               if self.colour=='red':
                    if self.rect.x>=random.randint(167,177):
                         self.repairing=True
                         self.move_toWall=False
                    self.rect.x += self.speed
               if self.colour=='blue':
                    if self.rect.x<=random.randint(955,965):
                         self.repairing=True
                         self.move_toWall=False
                    self.rect.x -= self.speed

          elif self.repairing:
               if self.index >= len(self.repair):
                    self.index = 0
               self.image = self.repair[self.index]
               self.index += 1

     

class RedWorker(Worker):
     def __init__(self):
          self.run=[pygame.image.load('sprites/player1/worker/run-0.png'),
                    pygame.image.load('sprites/player1/worker/run-1.png'),
                    pygame.image.load('sprites/player1/worker/run-2.png'),
                    pygame.image.load('sprites/player1/worker/run-3.png'),
                    pygame.image.load('sprites/player1/worker/run-4.png'),
                    pygame.image.load('sprites/player1/worker/run-5.png')]
          self.ready=pygame.image.load('sprites/player1/worker/ready.png')
          self.repair=[pygame.image.load('sprites/player1/worker/repair-0.png'),
                          pygame.image.load('sprites/player1/worker/repair-1.png'),
                          pygame.image.load('sprites/player1/worker/repair-2.png'),
                          pygame.image.load('sprites/player1/worker/repair-3.png'),]
          self.dig=[pygame.image.load('sprites/player1/worker/dig-0.png'),
                           pygame.image.load('sprites/player1/worker/dig-1.png'),
                           pygame.image.load('sprites/player1/worker/dig-2.png'),
                           pygame.image.load('sprites/player1/worker/dig-3.png'),
                           pygame.image.load('sprites/player1/worker/dig-4.png'),
                           pygame.image.load('sprites/player1/worker/dig-5.png'),
                           pygame.image.load('sprites/player1/worker/dig-6.png'),
                           pygame.image.load('sprites/player1/worker/dig-7.png'),
                           pygame.image.load('sprites/player1/worker/dig-8.png')]
          
          self.initial_pos = (random.randint(92, 154),280)
          self.colour='red'
          super().__init__(self.initial_pos, self.colour)
          

     
               
class BlueWorker(Worker):
     def __init__(self):
          self.run=[pygame.image.load('sprites/player2/worker/run-0.png'),
                    pygame.image.load('sprites/player2/worker/run-1.png'),
                    pygame.image.load('sprites/player2/worker/run-2.png'),
                    pygame.image.load('sprites/player2/worker/run-3.png'),
                    pygame.image.load('sprites/player2/worker/run-4.png'),
                    pygame.image.load('sprites/player2/worker/run-5.png')]
          self.ready=pygame.image.load('sprites/player2/worker/ready.png')
          self.repair=[pygame.image.load('sprites/player2/worker/repair-0.png'),
                          pygame.image.load('sprites/player2/worker/repair-1.png'),
                          pygame.image.load('sprites/player2/worker/repair-2.png'),
                          pygame.image.load('sprites/player2/worker/repair-3.png'),]
          self.dig=[pygame.image.load('sprites/player2/worker/dig-0.png'),
                           pygame.image.load('sprites/player2/worker/dig-1.png'),
                           pygame.image.load('sprites/player2/worker/dig-2.png'),
                           pygame.image.load('sprites/player2/worker/dig-3.png'),
                           pygame.image.load('sprites/player2/worker/dig-4.png'),
                           pygame.image.load('sprites/player2/worker/dig-5.png'),
                           pygame.image.load('sprites/player2/worker/dig-6.png'),
                           pygame.image.load('sprites/player2/worker/dig-7.png'),
                           pygame.image.load('sprites/player2/worker/dig-8.png')]
          self.initial_pos= (random.randint(996, 1058), 280)
          self.colour='blue'
          super().__init__(self.initial_pos, self.colour)


class AttackUnit(pygame.sprite.Sprite):
     
     def __init__(self, initial_pos, max_health, colour):
          super().__init__()
          self.index = 0
          self.image=self.ready
          self.rect=self.image.get_rect()
          self.rect.x, self.rect.y=initial_pos
          self.unleash = False
          self.falling = False
          self.current_health = max_health
          self.max_health = max_health
          self.health_bar_length = 25
          self.health_ratio = self.max_health / self.health_bar_length
          self.colour=colour
          self.sprite_ready=True

     def update(self):
          self.health_bar()
          
          if self.unleash:
               if self.index >= len(self.run):
                    self.index = 0
               self.image = self.run[self.index]
               self.index += 1
               if self.colour=='red':
                    self.rect.x += self.speed
               if self.colour=='blue':
                    self.rect.x -= self.speed
               
          elif self.falling:
               if self.index >= len(self.fallen):
                    self.kill()
               else:
                    self.image = self.fallen[self.index]
                    self.index += 1
                    
     def get_damage(self, amount):
          if self.current_health>0:
               self.current_health-=amount
          else:
               self.current_health=0
               
     def health_bar(self):
          pygame.draw.rect(game_display, (217, 55, 55), (self.rect.x-2, self.rect.y-10, self.current_health/self.health_ratio, 4))
          pygame.draw.rect(game_display, (0,0,0), (self.rect.x-2, self.rect.y-10, self.health_bar_length, 4),1)

     
    
class RedArcher(AttackUnit):
     def __init__(self):
          
          self.run=[pygame.image.load('sprites/player1/bow/run-0.png'),
                    pygame.image.load('sprites/player1/bow/run-1.png'),
                    pygame.image.load('sprites/player1/bow/run-2.png'),
                    pygame.image.load('sprites/player1/bow/run-3.png'),
                    pygame.image.load('sprites/player1/bow/run-4.png'),
                    pygame.image.load('sprites/player1/bow/run-5.png'),
                    pygame.image.load('sprites/player1/bow/run-6.png'),
                    pygame.image.load('sprites/player1/bow/run-7.png'),
                    pygame.image.load('sprites/player1/bow/run-8.png'),
                    pygame.image.load('sprites/player1/bow/run-9.png'),
                    pygame.image.load('sprites/player1/bow/run-10.png'),
                    pygame.image.load('sprites/player1/bow/run-11.png'),]
          self.ready=pygame.image.load('sprites/player1/bow/ready.png')
          self.shoot=[pygame.image.load('sprites/player1/bow/shoot-0.png'),
                          pygame.image.load('sprites/player1/bow/shoot-1.png')]
          self.fallen=[pygame.image.load('sprites/player1/bow/fallen-0.png'),
                           pygame.image.load('sprites/player1/bow/fallen-1.png'),
                           pygame.image.load('sprites/player1/bow/fallen-2.png'),
                           pygame.image.load('sprites/player1/bow/fallen-3.png'),
                           pygame.image.load('sprites/player1/bow/fallen-4.png'),
                           pygame.image.load('sprites/player1/bow/fallen-5.png')]
          self.initial_pos=(random.randint(92, 154), 280)
          self.max_health=60
          self.shooting=False
          self.colour='red'
          self.speed = 8
          super().__init__(self.initial_pos, self.max_health, self.colour)
          

     def update(self):
          super().update()
          if self.shooting:
               if self.index >= len(self.shoot):
                    self.index = 0
               self.image = self.shoot[self.index]
               self.index += 1
          
        
class BlueArcher(AttackUnit):
     def __init__(self):
          self.run=[pygame.image.load('sprites/player2/bow/run-0.png'),
                        pygame.image.load('sprites/player2/bow/run-1.png'),
                        pygame.image.load('sprites/player2/bow/run-2.png'),
                        pygame.image.load('sprites/player2/bow/run-3.png'),
                        pygame.image.load('sprites/player2/bow/run-4.png'),
                        pygame.image.load('sprites/player2/bow/run-5.png'),
                        pygame.image.load('sprites/player2/bow/run-6.png'),
                        pygame.image.load('sprites/player2/bow/run-7.png'),
                        pygame.image.load('sprites/player2/bow/run-8.png'),
                        pygame.image.load('sprites/player2/bow/run-9.png'),
                        pygame.image.load('sprites/player2/bow/run-10.png'),
                        pygame.image.load('sprites/player2/bow/run-11.png'),]
          self.ready=pygame.image.load('sprites/player2/bow/ready.png')
          self.shoot=[pygame.image.load('sprites/player2/bow/shoot-0.png'),
                          pygame.image.load('sprites/player2/bow/shoot-1.png')]
          self.fallen=[pygame.image.load('sprites/player2/bow/fallen-0.png'),
                           pygame.image.load('sprites/player2/bow/fallen-1.png'),
                           pygame.image.load('sprites/player2/bow/fallen-2.png'),
                           pygame.image.load('sprites/player2/bow/fallen-3.png'),
                           pygame.image.load('sprites/player2/bow/fallen-4.png'),
                           pygame.image.load('sprites/player2/bow/fallen-5.png')]
          
          self.initial_pos = (random.randint(996, 1058),280)
          self.shooting=False
          self.max_health=60
          self.colour='blue'
          self.speed = 8
          super().__init__(self.initial_pos, self.max_health, self.colour)

     def update(self):
          super().update()
          if self.shooting:
               if self.index >= len(self.shoot):
                    self.index = 0
               self.image = self.shoot[self.index]
               self.index += 1


          
class RedKnight(AttackUnit):
     def __init__(self):
          self.attack=[pygame.image.load('sprites/player1/sword/attack-0.png'),
               pygame.image.load('sprites/player1/sword/attack-1.png'),
               pygame.image.load('sprites/player1/sword/attack-2.png'),
               pygame.image.load('sprites/player1/sword/attack-3.png'),
               pygame.image.load('sprites/player1/sword/attack-4.png'),
               pygame.image.load('sprites/player1/sword/attack-5.png'),
               pygame.image.load('sprites/player1/sword/attack-6.png'),
               pygame.image.load('sprites/player1/sword/attack-7.png')]
          self.fallen=[pygame.image.load('sprites/player1/sword/fallen-0.png'),
                pygame.image.load('sprites/player1/sword/fallen-1.png'),
                pygame.image.load('sprites/player1/sword/fallen-2.png'),
                pygame.image.load('sprites/player1/sword/fallen-3.png'),
                pygame.image.load('sprites/player1/sword/fallen-4.png'),
                pygame.image.load('sprites/player1/sword/fallen-5.png')]
          self.ready=pygame.image.load('sprites/player1/sword/ready.png')
          self.run=[pygame.image.load('sprites/player1/sword/run-0.png'),
             pygame.image.load('sprites/player1/sword/run-1.png'),
             pygame.image.load('sprites/player1/sword/run-2.png'),
             pygame.image.load('sprites/player1/sword/run-3.png'),
             pygame.image.load('sprites/player1/sword/run-4.png'),
             pygame.image.load('sprites/player1/sword/run-5.png'),
             pygame.image.load('sprites/player1/sword/run-6.png'),
             pygame.image.load('sprites/player1/sword/run-7.png'),
             pygame.image.load('sprites/player1/sword/run-8.png'),
             pygame.image.load('sprites/player1/sword/run-9.png'),
             pygame.image.load('sprites/player1/sword/run-10.png'),
             pygame.image.load('sprites/player1/sword/run-11.png')]
          self.initial_pos = (random.randint(92, 154),280)
          self.attacking=False
          self.max_health=90
          self.colour='red'
          self.speed = 5
          super().__init__(self.initial_pos, self.max_health, self.colour)

     def update(self):
          super().update()
          if self.attacking:
               if self.index >= len(self.attack):
                    self.index = 0
               self.image = self.attack[self.index]
               self.index += 1

          

class BlueKnight(AttackUnit):
     def __init__(self):
          self.attack=[pygame.image.load('sprites/player2/sword/attack-0.png'),
             pygame.image.load('sprites/player2/sword/attack-1.png'),
             pygame.image.load('sprites/player2/sword/attack-2.png'),
             pygame.image.load('sprites/player2/sword/attack-3.png'),
             pygame.image.load('sprites/player2/sword/attack-4.png'),
             pygame.image.load('sprites/player2/sword/attack-5.png'),
             pygame.image.load('sprites/player2/sword/attack-6.png'),
             pygame.image.load('sprites/player2/sword/attack-7.png')]
          self.fallen=[pygame.image.load('sprites/player2/sword/fallen-0.png'),
                pygame.image.load('sprites/player2/sword/fallen-1.png'),
                pygame.image.load('sprites/player2/sword/fallen-2.png'),
                pygame.image.load('sprites/player2/sword/fallen-3.png'),
                pygame.image.load('sprites/player2/sword/fallen-4.png'),
                pygame.image.load('sprites/player2/sword/fallen-5.png')]
          self.ready=pygame.image.load('sprites/player2/sword/ready.png')
          self.run=[pygame.image.load('sprites/player2/sword/run-0.png'),
             pygame.image.load('sprites/player2/sword/run-1.png'),
             pygame.image.load('sprites/player2/sword/run-2.png'),
             pygame.image.load('sprites/player2/sword/run-3.png'),
             pygame.image.load('sprites/player2/sword/run-4.png'),
             pygame.image.load('sprites/player2/sword/run-5.png'),
             pygame.image.load('sprites/player2/sword/run-6.png'),
             pygame.image.load('sprites/player2/sword/run-7.png'),
             pygame.image.load('sprites/player2/sword/run-8.png'),
             pygame.image.load('sprites/player2/sword/run-9.png'),
             pygame.image.load('sprites/player2/sword/run-10.png'),
             pygame.image.load('sprites/player2/sword/run-11.png')]
          self.initial_pos = (random.randint(996, 1058),280)
          self.attacking=False
          self.max_health=90
          self.colour='blue'
          self.speed = 5
          super().__init__(self.initial_pos, self.max_health, self.colour)

     def update(self):
          super().update()
          if self.attacking:
               if self.index >= len(self.attack):
                    self.index = 0
               self.image = self.attack[self.index]
               self.index += 1
               

class ArcherArrows(pygame.sprite.Sprite):
     def __init__(self):
          super().__init__()
          self.index = 0
          self.image=self.horizontal[0]
          self.rect=self.image.get_rect()
          self.speed=20
          self.rect.x=self.pos_x
          self.rect.y=self.pos_y

     def update(self):
          
          if self.index >= len(self.horizontal):
               self.index = 0
          self.image = self.horizontal[self.index]
          self.index += 1
          if self.colour=='red':
               self.rect.x += self.speed
          if self.colour=='blue':
               self.rect.x -= self.speed
          

class RedArcher_Arrows(ArcherArrows):
     def __init__(self, pos_x, pos_y):
          self.horizontal=[pygame.image.load('sprites/player1/bow/arrowhor-0.png'),
                pygame.image.load('sprites/player1/bow/arrowhor-1.png')]
          self.pos_x=pos_x
          self.pos_y=pos_y
          self.colour='red'
          super().__init__()
          

class BlueArcher_Arrows(ArcherArrows):
     def __init__(self, pos_x, pos_y):
          self.horizontal=[pygame.image.load('sprites/player2/bow/arrowhor-0.png'),
                pygame.image.load('sprites/player2/bow/arrowhor-1.png'),]
          self.pos_x=pos_x
          self.pos_y=pos_y
          self.colour='blue'
          super().__init__()


class TowerArrows(pygame.sprite.Sprite):
     def __init__(self, initial_pos):
          super().__init__()
          self.index = 0
          self.image = self.diag_arrows[0]
          self.rect = self.image.get_rect()
          self.rect.x, self.rect.y=initial_pos
          self.speed = 30
          self.angle=0
          self.diagonal=False
          self.vertical=False

     def update(self):
          
          if self.diagonal:
               if self.index >= len(self.diag_arrows):
                    self.index = 0
               self.image = self.diag_arrows[self.index]
               self.index += 1
               self.x_diff = self.dest_x - self.rect.x
               self.y_diff = self.dest_y - self.rect.y
               self.angle = math.atan2(self.y_diff, self.x_diff)
               self.rect.x+=math.cos(self.angle)*self.speed
               self.rect.y+=math.sin(self.angle)*self.speed
               
          if self.vertical:
               if self.index >= len(self.vert_arrows):
                    self.index = 0
               self.image = self.vert_arrows[self.index]
               self.index += 1
               self.rect.y+=self.speed

class RedTower_Arrows(TowerArrows):
     def __init__(self,  dest_x, dest_y):
          self.diag_arrows=[
                pygame.image.load('sprites/player1/bow/arrowdiag-0.png'),
                pygame.image.load('sprites/player1/bow/arrowdiag-1.png')]
          self.vert_arrows=[pygame.image.load('sprites/player1/bow/arrowvert-0.png'),
                pygame.image.load('sprites/player1/bow/arrowvert-1.png')]
          self.initial_pos= (232,180)
          self.dest_x=dest_x
          self.dest_y=dest_y
          super().__init__(self.initial_pos)


class BlueTower_Arrows(TowerArrows):
     def __init__(self,  dest_x, dest_y):
          self.diag_arrows=[
                pygame.image.load('sprites/player2/bow/arrowdiag-0.png'),
                pygame.image.load('sprites/player2/bow/arrowdiag-1.png')]
          self.vert_arrows=[pygame.image.load('sprites/player2/bow/arrowvert-0.png'),
                pygame.image.load('sprites/player2/bow/arrowvert-1.png')]
          self.initial_pos=(900,180)
          self.dest_x=dest_x
          self.dest_y=dest_y
          super().__init__(self.initial_pos)      

def init_var_spritesCode():
     global redTower_current_health, blueTower_current_health
     redTower_current_health=max_health
     blueTower_current_health=max_health
     return redTower_current_health, blueTower_current_health

max_health=800
redTower_current_health, blueTower_current_health=max_health, max_health

  

def Red_TowerHealth():
     global redTower_current_health
     health_bar_length=100
     health_ratio = max_health / health_bar_length
     pygame.draw.rect(game_display, (217, 55, 55), (160, 120, redTower_current_health/health_ratio, 10))
     pygame.draw.rect(game_display, (0,0,0), (160, 120, health_bar_length, 10),1)

def Blue_TowerHealth():
     global blueTower_current_health, max_health
     health_bar_length=100
     health_ratio = max_health / health_bar_length
     pygame.draw.rect(game_display, (217, 55, 55), (888, 120, blueTower_current_health/health_ratio, 10))
     pygame.draw.rect(game_display, (0,0,0), (888, 120, health_bar_length, 10),1)

def Tower_getDamage(colour, amount):
     global redTower_current_health, blueTower_current_health
     if colour=='red':
          if redTower_current_health>0:
               redTower_current_health-=amount
          if redTower_current_health<0:
               redTower_current_health=0
     if colour=='blue':
          if blueTower_current_health>0:
               blueTower_current_health-=amount
          if blueTower_current_health<0:
               blueTower_current_health=0

def Tower_getHealth(colour, amount):
     global redTower_current_health, blueTower_current_health, max_health
     if colour=='red':
          if redTower_current_health<max_health:
               redTower_current_health+=amount
          if redTower_current_health>=max_health:
               redTower_current_health=max_health
               
     if colour=='blue':
          if blueTower_current_health<max_health:
               blueTower_current_health+=amount
          if blueTower_current_health>=max_health:
               blueTower_current_health=max_health


def get_red_tower_health():
    return redTower_current_health

def get_blue_tower_health():
    return blueTower_current_health


def store_data_spritesCode(data):
     global redTower_current_health, blueTower_current_health
     data["redTower_current_health"]=redTower_current_health
     data["blueTower_current_health"]=blueTower_current_health

def getData_values_spritesCode(data):
     global redTower_current_health, blueTower_current_health
     redTower_current_health=data.get("redTower_current_health")
     blueTower_current_health=data.get("blueTower_current_health")


