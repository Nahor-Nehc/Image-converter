
class State:
  def __init__(self, initial_state):
    self.state = initial_state
    
    self.substates = {
      "start":[],
      "menu":["level select"],
      "game":["paused"],
      "editor mode":[],
    }
    
    self.substate = None
  
  def set_state(self, state):
    self.state = state
    self.substate = None
    
  def get_state(self):
    return self.state
  
  def set_substate(self, substate):
    try:
      self.substate = self.substates[self.state][substate]
    except:
      pass
    
  def get_substate(self):
    return self.substate
  
  def get_possible_substates(self):
    return self.substates[self.state]