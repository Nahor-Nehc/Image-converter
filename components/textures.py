from pygame import Rect, image

SIZE = 40

TEXTURE_DICTIONARY = {
  "black":(0, 0),
  "dark":(SIZE, 0),
  "medium":(SIZE*2, 0),
  "light":(SIZE*3, 0),
  "white":(SIZE*4, 0),
  "empty":(0, SIZE),
}

# properties: ["letter representation"]
wall_properties = [1]

TEXTURE_PROPERTIES = {
  "black":["b"],
  "dark":["d"],
  "medium":["m"],
  "light":["l"],
  "white":["w"],
  "empty":[],
}

TEXTURE_CODE_LIST = list(TEXTURE_DICTIONARY.keys())

class TextureAtlas:
  def __init__(self, path_to_textures):
    
    self.texture_atlas = image.load(path_to_textures).convert()    
  
  def get_texture(self, texture_name): #Get a part of the image
    try:
      coords = TEXTURE_DICTIONARY[texture_name]
    except KeyError:
      raise KeyError(f"'{texture_name}' does not have a texture. Available textures are: {TEXTURE_DICTIONARY.keys()}")
    
    handle_surface = self.texture_atlas.copy() #Sprite that will get process later
    clip_rect = Rect(coords[0], coords[1], SIZE, SIZE) #Part of the image
    handle_surface.set_clip(clip_rect) #Clip or you can call cropped
    image = self.texture_atlas.subsurface(handle_surface.get_clip()) #Get subsurface
    return image.copy() #Return