import numpy as np

class Map:
  def __init__(self):
    self.size = -1
    self.map = None
    self.path = []
    self.last_Request = None

  def setup(self, size, request):
    self.map = np.zeros((size, size)).astype(int)
    self.size = size
    self.last_Request = request

  def update(self, game_state):
    self.map = np.zeros((self.size, self.size)).astype(int)
    self.set_food(game_state["board"]["food"])
    self.set_snakes(game_state["board"]["snakes"])
    self.last_Request = game_state
  
  def set_wall(self, x, y):
    self.map[x][y] = -1


  """
  [
    {"x": 5, "y": 5},
    {"x": 9, "y": 0},
    {"x": 2, "y": 6}
  ]
  """
  def set_food(self, foodList):
    for food in foodList:
      self.map[food["x"]][food["y"]] = 1 

  """
  [
    {
      "id": "snake-508e96ac-94ad-11ea-bb37",
      "name": "My Snake",
      "health": 54,
      "body": [
        {"x": 0, "y": 0},
        {"x": 1, "y": 0},
        {"x": 2, "y": 0}
      ],
      "latency": "111",
      "head": {"x": 0, "y": 0},
      "length": 3,
      "shout": "why are we shouting??",
      "customizations":{
        "color":"#FF0000",
        "head":"pixel",
        "tail":"pixel"
      }
    },
    {
      "id": "snake-b67f4906-94ae-11ea-bb37",
      "name": "Another Snake",
      "health": 16,
      "body": [
        {"x": 5, "y": 4},
        {"x": 5, "y": 3},
        {"x": 6, "y": 3},
        {"x": 6, "y": 2}
      ],
      "latency": "222",
      "head": {"x": 5, "y": 4},
      "length": 4,
      "shout": "I'm not really sure...",
      "customizations":{
        "color":"#26CF04",
        "head":"silly",
        "tail":"curled"
      }
    }
  ]
  """
  def set_snakes(self, snakes):
    other = False
    for snake in snakes:
      """
      {
        "id": "snake-508e96ac-94ad-11ea-bb37",
        "name": "My Snake",
        "health": 54,
        "body": [
          {"x": 0, "y": 0},
          {"x": 1, "y": 0},
          {"x": 2, "y": 0}
        ],
        "latency": "111",
        "head": {"x": 0, "y": 0},
        "length": 3,
        "shout": "why are we shouting??",
        "customizations":{
          "color":"#FF0000",
          "head":"pixel",
          "tail":"pixel"
        }
      }
      """
      bodys = snake["body"]
      for i in range(len(bodys)-1):
        body = bodys.pop(0)
        self.set_wall(body["x"], body["y"])
        if i == 0 and other:  
          self.no_zone(body["x"], body["y"])
        other = True
        
          
          
        
  
  def find_path(self, position:dict):
    to_visit = [(position["x"], position["y"], (position["x"], position["y"]))]
    visited_from = {}

    start = (position["x"], position["y"])
    found = None
    
    dw = [-1, +1, 0, 0]
    dh = [0, 0, +1, -1]
    print(self.map
    while to_visit:
      pos_x, pos_y, last_point = to_visit.pop(0)
      if self.map[pos_x][pos_y] == 1 and self.has_next_move(pos_x,pos_y, last_point): # stop search when food found
        found = (pos_x, pos_y)
        visited_from[pos_x, pos_y] = last_point
        break
      for i in range(4):
        if 0 <= pos_x + dw[i] < self.size and 0 <= pos_y + dh[i] < self.size:
          visited_from[(pos_x, pos_y)] = last_point # save last step to current point
          #print(self.map[pos_x+dw[i]][pos_y+dh[i]])
          if visited_from.get((pos_x+dw[i], pos_y+dh[i]), []) != [] or self.map[pos_x+dw[i]][pos_y+dh[i]] == -1:
            continue
          to_visit.append((pos_x+dw[i], pos_y+ dh[i], (pos_x, pos_y)))

    self.path = []
    if found:
      while found != start:
        self.path.append(found)
        found = visited_from[found]
    else:
      self.path = [(self.size // 2, self.size // 2)] # Path zu schweif
      for i in range(4):
        #print(dw[i], dh[i])
        if 0 <= pos_x + dw[i] < self.size and 0 <= pos_y + dh[i] < self.size and self.map[pos_x+dw[i]][pos_y+dh[i]] != -1:
          self.path = [(pos_x + dw[i], pos_y+dh[i])]
          break

    self.path = self.path.copy()[::-1]

  def next_step(self, position:dict):
    self.find_path(position)
    print(self.path)
    ziel = self.path.pop(0)
    return self.direction(position, ziel)

  # Valid moves are "up", "down", "left", or "right"
  def direction(self, position: dict, ziel):
    print(position, ziel)
    px = position["x"]
    py = position["y"]
    zx, zy = ziel
    if px == zx:
      if py > zy:
        return "down"
      else:
        return "up"
    elif py == zy:
      if px > zx:
        return "left"
      else:
        return "right"
    else:
      return self.valid_move(position)


  def no_zone(self, pos_x, pos_y):
    dw = [-1, +1, 0, 0]
    dh = [0, 0, +1, -1]
    for i in range(4):
      if 0 <= pos_x + dw[i] < self.size and 0 <= pos_y + dh[i] < self.size:
        self.map[pos_x + dw[i]][pos_y + dh[i]] = -1

  def has_next_move(self, pos_x, pos_y, last_pos):
    dw = [-1, +1, 0, 0]
    dh = [0, 0, +1, -1]
    for i in range(4):
      if 0 <= pos_x + dw[i] < self.size and 0 <= pos_y + dh[i] < self.size:
        if self.map[pos_x + dw[i]][pos_y + dh[i]] != -1 and (pos_x + dw[i], pos_y + dh[i]) != last_pos:
          return True

  def valid_move(self, position: dict):
    pos_x = position["x"]
    pos_y = position["y"]
    dw = [-1, +1, 0, 0]
    dh = [0, 0, +1, -1]
    directions = {0:"left", 1: "right", 2:"up", 3: "down"}
    for i in range(4):
      if 0 <= pos_x + dw[i] < self.size and 0 <= pos_y + dh[i] < self.size and self.map[pos_x][pos_y] != -1:
        print("valid:", 1)
        return directions[i]