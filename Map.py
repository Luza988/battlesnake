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
      for body in snake["body"]:
        self.set_wall(body["x"], body["y"])

  def update_map(self, current_request):
    self.update_food(self.last_Request["board"]["food"], current_request["board"]["food"])
    self.update_wall(self.last_Request["board"]["snakes"], current_request["board"]["snakes"])
    self.last_Request = current_request

  def update_food(self, alt_food, new_food):
    c = alt_food + new_food
    for i in c:
      if i not in alt_food or i not in new_food:
          if i in alt_food:
            print("Apple eaten at", i["x"], i["y"])
            if self.map[i["x"]][i["y"]] == 1:
              self.map[i["x"]][i["y"]] = 0
          else:
            self.map[i["x"]][i["y"]] = 1

  def update_wall(self, alt_wall, new_wall):
    alt_c = []
    new_c = []
    for j in alt_wall:
      for jj in j["body"]:
        alt_c.append(jj)
    for j in alt_wall:
      for jj in j["body"]:
        alt_c.append(jj)

    c = alt_c + new_c
    for i in c:
      if i not in alt_c or i not in new_c:
          if i in alt_c:
            print("Snake moved away from", i["x"], i["y"])
            if self.map[i["x"]][i["y"]] == -1:
              self.map[i["x"]][i["y"]] = 0
          else:
            print("Snake moved to", i["x"], i["y"])
            self.map[i["x"]][i["y"]] = -1
  
  def find_path(self, position:dict):
    to_visit = [(position["x"], position["y"], (position["x"], position["y"]))]
    visited_from = {}

    start = (position["x"], position["y"])
    found = None
    
    dw = [-1, +1, 0, 0]
    dh = [0, 0, +1, -1]
    print(self.map)
    while to_visit:
      pos_x, pos_y, last_point = to_visit.pop()
      if self.map[pos_x][pos_y] == 1: # stop search when food found
        found = (pos_x, pos_y)
        break
      for i in range(4):
        if 0 < pos_x + dw[i] < self.size and 0 < pos_y + dh[i] < self.size:
          visited_from[(pos_x,pos_y)] = last_point # save last step to current point
          print(self.map[pos_x+dw[i]][pos_y+dh[i]])
          if visited_from.get((pos_x+dw[i], pos_y+dh[i]), []) != [] or self.map[pos_x+dw[i]][pos_y+dh[i]] == -1:
            continue
          to_visit.append((pos_x+dw[i], pos_y+ dh[i], (pos_x, pos_y)))

    self.path = []
    if found:
      while found != start:
        self.path.append(found)
        found = visited_from[found]
    else:
      for i in range(4):
        print(dw[i], dh[i])
        if 0 < pos_x + dw[i] < self.size or 0 < pos_y + dh[i] < self.size or not self.map[pos_x+dw[i]][pos_y+dh[i]] == -1:
          self.path = [(pos_x + dw[i], pos_y+dh[i])]
          break

    self.path = self.path.copy()[::-1]

  def next_step(self, position:dict):
    self.find_path(position)
    print(self.path)
    ziel = self.path.pop()
    return self.direction(position, ziel)

  # Valid moves are "up", "down", "left", or "right"
  def direction(self, position: dict, ziel):
    px = position["x"]
    py = position["y"]
    zx, zy = ziel
    if px == zx:
      if py > zy:
        return "down"
      else:
        return "up"
    else:
      if px > zx:
        return "right"
      else:
        return "left"
      