from pygame import Rect, image

SIZE = 40

TEXTURE_DICTIONARY = {
  "wall":(0, 0),
  "wall-top-left":(SIZE, 0),
  "wall-left":(SIZE*2, 0),
  "wall-bottom-left":(SIZE*3, 0),
  "wall-bottom":(SIZE*4, 0),
  "wall-bottom-right":(SIZE*5, 0),
  "wall-right":(SIZE*6, 0),
  "wall-top-right":(SIZE*7, 0),
  "wall-top":(SIZE*8, 0),
  "wall-middle":(SIZE*9, 0),
  "empty":(0, SIZE),
}

# properties: ["collide/no collide", ]
wall_properties = [1]

TEXTURE_PROPERTIES = {
  "wall":wall_properties,
  "wall-top-left":wall_properties,
  "wall-left":wall_properties,
  "wall-bottom-left":wall_properties,
  "wall-bottom":wall_properties,
  "wall-bottom-right":wall_properties,
  "wall-right":wall_properties,
  "wall-top-right":wall_properties,
  "wall-top":wall_properties,
  "wall-middle":wall_properties,
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