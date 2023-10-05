import pygame
from components.gui import draw_around_surface

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

WIDTH, HEIGHT = 560, 560

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
pygame.display.set_caption("Image Converter")

# fonts
FONT = lambda x: pygame.font.SysFont("consolas.ttf", x)
TITLEFONT = FONT(70)

# tile property/ies
INITIAL_TILE_SIZE = 40

# file locations
from os import path
PATH_TO_ATLAS_IMAGE = path.join("assets", "images", "atlas.bmp")
PATH_TO_LEVELS = path.join("assets", "levels", "levels")

# handles all updates to the window
def draw(WIN, state, tile_space, debug_mode, texture_atlas, selected_texture, show_commands, tile_size):
  # create blank canvas
  WIN.fill(BLACK)
  
  # draws the tile_space
  tile_space.draw(WIN)
  
  # extra tools for the dev
  if debug_mode == True:
    text = FONT(20).render(state.get_state(), 1, WHITE)
    WIN.blit(text, (0, 0))
    
  # draw which 
  if state.get_state() == "editor":
    
    # draws the box around the image
    border_width = 5
    padding = 10
    x = WIDTH - INITIAL_TILE_SIZE - border_width*2 - padding
    y = padding
    container = pygame.Rect(x, y, INITIAL_TILE_SIZE + border_width*2, INITIAL_TILE_SIZE + border_width*2)
    pygame.draw.rect(WIN, RED, container, border_width)
    
    # draws the texture selected inside the box
    if selected_texture != "delete":
      image = texture_atlas.get_texture(selected_texture, INITIAL_TILE_SIZE)
      WIN.blit(image, (x + border_width, y + border_width))
    else:
      image = texture_atlas.get_texture("empty", INITIAL_TILE_SIZE)
      WIN.blit(image, (x + border_width, y + border_width))
    
    # shows commands
    if show_commands == False:
      padding = 10
      text = FONT(30).render("Press SPACE to show commands", 1, BLACK)
      x = padding
      y = HEIGHT - text.get_height() - padding
      #draw_around_surface(WIN, text, x, y, padding, BLACK, WHITE, 1)
      WIN.blit(text, (padding, HEIGHT - text.get_height() - padding))
    
    elif show_commands == True:
      padding = 10
      commands = "E: Eraser\nS: Save current image\nO: Open saved edit\nC: Clear image\nG: Show gridlines\n-: Decrease pixel size\n=: Increase pixel size"
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
  
  # GAME VARIABLES
  state = State("editor")
  
  # generates a tiling grid for the game
  
  # tiling produces this:
  #  0, 0 40, 0 ...
  # 40,40 80,40 ...
  # ...
  # 
  # tiling[a][b] returns co-ordinates: (20*a, 20*b)
  tile_size = INITIAL_TILE_SIZE
  
  texture_atlas = TextureAtlas(PATH_TO_ATLAS_IMAGE)
  tile_space = TileSpace(texture_atlas, tile_size, WIDTH, HEIGHT)
  
  # EDITOR MODE
  selected_texture = "black"
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

        #ends game loop
        run = False

        #terminates pygame
        pygame.quit()

        #terminates system
        import sys
        sys.exit()
        
      elif event.type == pygame.KEYDOWN:            
        if state.get_state() == "editor":
          # hot_keys for selections
          if event.key == pygame.K_1:
            selected_texture = "black"
          elif event.key == pygame.K_2:
            selected_texture = "dark"
          elif event.key == pygame.K_3:
            selected_texture = "medium"
          elif event.key == pygame.K_4:
            selected_texture = "light"
          elif event.key == pygame.K_5:
            selected_texture = "white"
          
          if event.key == pygame.K_s:
            from pyautogui import prompt
            name = prompt(text='Name/number of level', title='Save current level' , default='')
            if name != None:
              tile_space.save_tiling(PATH_TO_LEVELS, name)
            
          # tools
          elif event.key == pygame.K_c:
            tile_space.empty()
            
          elif event.key == pygame.K_g:
            tile_space.toggle_gridlines()
          
          # elif event.key == pygame.K_q:
          #   tile_space.toggle_show_empty_cells()
          
          elif event.key == pygame.K_e:
            selected_texture = "delete"
          
          elif event.key == pygame.K_SPACE:
            show_commands = not show_commands
          
          elif event.key == pygame.K_EQUALS:
            tile_size += 1
            tile_space.generate_tiling(tile_size, WIDTH, HEIGHT)
            
          elif event.key == pygame.K_MINUS:
            if len(tile_space.spaces[0].spaces) < 90:
              tile_size -= 1
              tile_space.generate_tiling(tile_size, WIDTH, HEIGHT)
      
    if state.get_state() == "editor":
      mouse_inputs = pygame.mouse.get_pressed()
      if mouse_inputs[0]:
        tile = tile_space.collide_tile_point(mouse[0], mouse[1])
        if tile == None:
          pass
        elif selected_texture == "delete":
          tile.empty()
        else:
          tile(selected_texture)
#     print(len(tile_space.spaces[0].spaces))
    draw(WIN, state, tile_space, debug_mode, texture_atlas, selected_texture, show_commands, tile_size)

main()