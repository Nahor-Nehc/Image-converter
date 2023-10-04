from collections.abc import MutableSequence
from components.textures import TEXTURE_PROPERTIES, TEXTURE_DICTIONARY
from pygame import rect
from itertools import groupby

def encode_list(s_list):
  list_ = [[key, str(len(list(group)))] for key, group in groupby(s_list)]
  final_list = []
  for key, number in list_:
    number_holder = int(number)
    while True:
      if number_holder <= 9:
        final_list.append("".join([key, str(number_holder)]))
        break
      else:
        final_list.append("".join([key, str(9)]))
        number_holder -= 9
  return final_list
    

class Tile:
  def __init__(self, atlas, x, y, tiling_size):
    self.tiling_size = tiling_size
    self.texture_name = None
    self.atlas = atlas
    self.x = x
    self.y = y
    self.image = self.atlas.get_texture("empty", self.tiling_size)
    self.set_texture_name("empty")
    
  def __call__(self, texture_name=None):
    self.set_texture_name(texture_name)
    
  def set_texture_name(self, texture_name=None):
    """texture_name comes from either texture_code_list or texture_dictionary"""
    if texture_name == None:
      self.empty()
      self.image = self.atlas.get_texture("empty", self.tiling_size)
    elif texture_name != "delete":
      try:
        TEXTURE_DICTIONARY[texture_name]
      except:
        raise KeyError(f"'{texture_name}' does not have a texture. Available textures are: {TEXTURE_DICTIONARY.keys()}")
      
      self.texture_name = texture_name
      self.properties = TEXTURE_PROPERTIES[texture_name]
      self.representation = self.properties[0]
      self.image = self.atlas.get_texture(self.texture_name, self.tiling_size)
    else:
      self.empty()
      self.image = self.atlas.get_texture("empty", self.tiling_size)
    
  def empty(self):
    self.texture_name = None
    self.representation = False
    self.properties = []
    self.set_texture_name("empty")
  
  def draw(self, window, show_empty_cells):
    if self.texture_name != None:
      window.blit(self.image, (self.x, self.y))
    elif show_empty_cells:
      self.image.fill((255, 0, 0))
      self.image.set_alpha(120)
      window.blit(self.image, (self.x, self.y))

class TileSpaceColumn(MutableSequence):
  def __init__(self, tiling, atlas, col, tiling_size):
    self.tiling_size = tiling_size
    self.tiling = tiling
    self.spaces = [Tile(atlas, coords[0], coords[1], self.tiling_size) for coords in self.tiling[col]]
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
  def __init__(self, atlas, tile_size, width, height):
    self.tiling_size = tile_size
    self.atlas = atlas
    
    self.generate_tiling(tile_size, width, height)
    
    self.show_empty_cells = True
    self.gridlines_shown = True

    super().__init__()
  
  def generate_tiling(self, tile_size, width, height):
    self.tiling_size = tile_size
    self.tiling = [[(x, y) for y in range(0, height, self.tiling_size)] for x in range(0, width, self.tiling_size)]
    self.generate_spaces()
    
  def generate_spaces(self):
    self.spaces = [TileSpaceColumn(self.tiling, self.atlas, col, self.tiling_size) for col in range(len(self.tiling))]
    
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

  def collide_tile_point(self, x, y, return_indexes = False) -> Tile:
    if x >= 0:
      x_index = x//self.tiling_size
    else:
      x_index = self.spaces[-1][-1].x*2
    if y >= 0:
      y_index = y//self.tiling_size
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
  
  def draw(self, window):
    for space in self.spaces:
      space.draw(window, self.show_empty_cells)
    
    if self.gridlines_shown:
      last_tile = self.tiling[-1][-1]
      
      from pygame import draw
      
      # horizontal dashed lines
      for y in range(0, last_tile[1] + self.tiling_size, self.tiling_size):
        for x in range(self.tiling_size//8, last_tile[0] + self.tiling_size, self.tiling_size//2):
          draw.line(window, (255, 0, 0, 50), (x, y), (x + self.tiling_size//4, y))
        
      #vertical dashed lines
      for x in range(0, last_tile[0] + self.tiling_size, self.tiling_size):
        for y in range(self.tiling_size//8, last_tile[1] + self.tiling_size, self.tiling_size//2):
          draw.line(window, (255, 0, 0, 50), (x, y), (x, y + self.tiling_size//4))
  

  def empty(self):
    for col in self:
      for cell in col:
        cell.empty()
  
  def create_tile_list(self):
    tile_list = []
    for column in self:
      col = [tile.representation for tile in column]
      tile_list.append(col)
    
    for i in range(len(tile_list) -1, -1, -1):
      if tile_list[i] != ["w"]*(len((tile_list[i]))):
        remove = i+1
        break
  
    tile_list = tile_list[:remove]
    # for item in tile_list:
    #   print("".join(item))
      
    flattened_list = [column[row] for row in range(len(tile_list[0])) for column in tile_list]
    # print(1, flattened_list)

    encoded_list = encode_list(flattened_list)
    # print(2, encoded_list)
    
    return encoded_list, len(tile_list)

  def tile_list_to_RLE(self):
    pass
  
  # def unpack_tile_list(self, tile_list):
  #   for column in range(len(self)):
  #     for tile in range(len(self[column])):
  #       self[column][tile](tile_list[column][tile])
  
  # def load_tiling(self, path_to_levels_folder, level_name):
  #   from shelve import open as open_shelf
  #   level_loader = open_shelf(path_to_levels_folder)
  #   tile_list = level_loader[level_name]
  #   self.unpack_tile_list(tile_list)
  #   level_loader.close()
    
  def save_tiling(self, path_to_levels_folder, level_name):   
    encoded_list, width = self.create_tile_list()
    if width < 10:
      width = "0" + str(width)
    else:
      width = str(width)
    text = width + "".join(encoded_list)
    
    with open(level_name+".txt", "w") as f:
      f.write(text)
  
  def toggle_gridlines(self):
    self.gridlines_shown = not self.gridlines_shown
  
  def toggle_show_empty_cells(self):
    self.show_empty_cells = not self.show_empty_cells