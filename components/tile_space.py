from collections.abc import MutableSequence
from components.textures import TEXTURE_PROPERTIES, TEXTURE_DICTIONARY
from pygame import rect

class Tile:
  def __init__(self, atlas, x, y):
    self.texture_name = None
    self.atlas = atlas
    self.x = x
    self.y = y
    self.image = self.atlas.get_texture("empty")
    
  def __call__(self, texture_name=None):
    self.set_texture_name(texture_name)
    
  def set_texture_name(self, texture_name=None):
    """texture_name comes from either texture_code_list or texture_dictionary"""
    if texture_name == None:
      self.empty()
      self.image = self.atlas.get_texture("empty")
    elif texture_name != "delete":
      try:
        TEXTURE_DICTIONARY[texture_name]
      except:
        raise KeyError(f"'{texture_name}' does not have a texture. Available textures are: {TEXTURE_DICTIONARY.keys()}")
      
      self.texture_name = texture_name
      self.properties = TEXTURE_PROPERTIES[texture_name]
      self.collide_mode = self.properties[0]
      self.image = self.atlas.get_texture(self.texture_name)
    else:
      self.empty()
      self.image = self.atlas.get_texture("empty")
    
  def empty(self):
    self.texture_name = None
    self.collide_mode = False
    self.properties = []
  
  def draw(self, window, show_empty_cells):
    if self.texture_name != None:
      window.blit(self.image, (self.x, self.y))
    elif show_empty_cells:
      self.image.fill((255, 0, 0))
      self.image.set_alpha(120)
      window.blit(self.image, (self.x, self.y))

class TileSpaceColumn(MutableSequence):
  def __init__(self, tiling, atlas, col):
    self.tiling = tiling
    self.spaces = [Tile(atlas, coords[0], coords[1]) for coords in self.tiling[col]]
    super().__init__()
    
  def __getitem__(self, i):
    return self.spaces[i]
  
  def __len__(self):
    return len(self.spaces)
  
  def __setitem__(self, index, value):
    self.spaces[index] = value
    
  def __delitem__(self, key):
    self.spaces.remove(key)
    
  def insert(self, index, object):
    self.spaces.insert(index, object)
    
  def draw(self, window, show_empty_cells):
    for space in self.spaces:
      space.draw(window, show_empty_cells)

class TileSpace(MutableSequence):
  def __init__(self, tiling, atlas, tile_size):
    self.tiling = tiling
    self.tiling_size = tile_size
    self.atlas = atlas
    
    self.show_empty_cells = False
    self.gridlines_shown = False
    
    self.generate_spaces()
    super().__init__()
    
  def generate_spaces(self):
    self.spaces = [TileSpaceColumn(self.tiling, self.atlas, col) for col in range(len(self.tiling))]
    
  def __getitem__(self, i):
    return self.spaces[i]
  
  def __len__(self):
    return len(self.spaces)
  
  def __setitem__(self, index, value):
    self.spaces[index] = value
    
  def __delitem__(self, key):
    self.spaces.remove(key)
    
  def insert(self, index, object):
    self.spaces.insert(index, object)
  
  def draw(self, window):
    for space in self.spaces:
      space.draw(window, self.show_empty_cells)
    
    if self.gridlines_shown:
      last_tile = self.tiling[-1][-1]
      
      from pygame import draw
      
      # horizontal dashed lines
      for y in range(0, last_tile[1] + self.tiling_size, self.tiling_size):
        for x in range(self.tiling_size//8, last_tile[0] + self.tiling_size, self.tiling_size//2):
          draw.line(window, (255, 255, 255, 50), (x, y), (x + self.tiling_size//4, y))
        
      #vertical dashed lines
      for x in range(0, last_tile[0] + self.tiling_size, self.tiling_size):
        for y in range(self.tiling_size//8, last_tile[1] + self.tiling_size, self.tiling_size//2):
          draw.line(window, (255, 255, 255), (x, y), (x, y + self.tiling_size//4))
  
  def collide_tile_point(self, x, y, return_indexes = False) -> Tile:
    if x >= 0:
      x_index = x//40
    else:
      x_index = self.spaces[-1][-1].x*2
    if y >= 0:
      y_index = y//40
    else:
      y_index = self.spaces[-1][-1].y*2
    try:
      if return_indexes == False:
        return self[x_index][y_index]
      else:
        return x_index, y_index
    except IndexError:
      return None
    
  def check_collidable(self, list_of_tiles):
    if list_of_tiles != None:
      tiles = [tile.collide_mode for tile in list_of_tiles]
      return tiles
    else:
      print("out of bounds")
  
  def collide_tile_rect(self, rect:rect.Rect, return_indexes = False):
    # get minimum tiles to be check
    
    # get corners (TL and BR) of rect
    x1, y1 = self.collide_tile_point(rect.left, rect.top, return_indexes = True)
    x2, y2 = self.collide_tile_point(rect.right, rect.bottom, return_indexes = True)
    
    # get tiles between corners
    x_ranges = [x for x in range(x1, x2 + 1)]
    y_ranges = [y for y in range(y1, y2 + 1)]
    tile_indexes = [(x, y) for x in x_ranges for y in y_ranges]
    
    try:
      if return_indexes == False:
        return [self[x][y] for x, y in tile_indexes]
      else:
        return tile_indexes
    except IndexError:
      return None
    

  def empty(self):
    for col in self:
      for cell in col:
        cell.empty()
  
  def create_tile_list(self):
    tile_list = []
    for column in self:
      tile_list.append([tile.texture_name for tile in column])
    return tile_list
  
  def unpack_tile_list(self, tile_list):
    for column in range(len(self)):
      for tile in range(len(self[column])):
        self[column][tile](tile_list[column][tile])
  
  def load_tiling(self, path_to_levels_folder, level_name):
    from shelve import open as open_shelf
    level_loader = open_shelf(path_to_levels_folder)
    tile_list = level_loader[level_name]
    self.unpack_tile_list(tile_list)
    level_loader.close()
    
  def save_tiling(self, path_to_levels_folder, level_name):
    from shelve import open as open_shelf
    level_loader = open_shelf(path_to_levels_folder)
    try:
      _ = level_loader[level_name]
      from pyautogui import confirm
      check = confirm(text='WARNING: There is already a file saved here. Do you want to replace it?', title='WARNING: OVERWRITE ERROR', buttons=['Yes', 'No'])
      if check == "Yes":
        level_loader[level_name] = self.create_tile_list()
      elif check == "No":
        pass
        
    except KeyError:
      level_loader[level_name] = self.create_tile_list()

    level_loader.close()
  
  def toggle_gridlines(self):
    self.gridlines_shown = not self.gridlines_shown
  
  def toggle_show_empty_cells(self):
    self.show_empty_cells = not self.show_empty_cells