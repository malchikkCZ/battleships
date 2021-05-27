import random
from constants import SIZE
from ships import Ship


class Player:

    def __init__(self, setup):
        self.moves = []
        self.hits = []
        self.setup = setup
        self.board = [[" " for i in range(SIZE)] for j in range(SIZE)]
        self.ships = self.ship_setup()

    def ship_setup(self):
        ships = []
        filled = []
        for size in self.setup:
            ship = Ship(size, filled)
            ships.append(ship)
            filled = list(set(filled + ship.coords + ship.around()))
        return ships

    def ship_destroyed(self, other, ship):
        length = ship.size
        for sq in ship.coords:
            if sq in other.hits:
                length -= 1
        if length <= 0:
            self.ships.remove(ship)
            around = ship.around()
            for sq in around:
                r = sq // SIZE
                c = sq % SIZE
                self.board[r][c] = "."
                other.moves.append(sq)
            return "The ship was DESTROYED.\n"
        return "\n"

    def attack(self, other, coord):
        r = coord // SIZE
        c = coord % SIZE
        self.moves.append(coord)
        for ship in other.ships:
            if coord in ship.coords:
                self.hits.append(coord)
                other.board[r][c] = "X"
                message = "HIT! " + other.ship_destroyed(self, ship)
                self.fill = False
                return message
        other.board[r][c] = "."
        return "MISS!\n"
    
    def is_victorious(self, other):
        if len(other.ships) == 0:
            return True


class Human(Player):

    def __init__(self, setup):
        super().__init__(setup)
        self.name = "PLAYER ONE"
        self.fill = False

    def show_ships(self):
        for ship in self.ships:
            for sq in ship.coords:
                r = sq // SIZE
                c = sq % SIZE
                self.board[r][c] = "\033[90m" + "O" + "\033[0m"
                
    def auto_fill(self):
        self.fill = True
        for sq in range(SIZE*SIZE):
            if sq not in self.moves:
                return [sq // SIZE, sq % SIZE]


class Computer(Player):

    def __init__(self, setup):
        super().__init__(setup)
        self.name = "COMPUTER"
    
    def get_computer_move(self):
        coord = random.randint(0, SIZE*SIZE-1)
        while coord in self.moves:
            coord = random.randint(0, SIZE*SIZE-1)
        if len(self.hits) > 0:
            for hit in self.hits:
                if hit+1 not in self.moves and hit % SIZE < SIZE-1:
                    coord = hit + 1
                elif hit + 10 not in self.moves and hit // SIZE < SIZE-1:
                    coord = hit + 10
                elif hit - 1 not in self.moves and hit % SIZE > 0:
                    coord = hit - 1
                elif hit - 10 not in self.moves and hit // SIZE > 0:
                    coord = hit - 10
        self.moves.append(coord)
        return coord
