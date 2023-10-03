import pygame
from components.gui import draw_around_surface

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

WIDTH, HEIGHT = 960, 560

FPS = 30

# general colours
BLACK =  (  0,   0,   0)
WHITE =  (255, 255, 255)
RED =    (211,   0,   0)
GREEN =  (  0, 150,   0)
DGREEN = (  0, 100,   0)
BLUE =   (  0,   0, 211)
LBLUE =  (137, 207, 240)
GREY =   (201, 201, 201)
LGREY =  (231, 231, 231)
DGREY =  ( 50,  50,  50)
LBROWN = (185, 122,  87)
DBROWN = (159, 100,  64)

# display window that is drawn to
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Time platformer")

# fonts
FONT = lambda x: pygame.font.SysFont("consolas.ttf", x)
TITLEFONT = FONT(70)

# tile property/ies
TILE_SIZE = 40

# file locations
from os import path
PATH_TO_ATLAS_IMAGE = path.join("assets", "images", "atlas.bmp")
PATH_TO_LEVELS = path.join("assets", "levels", "levels")

# handles all updates to the window
def draw(WIN, state, tile_space, debug_mode, texture_atlas, selected_texture, show_commands, player):
  # create blank canvas
  WIN.fill(BLACK)
  
  # draws the tile_space
  tile_space.draw(WIN)
  
  player.draw(WIN)
  
  # extra tools for the dev
  if debug_mode == True:
    text = FONT(20).render(state.get_state(), 1, WHITE)
    WIN.blit(text, (0, 0))
    
  # draw which 
  if state.get_state() == "editor mode":
    
    # draws the box around the image
    border_width = 5
    padding = 10
    x = WIDTH - TILE_SIZE - border_width*2 - padding
    y = padding
    container = pygame.Rect(x, y, TILE_SIZE + border_width*2, TILE_SIZE + border_width*2)
    pygame.draw.rect(WIN, RED, container, border_width)
    
    # draws the texture selected inside the box
    if selected_texture != "delete":
      image = texture_atlas.get_texture(selected_texture)
      WIN.blit(image, (x + border_width, y + border_width))
    else:
      image = texture_atlas.get_texture("empty")
      WIN.blit(image, (x + border_width, y + border_width))
    
    # shows commands
    if show_commands == False:
      padding = 10
      text = FONT(30).render("Press SPACE to show commands", 1, WHITE)
      x = padding
      y = HEIGHT - text.get_height() - padding
      draw_around_surface(WIN, text, x, y, padding, BLACK, WHITE, 1)
      WIN.blit(text, (padding, HEIGHT - text.get_height() - padding))
    
    elif show_commands == True:
      padding = 10
      commands = "E: Eraser\nQ: Show empty cells\nS: Save current edit\nO: Open saved edit\nC: Clear edit\nG: Show gridlines"
      text = FONT(30).render(commands, 1, WHITE)
      x = padding
      y = HEIGHT - text.get_height() - padding
      draw_around_surface(WIN, text, x, y, padding, BLACK, WHITE, 1)
      WIN.blit(text, (x, y))
  
  # updates the display to show the changes
  pygame.display.flip()

def main():
  clock = pygame.time.Clock()
  
  # remove unnecessary events from event list
  pygame.event.set_blocked(None)
  pygame.event.set_allowed([pygame.QUIT, pygame.KEYUP, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
  #pygame.event.set_allowed(USEREVENTS)
  
  from components.state import State
  from components.textures import TextureAtlas
  from components.tile_space import TileSpace
  from components.player import Player
  
  # GAME VARIABLES
  state = State("start")
  
  player_image = pygame.Surface((40, 40))
  player_image.fill(GREEN)
  player = Player(0, 0, player_image, 5, 1)
  
  # generates a tiling grid for the game
  tiling = [[(x, y) for y in range(0, HEIGHT, TILE_SIZE)] for x in range(0, WIDTH, TILE_SIZE)]
  # tiling produces this:
  #  0, 0 40, 0 ...
  # 40,40 80,40 ...
  # ...
  # 
  # tiling[a][b] returns co-ordinates: (20*a, 20*b)
  
  texture_atlas = TextureAtlas(PATH_TO_ATLAS_IMAGE)
  tile_space = TileSpace(tiling, texture_atlas, TILE_SIZE)
  
  # EDITOR MODE
  selected_group = "walls"
  selected_texture = "wall"
  show_commands = False
  
  # DEBUG MODE
  debug_mode = True
  
  #initiates game loop
  run = 1
  while run:
    
    #ticks the clock
    clock.tick(FPS)

    #gets mouse position
    mouse = pygame.mouse.get_pos()
    
    #for everything that the user has inputted ...
    for event in pygame.event.get():

      #if the "x" button is pressed ...
      if event.type == pygame.QUIT:
        
        #save game with shelve?
        #

        #ends game loop
        run = False

        #terminates pygame
        pygame.quit()

        #terminates system
        import sys
        sys.exit()
        
      elif event.type == pygame.KEYDOWN:
        if state.get_state() == "start":
          if event.key == pygame.K_e: # temp
            state.set_state("editor mode")
            
        elif state.get_state() == "editor mode":
          # hot_keys for selections
          if selected_group == "walls":
            if event.key == pygame.K_1:
              selected_texture = "wall"
            elif event.key == pygame.K_2:
              selected_texture = "wall-middle"
            elif event.key == pygame.K_3:
              selected_texture = "wall-left"
            elif event.key == pygame.K_4:
              selected_texture = "wall-bottom"
            elif event.key == pygame.K_5:
              selected_texture = "wall-right"
            elif event.key == pygame.K_6:
              selected_texture = "wall-top"
            elif event.key == pygame.K_7:
              selected_texture = "wall-top-left"
            elif event.key == pygame.K_8:
              selected_texture = "wall-bottom-left"
            elif event.key == pygame.K_9:
              selected_texture = "wall-bottom-right"
            elif event.key == pygame.K_0:
              selected_texture = "wall-top-right"
          
          if event.key == pygame.K_s:
            from pyautogui import prompt
            name = prompt(text='Name/number of level', title='Save current level' , default='')
            if name != None:
              tile_space.save_tiling(PATH_TO_LEVELS, name)
          
          elif event.key == pygame.K_o:
            from pyautogui import prompt
            name = prompt(text='Name/number of level', title='Open level' , default='')
            if name != None:
              tile_space.load_tiling(PATH_TO_LEVELS, name)
            
          # tools
          elif event.key == pygame.K_c:
            tile_space.empty()
            
          elif event.key == pygame.K_g:
            tile_space.toggle_gridlines()
          
          elif event.key == pygame.K_q:
            tile_space.toggle_show_empty_cells()
          
          elif event.key == pygame.K_e:
            selected_texture = "delete"
          
          elif event.key == pygame.K_SPACE:
            show_commands = not show_commands
          
          # temp
          elif event.key == pygame.K_t:
            state.set_state("game")
        
        elif state.get_state() == "game":
          if event.key == pygame.K_SPACE:
            player.jump()
      
    if state.get_state() == "editor mode":
      mouse_inputs = pygame.mouse.get_pressed()
      if mouse_inputs[0]:
        tile = tile_space.collide_tile_point(mouse[0], mouse[1])
        if tile == None:
          pass
        elif selected_texture == "delete":
          tile.empty()
        else:
          tile(selected_texture)
    
    pressing = pygame.key.get_pressed()
    player.update(pressing, state, tile_space)
    
    draw(WIN, state, tile_space, debug_mode, texture_atlas, selected_texture, show_commands, player)

main()