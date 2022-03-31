#!/usr/bin/env python3
#        _                        _            ___  _  _   
#   __ _| | _____  _____ ___   __| | ___ _ __ / _ \| || |  
#  / _` | |/ _ \ \/ / __/ _ \ / _` |/ _ \ '__| | | | || |_ 
# | (_| | |  __/>  < (_| (_) | (_| |  __/ |  | |_| |__   _|
#  \__,_|_|\___/_/\_\___\___/ \__,_|\___|_|   \___/   |_|  
# 
# Copyright (c) 2021 alexcoder04 <https://github.com/alexcoder04>
# 
# a script that can play the Uno card game
# requires: sqlite3
#

import os
import random
import sqlite3


CARDS_BEGIN = 7


class UnoPlayer:
    def __init__(self) -> None:
        print("Creating Uno player...")
        print("Creating database...")
        self.made_first_move = False
        self.skip_pull = None
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE mycards (id integer PRIMARY KEY AUTOINCREMENT, color text, number text, special boolean)")
        self.players_number = self.get_int("players number: ")
        print("reading own cards...")
        for _ in range(CARDS_BEGIN):
            color, number, special = self.get_card("given card: ")
            self.cursor.execute(f"INSERT INTO mycards (color, number, special) VALUES ('{color}', '{number}', {special})")
        self.conn.commit()
        self.clear_screen()
        print("I am now ready to play!")

    def best_color(self):
        max_num = 0
        selected = {"r", "g", "b", "y"}
        for color in {"r", "g", "b", "y"}:
            self.cursor.execute(f"SELECT * FROM mycards WHERE color = '{color}'")
            length = len(self.cursor.fetchall())
            if length > max_num:
                selected = {color}
                max_num = length
                continue
            if length == max_num:
                selected.add(color)
        return random.choice(list(selected))

    def clear_screen(self):
        input("Press <enter> to clear the screen and continue")
        os.system("clear")

    def get_all_cards(self):
        self.cursor.execute("SELECT * FROM mycards")
        return self.cursor.fetchall()

    def get_int(self, prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                continue

    def get_card(self, prompt):
        while True:
            [color, number] = input(prompt).split(",")
            color, number = color.strip(), number.strip()
            if color not in ("r", "g", "b", "y", "s"):
                print("invalid color")
                continue
            if color != "s" and number not in ("0","1","2","3","4","5","6","7","8","9","r","n","+2","j"):
                print("invalid number")
                continue
            if color == "s" and number not in ("j","+4"):
                print("invalid number")
                continue
            special = 1 if color == "s" else 0
            return color, number, special

    def get_pull_number(self):
        inp = input("pull: ")
        try:
            return int(inp)
        except ValueError:
            return 0

    def say(self, message):
        message = "-----" + message + "-----"
        header = len(message) * "-"
        print(header)
        print(message)
        print(header)

    def handle_pull(self, curColor, curNumber):
        color, number, special = self.get_card("I pulled: ")
        if special == 1:
            self.say("put pulled card")
            self.say(f"I want {self.best_color()}!")
            return
        if color == curColor or number == curNumber:
            self.say("put pulled card")
            return
        self.cursor.execute(f"INSERT INTO mycards (color, number, special) VALUES ('{color}', '{number}', {special})")
        self.conn.commit()
        self.clear_screen()

    def game_loop(self):
        while True:
            cards = self.get_all_cards()
            if len(cards) == 1:
                self.say("UNO")
            if len(cards) == 0:
                print("WON!")
                self.end_game()
                break
            if self.made_first_move:
                print("Zug beendet")
            if self.skip_pull is None:
                pull = self.get_pull_number()
                if pull != 0:
                    for _ in range(pull):
                        color, number, special = self.get_card("pull card: ")
                        self.cursor.execute(f"INSERT INTO mycards (color, number, special) VALUES ('{color}', '{number}', {special})")
                    self.conn.commit()
                    self.clear_screen()
                    continue
                curColor, curNumber, _ = self.get_card("current: ")
            else:
                (curColor, curNumber) = self.skip_pull
                self.skip_pull = None
            self.cursor.execute(f"SELECT * FROM mycards WHERE special = 0 AND (color = '{curColor}' OR number = '{curNumber}')")
            possible = self.cursor.fetchall()
            if len(possible) == 0:
                self.cursor.execute(f"SELECT * FROM mycards WHERE special = 1")
                res = self.cursor.fetchall()
                if len(res) == 0:
                    self.handle_pull(curColor, curNumber)
                    continue
                if len(res) == 1:
                    (card_id, color, number, special) = res[0]
                    self.cursor.execute(f"DELETE FROM mycards WHERE id = {card_id}")
                    self.conn.commit()
                    self.say(f"put {color} {number}")
                    self.say(f"I want {self.best_color()}!")
                    if number == "+4" and self.players_number == 2:
                        self.skip_pull = (self.best_color(), number)
                    continue
                jokers = [i for i in res if i[2] != "+4"]
                plus4s = [i for i in res if i[2] == "+4"]
                if len(jokers) == 0:
                    (card_id, color, number, special) = random.choice(plus4s)
                    if self.players_number == 2:
                        self.skip_pull = (self.best_color(), number)
                else:
                    (card_id, color, number, special) = random.choice(jokers)
                self.cursor.execute(f"DELETE FROM mycards WHERE id = {card_id}")
                self.conn.commit()
                self.say(f"put {color} {number}")
                self.say(f"I want {self.best_color()}!")
                continue
            (card_id, color, number, special) = random.choice(possible)
            self.cursor.execute(f"DELETE FROM mycards WHERE id = {card_id}")
            self.conn.commit()
            self.say(f"put {color} {number}")
            if number in ("+2", "n", "r") and self.players_number == 2:
                self.skip_pull = (color, number)

    def end_game(self):
        print("Closing database...")
        self.conn.close()
        print("Thank you very much for the game!")


if __name__ == "__main__":
    player = UnoPlayer()
    try:
        player.game_loop()
    except KeyboardInterrupt:
        player.end_game()

