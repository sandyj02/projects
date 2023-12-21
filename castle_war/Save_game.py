import json
from SpritesCode import RedWorker, BlueWorker, RedKnight, BlueKnight, RedArcher, BlueArcher, RedArcher_Arrows, BlueArcher_Arrows, RedTower_Arrows, BlueTower_Arrows
import pygame
import base64

def save_data(data):
     with open("saved_game.txt", "w") as saved_file:
          json.dump(data, saved_file)

def load_data():
     try:
          with open ("saved_game.txt") as saved_file:
               data=json.load(saved_file)
               return data
     except FileNotFoundError:
          print("no data found")
          return None

def store_Workers_attributes(group):
     attributes_list=[]
     for sprite in group:
          image_string=pygame.image.tostring(sprite.image, 'RGBA')
          encoded_image=base64.b64encode(image_string).decode('utf-8')
          attributes={
          "rect.x":sprite.rect.x,
          "rect.y":sprite.rect.y,
          "image_width": sprite.image.get_width(),
          "image_height": sprite.image.get_height(),
          "image":encoded_image,
          "sprite_ready":sprite.sprite_ready,
          "index":sprite.index,
          "speed":sprite.speed,
          "move_toMine":sprite.move_toMine,
          "move_toWall":sprite.move_toWall,
          "digging":sprite.digging,
          "repairing":sprite.repairing,
          "colour":sprite.colour}
          attributes_list.append(attributes)
     return attributes_list

def store_Archer_attributes(group):
     attributes_list=[]
     for sprite in group:
          image_string=pygame.image.tostring(sprite.image, 'RGBA')
          encoded_image=base64.b64encode(image_string).decode('utf-8') 
          attributes={
          "rect.x":sprite.rect.x,
          "rect.y":sprite.rect.y,
          "image_width": sprite.image.get_width(),
          "image_height": sprite.image.get_height(),
          "image":encoded_image,
          "sprite_ready":sprite.sprite_ready,
          "index":sprite.index,
          "speed":sprite.speed,
          "unleash":sprite.unleash,
          "shooting":sprite.shooting,
          "falling":sprite.falling,
          "current_health":sprite.current_health,
          "colour":sprite.colour}
          attributes_list.append(attributes)
     return attributes_list

def store_Knight_attributes(group):
     attributes_list=[]
     for sprite in group:
          image_string=pygame.image.tostring(sprite.image, 'RGBA')
          encoded_image=base64.b64encode(image_string).decode('utf-8')
          attributes={
          "rect.x":sprite.rect.x,
          "rect.y":sprite.rect.y,
          "image_width": sprite.image.get_width(),
          "image_height": sprite.image.get_height(),
          "image":encoded_image,
          "sprite_ready":sprite.sprite_ready,
          "index":sprite.index,
          "speed":sprite.speed,
          "unleash":sprite.unleash,
          "attacking":sprite.attacking,
          "falling":sprite.falling,
          "current_health":sprite.current_health,
          "colour":sprite.colour}
          attributes_list.append(attributes)
     return attributes_list


def getWorker_attributes(sprite, worker):
       worker.rect.x = sprite.get("rect.x")
       worker.rect.y = sprite.get("rect.y")
       
       encoded_image = sprite.get("image")
       image_string = base64.b64decode(encoded_image)
       image_width=sprite.get("image_width")
       image_height=sprite.get("image_height")
       worker.image = pygame.image.fromstring(image_string, (image_width, image_height), 'RGBA')

       worker.sprite_ready = sprite.get("sprite_ready")
       worker.index = sprite.get("index")
       worker.speed = sprite.get("speed")
       worker.move_toMine = sprite.get("move_toMine")
       worker.move_toWall = sprite.get("move_toWall")
       worker.digging = sprite.get("digging")
       worker.repairing = sprite.get("repairing")
       worker.colour = sprite.get("colour")


def getData_RedWorker_attributes(data, RedWorker_group):
    attributes_list = data.get("RedWorker_group")
    if attributes_list:
        for sprite in attributes_list:
            red_worker = RedWorker()
            RedWorker_group.add(red_worker)
            getWorker_attributes(sprite, red_worker)


def getData_BlueWorker_attributes(data, BlueWorker_group):
    attributes_list = data.get("BlueWorker_group")
    if attributes_list:
        for sprite in attributes_list:
            blue_worker = BlueWorker()
            BlueWorker_group.add(blue_worker)
            getWorker_attributes(sprite, blue_worker)
            

def getArcher_attributes(sprite, archer):
     archer.rect.x=sprite.get("rect.x")
     archer.rect.y=sprite.get("rect.y")
     
     encoded_image = sprite.get("image")
     image_string = base64.b64decode(encoded_image)
     image_width = sprite.get("image_width")
     image_height = sprite.get("image_height")
     archer.image = pygame.image.fromstring(image_string, (image_width, image_height), 'RGBA')

     archer.sprite_ready = sprite.get("sprite_ready")
     archer.index=sprite.get("index")
     archer.speed=sprite.get("speed")
     archer.unleash=sprite.get("unleash")
     archer.shooting=sprite.get("shooting")
     archer.falling=sprite.get("falling")
     archer.current_health=sprite.get("current_health")
     archer.colour=sprite.get("colour")
     

def getData_RedArcher_attributes(data, RedArcher_group):
     attributes_list=data.get("RedArcher_group")
     if attributes_list:
          for sprite in attributes_list:
               red_archer=RedArcher()
               RedArcher_group.add(red_archer)
               getArcher_attributes(sprite, red_archer)
               

def getData_BlueArcher_attributes(data, BlueArcher_group):
    attributes_list = data.get("BlueArcher_group")
    if attributes_list:
        for sprite in attributes_list:
            blue_archer = BlueArcher()
            BlueArcher_group.add(blue_archer)
            getArcher_attributes(sprite, blue_archer)

def getKnight_attributes(sprite, knight):
     knight.rect.x = sprite.get("rect.x")
     knight.rect.y = sprite.get("rect.y")

     encoded_image = sprite.get("image")
     image_string = base64.b64decode(encoded_image)
     image_width = sprite.get("image_width")
     image_height = sprite.get("image_height")
     knight.image = pygame.image.fromstring(image_string, (image_width, image_height), 'RGBA')

     knight.sprite_ready = sprite.get("sprite_ready")
     knight.index = sprite.get("index")
     knight.speed = sprite.get("speed")
     knight.unleash = sprite.get("unleash")
     knight.attacking = sprite.get("attacking")
     knight.falling = sprite.get("falling")
     knight.current_health = sprite.get("current_health")
     knight.colour = sprite.get("colour")

def getData_RedKnight_attributes(data, RedKnight_group):
    attributes_list = data.get("RedKnight_group")
    if attributes_list:
        for sprite in attributes_list:
            red_knight = RedKnight()
            RedKnight_group.add(red_knight)
            getKnight_attributes(sprite, red_knight)
            

def getData_BlueKnight_attributes(data, BlueKnight_group):
    attributes_list = data.get("BlueKnight_group")
    if attributes_list:
        for sprite in attributes_list:
            blue_knight = BlueKnight()
            BlueKnight_group.add(blue_knight)
            getKnight_attributes(sprite, blue_knight)
            


               
