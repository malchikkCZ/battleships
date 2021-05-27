import time
from constants import ASCI, SETUP, SIZE
from players import Human, Computer
from ui import Window


window = Window()

player1 = Human(SETUP)
player2 = Computer(SETUP)

window.update(player1, player2)

player1.name = window.get_player_name()
player1.show_ships()

window.update(player1, player2)

print("\nEverything is ready. To see some instructions, type HELP.")

game = True

while game:
  
    coord1 = window.get_player_move(player1)
    if coord1 == None:
        window.update(player1, player2)
        continue

    result1 = player1.attack(player2, coord1)
        
    print("Counting ...")
    time.sleep(0.5)
    
    window.update(player1, player2)

    result = f"\nYou fire to the coordinate: {chr(coord1//SIZE+ASCI)}{coord1%SIZE}\n" + result1
    
    if player1.is_victorious(player2):
        print(result)
        print(f"GAME OVER! The winner is {player1.name}.\n")
        game = False
        continue

    coord2 = player2.get_computer_move()
    result2 = player2.attack(player1, coord2)

    window.update(player1, player2)

    result += f"\nComputer fires to the coordinate: {chr(coord2//SIZE+ASCI)}{coord2%SIZE}\n" + result2
    
    print(result)

    if player2.is_victorious(player1):
        print(f"GAME OVER! The winner is {player2.name}.\n")
        game = False
        continue
