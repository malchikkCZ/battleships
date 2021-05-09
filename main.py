# Na motivy hry Battleships naprogramoval Malchikk.CZ (C)
# Prvni verze (C) 25.3.2021 - Chybi doprogramovat skript pro rucni rozdeleni lodi hracem.

import sys
import os
import random
import time

SIZE = 10                                                 # definuje velikost herni mapy
SETUP = [5, 4, 3, 2, 2, 1, 1]                             # definuje velikost lodi
ASCI = 65                                                 # konstanta pro prepocet ASCII

def cls():
  '''Tato funkce smaze obrazovku v ruznych OS.'''
  os.system('cls' if os.name=='nt' else 'clear')

def rules(cont):
  '''Tato funkce vypise na obrazovku napovedu.'''
  cls()
  print("Hrajeme hru ... BATTLESHIPS!\n")
  print("\nCilem hry je potopit protivnikovy lode drive, nez on potopi ty tvoje.")
  print("Kazdy hrac ma k dispozici flotilu sedmi lodi:\n")
  print("   1x Letadlova lod ... 5 policek      1x Bitevnik      ... 4 policka")
  print("   1x Kriznik       ... 3 policka      2x Torpedoborec  ... 2 policka")
  print("   2x Ponorka       ... 1 policko\n")
  print("Pokud jsi na tahu, zadej souradnice v poradi rada a sloupec, tedy napr. >>> C6")
  print("Je li na danem poli lod, pocitac ohlasi ZASAH a oznaci pole krizkem.")
  print("V opacnem pripade ohlasi VODA a oznaci pole teckou. Pote utoci pocitac na tve lode.")
  print("\nBudes-li v budoucnu potrebovat tuto napovedu, zadej misto souradnic slovo HELP.")
  input(f"\n\nJe vsechno jasne? Pro {cont} hry stiskni ENTER.")
  show_map()
  print()

def show_map():
  '''Tato funkce vykresli na obrazovku dva herni plany vedle sebe.'''
  cls()
  print()
  for r in range(SIZE):
    prt = "  "
    if r == 0:
      for p in range(2):  
        for c in range(SIZE):
          prt = prt + "  " + (str(c)) + " "               # vyplni vodorovne souradnice
        prt = prt + " " * 13
      print("   " + prt)
      prt = "  "
    print("     " + "+---"*SIZE + "+" + " " * 12 + "+---"*SIZE + "+")
    for p in range(2):
      prt = prt + str(chr(ASCI+r)) + " "                  # vyplni svisle souradnice
      for c in range(SIZE):
        if p == 0:
          map = str(player_map_visible[r][c])
        else:
          map = str(computer_map_visible[r][c])
        prt = prt + "| " + map + " "
      prt = prt + "|          "
    print(" " + prt )
  print("     " + "+---"*SIZE + "+" + " " * 12 + "+---"*SIZE + "+")
  running_score()                                         # zavola funkci pro vypsani skore


def running_score():
  '''Tato funkce slouzi k vypsani prubezneho score pod herni mapou.'''
  if init_score == True:                                 # overi, zda se jedna o prvni beh funkce
    p_left = len(SETUP)
    c_left = len(SETUP)
  else:
    p_left = len(player_ships)
    c_left = len(computer_ships)
  p_killed = len(SETUP)-p_left
  c_killed = len(SETUP)-c_left
  score = "\n     "
  score = score + player_name + ":" + " " * (20-len(player_name))
  score = score + f" zniceno {p_killed}"
  score = score + f" | zbyva {p_left}"
  score = score + " " * 12 + "COMPUTER:" + " " * 12
  score = score + f" zniceno {c_killed}"
  score = score + f" | zbyva {c_left}\n"
  print(score) 

def player_setup():
  '''Tato funkce umisti hracovy lode na herni plan.'''
  # tuto cast kodu je potreba doprogramovat, aby si hrac mohl sam rozlozit lode na mapu

def auto_setup():
  '''Tato funkce automaticky rozmisti lode na herni plan.'''
  ships = []
  filled = []
  for n in SETUP:                                       # nastavi velikost konkretni lode
    ship = []
    while len(ship) != n:                               # cyklus pokracuje dokud nejsou umisteny vsechny casti lode
      if len(ship) == 0:
        coord = random.randint(0, SIZE*SIZE-1)          # prvni cast lode umisti nahodne
      else:
        direction = random.randint(0, 3)                # dalsi casti umistuje v nahodnych smerech tak, aby navazovaly
        if direction == 0 and coord % SIZE < 9:
          coord = coord + 1
        elif direction == 1 and coord // SIZE < 9:
          coord = coord + SIZE
        elif direction == 2 and coord % SIZE > 0:
          coord = coord - 1
        elif direction == 3 and coord // SIZE > 0:
          coord = coord - SIZE
        else:
          ship = []                                     # pokud nemuze nejakou cast umistit, zacne znovu
          continue
      if coord not in ship and coord not in filled:     # overi, zda na dane souradnici neni jina lod nebo okoli lodi
        ship.append(coord)                              # pak ulozi souradnici do polohy lodi
      else:
        ship = []                                       # pokud nemuze nejakou cast umistit, zacne znovu
    ships.append(ship)                                  # jakmile je lod hotova, ulozi jeji souradnice
    filled = list(set(filled + ship + around(ship)))    # urci okoli lodi a vse ulozi, aby se lode neprekryvaly nebo nedotykaly
  return ships

def around(ship):
  '''Tato funkce urci souradnice poli okolo lodi.'''
  around_ship = []
  for part in ship:                                     # pro kazdou cast lodi
    # check up
    if part // 10 > 0 and part-10 not in ship:          # pokud je v danem smeru mozne neco umistit
      around_ship.append(part-10)                       # oznaci to jako okoli lodi
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
  around_ship = list(set(around_ship))                  # ze seznamu okoli lodi odstrani duplicity
  return around_ship

def if_error():
  '''Tato funkce vypise chybovou hlasku pri spatne zadanych souradnicich.'''
  show_map()
  print("\nMusis zadat souradnice ve spravnem formatu.")

def player_turn(answer):
  '''Tato funkce vyhodnoti hracuv tah.'''
  global fill                                           # globalni promenna fill pomoha pri automatickem vyplnovani
  coord = answer[0] * 10 + answer[1]                    # prevede uzivatelem zadane souradnice na strojove
  if coord in player_moves:                             # pokud uz je toto misto zname, vypise chybu
    show_map()
    print(f"\nSouradnice {chr(answer[0]+ASCI)}{answer[1]} uz byla odkryta.")
    result = ""
    return True, False, result
  player_moves.append(coord)                            # prida souradnici do seznamu hracovych tahu
  for ship in computer_ships:                           # pro kazdou lod z pocitacovy flotily
    if coord in ship:                                   # pokud je tato souradnice soucasti lodi
      player_hits.append(coord)                         # prida souradnici do seznamu hracovych zasahu
      computer_map_visible[answer[0]][answer[1]] = "X"  # a oznaci ji na mape symbolem X
      message = ship_destroyed(player_hits, computer_ships, computer_map_visible, player_moves)
      result = "ZASAH! " + message
      fill = False                                      # pokud doslo k zasahu automatickym vyplnovanim, toto se zastavi
  if coord not in player_hits:                          # pokud souradnice nevedla k zasahu
    computer_map_visible[answer[0]][answer[1]] = "."    # oznaci se na mape symbolem .
    result = "VODA!\n"
  return False, True, result                            # prepne na tah pocitace a vrati vysledek
  
def auto_fill():
  '''Tato funkce spusti automaticke vyplnovani od prvniho policka.'''
  global fill                                           # globalni promenna fill pomoha pri automatickem vyplnovani
  fill = True                                           # zapne automaticke vyplnovani mapy
  for i in range(SIZE*SIZE):                            # postupne generuje souradnice od 0 do 99
    if i not in player_moves:                           # pokud toto pole jeste neni zname
      answer = [i // SIZE, i % SIZE]                    # posle ho zpatky programu ve formatu, jako by ho zadal hrac z klavesnice
      return answer

def computer_turn():
  '''Tato funkce vyhodnoti tah pocitace.'''
  for ship in player_ships:                             # pro kazdou lod z hracovy flotily
    if coord in ship:                                   # pokud je tato souradnice soucasti lodi
      computer_hits.append(coord)                       # prida souradnici do seznamu pocitacovych zasahu
      player_map_visible[r][c] = "X"                    # a oznaci ji na mape symbolem X
      message = ship_destroyed(computer_hits, player_ships, player_map_visible, computer_moves)
      result = "ZASAH! " + message
  if coord not in computer_hits:                        # pokud souradnice nevedla k zasahu
    player_map_visible[r][c] = "."                      # oznaci se na mape symbolem .
    result = "VODA!\n"
  return True, False, result                            # prepne na tah hrace a vrati vysledek

def ship_destroyed(hits, ships, map_visible, moves):
  '''Tato funkce overi a vyhodnoti potopeni lodi.'''
  for ship in ships:                                    # pro kazdou lod ve flotile
    length = len(ship)                                  # urci delku lodi
    for i in ship:
      if i in hits:                                     # za kazdou souradnici v seznamu zasahu
        length -= 1                                     # zkrati delku lodi o 1
    if length <= 0:                                     # pokud je delka lodi 0
      ships.remove(ship)                                # vymaze ji z flotily
      around_ship = around(ship)                        # a urci jeji okoli
      for i in around_ship:
        r = i // SIZE
        c = i % SIZE
        map_visible[r][c] = "."                         # vyteckuje okoli lodi na mape
        moves.append(i)                                 # a vsechny takto vyteckovane souradnice prida do seznamu tahu
      return "Lod byla POTOPENA.\n"
  return "\n"

def game_over(ships, winner):
  '''Tato funkce overi, zda nastal konec hry.'''
  if len(ships) == 0:                                   # pokud ve flotile nezbyva zadna lod
    print(f"KONEC HRY! Vitezem se stava {winner}.\n")   # vyhodnoti se vitez
    sys.exit()                                          # a program se ukonci


player_moves = []                                       # urcime promenne, se kterymi budeme pracovat
player_hits = []
computer_moves = []
computer_hits = []

init_score = True
player_name = "PLAYER ONE"

player_map_visible = [[" " for i in range(SIZE)] for j in range(SIZE)]
computer_map_visible = [[" " for i in range(SIZE)] for j in range(SIZE)]

show_map()                                              # po spusteni programu se vykresli prazdna mapa

player_name = input("\nAbychom mohli zacit, musis nejprve zadat sve jmeno >>> ")
if len(player_name) == 0:
  player_name = "PLAYER ONE"                            # pokud hrac nezada jmeno, pouzije se defaultni hodnota
player_name = player_name.upper()                       # at hrac zada cokoli, prevede se to na kapitalky
answer = ""

# tahle cast kodu bude vyhodnocovat, zda si chce hrac rozdelit lode sam
while answer not in ["a", "A"]: # sem doplnit "n", "N"
  show_map()
#  answer = input("\nChces, aby pocitac rozmistil lode na herni plochu misto tebe (A/N) >>> ")
#  answer = answer.upper()
  answer = "A" # vymazat
  if answer == "A":
    player_ships = auto_setup()
    computer_ships = auto_setup()
  elif answer == "N":
    input("Je mi lito, ale rucni rozlozeni lodi tento program jeste neumi. Stiskni ENTER.")
  else:
    input("Musis zadat A jako ano nebo N jako ne, jinak ti neumim pomoct. Stiskni ENTER.")
# tahle cast kodu bude vyhodnocovat, zda si chce hrac rozdelit lode sam

player = True
computer = False                                        # urcuje, kdo je zacinajici hrac
fill = False                                            # ve vychozim stavu je automaticke vyplneni vypnute

for ship in player_ships:
  for part in ship:                                     # vyznaci hracovy lode na mape pomoci symbolu 0
    r = part // SIZE
    c = part % SIZE
    player_map_visible[r][c] = "\033[90m" + "O" + "\033[0m"
    init_score = False                                  # ukonci proces inicializace, odted se bude vypisovat realne skore
show_map()                                              # vykresli mapu s vyznacenymi lodemi hrace
print("\nVse je pripraveno, zaciname. Pro vyvolani napovedy napis slovo HELP.")

while True:                                             # tady zacina bezet samotny program
  player_result = ""
  computer_result = ""                                  # nastavi prazdne hodnoty pro vysledky tahu hrace a pocitace

  while player == True:                                 # zacatek tahu hrace
    answer = ""                                         # vychozi prazdna hodnota souradnic
    if fill == True:
      answer = auto_fill()                              # pokud je nastavene automaticke vyplnovani, tak vyplnuj
    else:
      answer = input("Zadej souradnice v poradi rada a sloupec, napr. E6 >>> ")
      if answer.upper() == "HELP":                      # pokud hrac zadal HELP, vypise pravidla hry
        rules("pokracovani")
        break
      elif answer.upper() == "FILL":                    # pokud hrac zadal FILL, zapne automaticke vyplnovani
        answer = auto_fill()
      elif len(answer) < 2 or len(answer) > 2:          # pokud zadal souradnice spatne, vypise se chyba
        if_error()
        break
      else:
        answer = list(answer)                           # rozdeli odpoved hrace na dve hodnoty
        answer[0] = ord(answer[0].upper()) - ASCI       # prvni hodnotu prevede na ASCII kod
        if answer[0] < 0 or answer[0] > SIZE-1:         # pokud je hodnota mimo rozsah, vypise chybu
          if_error()
          break
        try:
          answer[1] = int(answer[1])                    # prevede druhou hodnotu na cele cislo
        except ValueError:                              # pokud to nejde, vypise chybu
          if_error()
          break
    player, computer, player_result = player_turn(answer)     # vyhodnoti tah hrace a vrati vysledek
   
  while computer == True:                               # zacatek tahu pocitace
    coord = 100                                         # vychozi hodnota souradnice
    while coord in computer_moves or coord > 99:
      coord = random.randint(0, SIZE*SIZE-1)            # generuje nahodne cislo, dokud nenajde to spravne
    if len(computer_hits) > 0:                          # pokud je ale v seznamu zasahu nejaka hodnota, overi, zda muze strilet kolem ni
      for hit in computer_hits:                         # to je dulezite, aby pocitac nejprve dokoncil potopeni lodi, nez zacne zase strilet nahodne
        if hit + 1 not in computer_moves and hit % SIZE < SIZE-1:
          coord = hit + 1
        elif hit + 10 not in computer_moves and hit // SIZE < SIZE-1:
          coord = hit + 10
        elif hit - 1 not in computer_moves and hit % SIZE > 0:
          coord = hit - 1
        elif hit - 10 not in computer_moves and hit // SIZE > 0:
          coord = hit - 10
    computer_moves.append(coord)                        # zapise souradnici do seznamu pocitacovych tahu
    r = coord // SIZE
    c = coord % SIZE
    player, computer, computer_result = computer_turn()       # vyhodnoti tah pocitace a vrati vysledek

  if player_result != "":                               # pokud mam relevantni vysledky tak pokracuju
    print("Pocitam ...")
    time.sleep(0.5)                                     # chvilka napeti
    show_map()
    print(f"\nStrilis na souradnici: {chr(answer[0]+ASCI)}{answer[1]}")
    print(player_result)                                # vypise vysledek hracova tahu
    game_over(computer_ships, player_name)              # overi, zda hrac vyhral
    print(f"Pocitac strili na souradnici: {chr(r+ASCI)}{c}")
    print(computer_result)                              # vypise vysledek pocitacova tahu
    game_over(player_ships, "COMPUTER")                 # overi, zda pocitac vyhral
