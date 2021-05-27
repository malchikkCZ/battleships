import sys
import os
import random
import time

SIZE = 10
SETUP = [5, 4, 3, 2, 2, 1, 1]
ASCI = 65


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def rules():
    cls()
    print("We are playing ... BATTLESHIPS!\n")
    print("\nThe aim of the game is to sink all the enemy ships before he sinks yours.")
    print("Each player has a fleet of seven ships:\n")
    print("   1x Carrier     ... 5 squares      1x Battleship  ... 4 squares")
    print("   1x Cruiser     ... 3 squares      2x Destroyer   ... 2 squares")
    print("   2x Submarine   ... 1 square\n")
    print("In your turn enter the coordinates of a square, first row and then column, e.g. >>> C6")
    print("If there is a ship on this square, the computer shows HIT and marks it with a cross.")
    print("In the opposite case the computer shows MISS and marks the square with a dot. Now it's computer's turn.")
    print("\nIf you'll need this help any time in the future, write HELP instead of the coordinates.")
    input(f"\n\nIs everything clear? Press ENTER to continue.")
    show_map()
    print()


def show_map():
    cls()
    print()
    for r in range(SIZE):
        prt = "  "
        if r == 0:
            for p in range(2):
                for c in range(SIZE):
                    prt = prt + "  " + (str(c)) + " "
                prt = prt + " " * 13
            print("   " + prt)
            prt = "  "
        print("     " + "+---"*SIZE + "+" + " " * 12 + "+---"*SIZE + "+")
        for p in range(2):
            prt = prt + str(chr(ASCI+r)) + " "
            for c in range(SIZE):
                if p == 0:
                    map = str(player_map_visible[r][c])
                else:
                    map = str(computer_map_visible[r][c])
                prt = prt + "| " + map + " "
            prt = prt + "|          "
        print(" " + prt)
    print("     " + "+---"*SIZE + "+" + " " * 12 + "+---"*SIZE + "+")
    running_score()


def running_score():
    if init_score == True:
        p_left = len(SETUP)
        c_left = len(SETUP)
    else:
        p_left = len(player_ships)
        c_left = len(computer_ships)
    p_killed = len(SETUP)-p_left
    c_killed = len(SETUP)-c_left
    score = "\n     "
    score = score + player_name + ":" + " " * (20-len(player_name))
    score = score + f"destroyed {p_killed}"
    score = score + f" | left {p_left}"
    score = score + " " * 12 + "COMPUTER:" + " " * 12
    score = score + f"destroyed {c_killed}"
    score = score + f" | left {c_left}\n"
    print(score)


def auto_setup():
    ships = []
    filled = []
    for n in SETUP:
        ship = []
        while len(ship) != n:
            if len(ship) == 0:
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
                    ship = []
                    continue
            if coord not in ship and coord not in filled:
                ship.append(coord)
            else:
                ship = []
        ships.append(ship)
        filled = list(set(filled + ship + around(ship)))
    return ships


def around(ship):
    around_ship = []
    for part in ship:
        # check up
        if part // 10 > 0 and part-10 not in ship:
            around_ship.append(part-10)
        # check down
        if part // 10 < 9 and part+10 not in ship:
            around_ship.append(part+10)
        # check left
        if part % 10 > 0 and part-1 not in ship:
            around_ship.append(part-1)
        # check right
        if part % 10 < 9 and part+1 not in ship:
            around_ship.append(part+1)
        # check top left
        if part // 10 > 0 and part % 10 > 0 and part-11 not in ship:
            around_ship.append(part-11)
        # check top right
        if part // 10 > 0 and part % 10 < 9 and part-9 not in ship:
            around_ship.append(part-9)
        # check bottom left
        if part // 10 < 9 and part % 10 > 0 and part+9 not in ship:
            around_ship.append(part+9)
        # check bottom right
        if part // 10 < 9 and part % 10 < 9 and part+11 not in ship:
            around_ship.append(part+11)
    around_ship = list(set(around_ship))
    return around_ship


def if_error():
    show_map()
    print("\nYou have to enter the right coordinates.")


def player_turn(answer):
    global fill
    coord = answer[0] * 10 + answer[1]
    if coord in player_moves:
        show_map()
        print(
            f"\nThe coordinate {chr(answer[0]+ASCI)}{answer[1]} has been already marked.")
        result = ""
        return True, False, result
    player_moves.append(coord)
    for ship in computer_ships:
        if coord in ship:
            player_hits.append(coord)
            computer_map_visible[answer[0]][answer[1]] = "X"
            message = ship_destroyed(
                player_hits, computer_ships, computer_map_visible, player_moves)
            result = "HIT! " + message
            fill = False
    if coord not in player_hits:
        computer_map_visible[answer[0]][answer[1]] = "."
        result = "MISS!\n"
    return False, True, result


def auto_fill():
    global fill
    fill = True
    for i in range(SIZE*SIZE):
        if i not in player_moves:
            answer = [i // SIZE, i % SIZE]
            return answer


def computer_turn():
    for ship in player_ships:
        if coord in ship:
            computer_hits.append(coord)
            player_map_visible[r][c] = "X"
            message = ship_destroyed(
                computer_hits, player_ships, player_map_visible, computer_moves)
            result = "HIT! " + message
    if coord not in computer_hits:
        player_map_visible[r][c] = "."
        result = "MISS!\n"
    return True, False, result


def ship_destroyed(hits, ships, map_visible, moves):
    for ship in ships:
        length = len(ship)
        for i in ship:
            if i in hits:
                length -= 1
        if length <= 0:
            ships.remove(ship)
            around_ship = around(ship)
            for i in around_ship:
                r = i // SIZE
                c = i % SIZE
                map_visible[r][c] = "."
                moves.append(i)
            return "The ship was DESTROYED.\n"
    return "\n"


def game_over(ships, winner):
    if len(ships) == 0:
        print(f"GAME OVER! The winner is {winner}.\n")
        sys.exit()


player_moves = []
player_hits = []
computer_moves = []
computer_hits = []

init_score = True
player_name = "PLAYER ONE"

player_map_visible = [[" " for i in range(SIZE)] for j in range(SIZE)]
computer_map_visible = [[" " for i in range(SIZE)] for j in range(SIZE)]

show_map()

player_name = input("\nTo start please enter your name >>> ")
if len(player_name) == 0:
    player_name = "PLAYER ONE"
player_name = player_name.upper()
answer = ""

player_ships = auto_setup()
computer_ships = auto_setup()


player = True
computer = False
fill = False

for ship in player_ships:
    for part in ship:
        r = part // SIZE
        c = part % SIZE
        player_map_visible[r][c] = "\033[90m" + "O" + "\033[0m"
        init_score = False
show_map()
print("\nEverything is ready. To see some instructions, type HELP.")

while True:
    player_result = ""
    computer_result = ""

    while player == True:
        answer = ""
        if fill == True:
            answer = auto_fill()
        else:
            answer = input(
                "Please enter the coordinates of row and column, e.g. E6 >>> ")
            if answer.upper() == "HELP":
                rules()
                break
            elif answer.upper() == "FILL":
                answer = auto_fill()
            elif len(answer) < 2 or len(answer) > 2:
                if_error()
                break
            else:
                answer = list(answer)
                answer[0] = ord(answer[0].upper()) - ASCI
                if answer[0] < 0 or answer[0] > SIZE-1:
                    if_error()
                    break
                try:
                    answer[1] = int(answer[1])
                except ValueError:
                    if_error()
                    break
        player, computer, player_result = player_turn(answer)

    while computer == True:
        coord = 100
        while coord in computer_moves or coord > 99:
            coord = random.randint(0, SIZE*SIZE-1)
        if len(computer_hits) > 0:
            for hit in computer_hits:
                if hit + 1 not in computer_moves and hit % SIZE < SIZE-1:
                    coord = hit + 1
                elif hit + 10 not in computer_moves and hit // SIZE < SIZE-1:
                    coord = hit + 10
                elif hit - 1 not in computer_moves and hit % SIZE > 0:
                    coord = hit - 1
                elif hit - 10 not in computer_moves and hit // SIZE > 0:
                    coord = hit - 10
        computer_moves.append(coord)
        r = coord // SIZE
        c = coord % SIZE
        player, computer, computer_result = computer_turn()

    if player_result != "":
        print("Searching ...")
        time.sleep(0.5)
        show_map()
        print(
            f"\nYou fire to the coordinate: {chr(answer[0]+ASCI)}{answer[1]}")
        print(player_result)
        game_over(computer_ships, player_name)
        print(f"Computer fires to the coordinate: {chr(r+ASCI)}{c}")
        print(computer_result)
        game_over(player_ships, "COMPUTER")
