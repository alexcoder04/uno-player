
import os


class CmdLineDataloader:
    def __init__(self) -> None:
        pass

    def get_players_number(self):
        while True:
            try:
                return int(input("players number: "))
            except ValueError:
                continue

    def read_card(self, prompt):
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
            special = 1 if color == "s" else 0
            return color, number, special

    def get_how_many_to_pull(self):
        inp = input("Do I have to pull? If so, how much: ")
        try:
            return int(inp)
        except ValueError:
            return 0

    def clear(self):
        input("Press <enter> to clear the screen and continue")
        os.system("clear")
