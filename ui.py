import os
from constants import ASCI, SIZE


class Window:

    def __init__(self):
        pass

    def update(self, player1, player2):
        self.update_board(player1, player2)
        self.update_score(player1, player2)

    def update_board(self, player1, player2):
        os.system('cls' if os.name == 'nt' else 'clear')
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
                        map = str(player1.board[r][c])
                    else:
                        map = str(player2.board[r][c])
                    prt = prt + "| " + map + " "
                prt = prt + "|          "
            print(" " + prt)
        print("     " + "+---"*SIZE + "+" + " " * 12 + "+---"*SIZE + "+")

    def update_score(self, player1, player2):
        p_left = len(player1.ships)
        c_left = len(player2.ships)
        p_killed = len(player1.setup)-p_left
        c_killed = len(player2.setup)-c_left
        score = "\n     "
        score = score + player1.name + ":" + " " * (20-len(player1.name))
        score = score + f"destroyed {p_killed}"
        score = score + f" | left {p_left}"
        score = score + " " * 12 + player2.name + ":" + " " * (20-len(player2.name))
        score = score + f"destroyed {c_killed}"
        score = score + f" | left {c_left}\n"
        print(score)

    def show_rules(self):
        os.system('cls' if os.name == 'nt' else 'clear')
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

    def get_player_name(self):
        name = input("\nTo start please enter your name >>> ")
        if len(name) > 0:
            return name.upper()
        else:
            return "PLAYER ONE"

    def get_player_move(self, player):
        answer = ""
        if player.fill == True:
            answer = player.auto_fill()
        else:
            answer = input("Please enter the coordinates of row and column, e.g. E6 >>> ")
            if answer.upper() == "HELP":
                self.show_rules()
                return None
            elif answer.upper() == "FILL":
                answer = player.auto_fill()
            elif len(answer) < 2 or len(answer) > 2:
                print("\nYou have to enter the right coordinates.")
                return self.get_player_move(player)
            else:
                answer = list(answer)
                answer[0] = ord(answer[0].upper()) - ASCI
                if answer[0] < 0 or answer[0] > SIZE-1:
                    print("\nYou have to enter the right coordinates.")
                    return self.get_player_move(player)
                try:
                    answer[1] = int(answer[1])
                except ValueError:
                    print("\nYou have to enter the right coordinates.")
                    return self.get_player_move(player)
        
        coord = answer[0] * SIZE + answer[1]
        if coord in player.moves:
            print(f"\nThe coordinate {chr(answer[0]+ASCI)}{answer[1]} has been already marked.")
            return self.get_player_move(player)
        else:
            return coord
