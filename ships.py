import random
from constants import SIZE


class Ship:

    def __init__(self, size, filled):
        self.size = size
        self.filled = filled
        self.coords = self.setup()
    
    def setup(self):
        coords = []
        while len(coords) < self.size:
            if len(coords) == 0:
                coord = random.randint(0, SIZE*SIZE-1)
            else:
                direction = random.randint(0, 3)
                if direction == 0 and coord % SIZE < 9:
                    coord = coord + 1
                elif direction == 1 and coord // SIZE < 9:
                    coord = coord + SIZE
                elif direction == 2 and coord % SIZE > 0:
                    coord = coord - 1
                elif direction == 3 and coord // SIZE > 0:
                    coord = coord - SIZE
                else:
                    coords = []
                    continue
            if coord not in coords and coord not in self.filled:
                coords.append(coord)
            else:
                coords = []
        return coords

    def around(self):
        around_ship = []
        for part in self.coords:
            # check up
            if part // 10 > 0 and part-10 not in self.coords:
                around_ship.append(part-10)
            # check down
            if part // 10 < 9 and part+10 not in self.coords:
                around_ship.append(part+10)
            # check left
            if part % 10 > 0 and part-1 not in self.coords:
                around_ship.append(part-1)
            # check right
            if part % 10 < 9 and part+1 not in self.coords:
                around_ship.append(part+1)
            # check top left
            if part // 10 > 0 and part % 10 > 0 and part-11 not in self.coords:
                around_ship.append(part-11)
            # check top right
            if part // 10 > 0 and part % 10 < 9 and part-9 not in self.coords:
                around_ship.append(part-9)
            # check bottom left
            if part // 10 < 9 and part % 10 > 0 and part+9 not in self.coords:
                around_ship.append(part+9)
            # check bottom right
            if part // 10 < 9 and part % 10 < 9 and part+11 not in self.coords:
                around_ship.append(part+11)
        around_ship = list(set(around_ship))
        return around_ship
