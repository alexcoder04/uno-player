
"""
Command-Line Interface for entering the cards and other data
"""

import os


class CmdLineDataloader:
    def __init__(self) -> None:
        pass

    def get_players_number(self) -> int:
        while True:
            try:
                return int(input("Players number: "))
            except ValueError:
                print("Sorry, this is not a number")
                continue

    def read_card(self, prompt: str) -> (str, str, bool):
        while True:
            try:
                [color, number] = input(prompt).split(",")
            except ValueError:
                print("Sorry, cannot read your input")
                continue
            color, number = color.strip(), number.strip()
            if color not in ("r", "g", "b", "y", "s"):
                print("Sorry, invalid color, use (r,g,b,y,s)")
                continue
            if color != "s" and number not in ("0","1","2","3","4","5","6","7","8","9","r","n","+2","j"):
                print("Sorry, invalid number, use(0,1,2,3,4,5,6,7,8,9,r,n,+2,j)")
                continue
            if color == "s" and number not in ("j","+4"):
                print("Sorry, invalid number, use (j,+4)")
                continue
            special = True if color == "s" else False
            return color, number, special

    def get_how_many_to_pull(self) -> int:
        inp = input("Do I have to pull? If so, how much: ")
        try:
            return int(inp)
        except ValueError:
            return 0

    def clear(self) -> None:
        input("Press <enter> to clear the screen and continue")
        os.system("clear")

