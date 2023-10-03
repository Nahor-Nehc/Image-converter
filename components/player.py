from pygame import Surface, sprite
from pygame import K_w, K_a, K_s, K_d, K_LEFT, K_RIGHT, K_UP, K_DOWN, Vector2
from math import sqrt

class Movable(sprite.Sprite):
  def move(self, movement:Vector2):
    self.rect.x += movement.x
    self.rect.y += movement.y

class Player(Movable):
  def __init__(self, x, y, image:Surface, speed, gravity):
    sprite.Sprite.__init__(self)
    self.x = x
    self.y = y
    self.max_speed = speed
    self.speed = speed
    self.movement = Vector2()
    self.image = image
    self.rect = image.get_rect()
    self.gravity = gravity
    self.jump_momentum = Vector2(0, 0)
  
  def normalise_movement(self, movement):
    if movement.x != 0 and movement.y != 0:
      self.speed = self.max_speed / sqrt(2)
    else:
      self.speed = self.max_speed
    return movement

  def add_speed(self, movement):
    print("added speed")
    movement.x = movement.x * self.speed
    movement.y = movement.y * self.speed
    
    return movement
  
  def check_movement(self, keys_pressed, state) -> Vector2:
    """applies the movement vector to the object, generated from key presses"""
    print("movement checked")
    pressing = keys_pressed
    movement = Vector2(0, 0)
    
    if state.get_state() == "editor mode":
      if pressing[K_UP]:
        movement.y -= 1
      if pressing[K_DOWN]:
        movement.y += 1
      if pressing[K_LEFT]:
        movement.x -= 1
      if pressing[K_RIGHT]:
        movement.x += 1
        
    
    elif state.get_state() == "game":
      if pressing[K_LEFT]:
        movement.x -= 1
      if pressing[K_RIGHT]:
        movement.x += 1
      
      
    movement = self.normalise_movement(movement)

    return movement
  
  def jump(self):
    self.jump_momentum = Vector2(0, -5)
  
  def update(self, keys_pressed, state, tile_space):
    print("updating", self.jump_momentum)
    """
    - check horizontal movement
    
    - jumping
    
      1) decrease jump_movement by self.gravity
      
      2) check for collisions in tile_space
      
      3) code logic for landing
    
    """
    # check horizontal movement
    self.movement = self.add_speed(self.check_movement(keys_pressed, state))
    
    if state.get_state() == "game":
      # check collisions
      soft_colliding_tiles = tile_space.collide_tile_rect(self.rect, False)
      hard_colliding_tiles = tile_space.check_collidable(soft_colliding_tiles)
      
      summed = sum(hard_colliding_tiles)
      if summed > 0:
        colliding = True
      elif summed == 0:
        colliding = False
      
      if not colliding:
        self.jump_momentum.y += self.gravity
        self.movement += self.jump_momentum
      
      else:
        self.jump_momentum.y = 0
      
    self.move(self.movement)
    
    
  def draw(self, window:Surface):
    window.blit(self.image, (self.rect.x, self.rect.y))