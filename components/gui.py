from pygame import surface, event, draw

class Element(surface.Surface):
  def __init__(self, size:tuple(), x, y):
    self.x = x
    self.y = y
    super().__init__(size)
    
    self.shown = False
  
  def toggle_shown(self):
    self.shown = not self.shown

class Button(Element):
  def __init__(self, size:tuple(), x, y, user_event, image):
    super().__init__(self, size, x, y)
    
    self.image = image
    
    self.event = user_event
    self.rect = self.get_rect()
    print(self.x)
  
  def collide_point(self, x, y):
    """call when mouse button pressed"""
    if self.shown:
      if self.rect.collidepoint(x, y):
        event.post(self.event)

def draw_around_surface(window, surface, surface_x, surface_y, padding, colour, border_colour, border_width):
  rect = surface.get_rect()
  rect.topleft = (surface_x - padding, surface_y - padding)
  rect.width += padding*2
  rect.height += padding*2
  draw.rect(window, colour, rect)
  draw.rect(window, border_colour, rect, border_width)