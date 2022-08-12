#!/usr/bin/env python3
#        _                        _            ___  _  _   
#   __ _| | _____  _____ ___   __| | ___ _ __ / _ \| || |  
#  / _` | |/ _ \ \/ / __/ _ \ / _` |/ _ \ '__| | | | || |_ 
# | (_| | |  __/>  < (_| (_) | (_| |  __/ |  | |_| |__   _|
#  \__,_|_|\___/_/\_\___\___/ \__,_|\___|_|   \___/   |_|  
# 
# Copyright (c) 2021-2022 alexcoder04 <https://github.com/alexcoder04>
# 
# a script that can play the Uno card game
# requires: sqlite3
#

import random
# classes for data input and database
# can be replaced with any compatible classes (e. g. for AI-based camera input)
from dataloader import CmdLineDataloader
from database import SqliteDatabase


CARDS_BEGIN = 7


class UnoPlayer:
    def __init__(self) -> None:
        print("Creating Uno player...")
        self.NORMAL_COLORS = {"r", "g", "b", "y"}
        print("Creating Data Loader...")
        self.dl = CmdLineDataloader()
        print("Creating Database...")
        self.db = SqliteDatabase()
        self.made_first_move = False
        self.skip_pull = None
        self.players_number = self.dl.get_players_number()
        print("Reading own cards...")
        for _ in range(CARDS_BEGIN):
            color, number, special = self.dl.read_card("given card: ")
            self.db.add_card(color, number, special)
        self.dl.clear()
        print("I am now ready to play!")

    # the best color, which we wish if we put a joker
    def best_color(self):
        max_num = 0
        selected = self.NORMAL_COLORS.copy()
        for color in self.NORMAL_COLORS:
            length = len(self.db.get_cards_by_color(color))
            if length > max_num:
                selected = {color}
                max_num = length
                continue
            if length == max_num:
                selected.add(color)
        return random.choice(list(selected))

    # output a message on the console
    def say(self, message):
        message = "-----" + message + "-----"
        header = len(message) * "-"
        print(header)
        print(message)
        print(header)

    # put pulled card if it matches
    def handle_pull(self, curColor, curNumber):
        print("Well, I have to pull...")
        color, number, special = self.dl.read_card("I pulled: ")
        if special == 1:
            self.say("put pulled card")
            self.say(f"I want {self.best_color()}!")
            return
        if color == curColor or number == curNumber:
            self.say("put pulled card")
            return
        self.db.add_card(color, number, special)
        self.dl.clear()

    # main game loop which runs
    def game_loop(self):
        while True:
            cards = self.db.get_cards_all()
            if len(cards) == 1:
                self.say("UNO")
            if len(cards) == 0:
                print("WON!")
                self.end_game()
                break
            if self.made_first_move:
                print("Move ended")
            if self.skip_pull is None:
                pull = self.dl.get_how_many_to_pull()
                if pull != 0:
                    for _ in range(pull):
                        color, number, special = self.dl.read_card("pull card: ")
                        self.db.add_card(color, number, special)
                    self.dl.clear()
                    continue
                curColor, curNumber, _ = self.dl.read_card("current: ")
            else:
                (curColor, curNumber) = self.skip_pull
                self.skip_pull = None
            possible = self.db.get_cards_matching_no_special(curColor, curNumber)
            if len(possible) == 0:
                res = self.db.get_cards_special()
                if len(res) == 0:
                    self.handle_pull(curColor, curNumber)
                    continue
                if len(res) == 1:
                    (card_id, color, number, special) = res[0]
                    self.db.delete_card_by_id(card_id)
                    self.say(f"Put {color} {number}")
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
                self.db.delete_card_by_id(card_id)
                self.say(f"put {color} {number}")
                self.say(f"I want {self.best_color()}!")
                continue
            (card_id, color, number, special) = random.choice(possible)
            self.db.delete_card_by_id(card_id)
            self.say(f"Put {color} {number}")
            if number in ("+2", "n", "r") and self.players_number == 2:
                self.skip_pull = (color, number)

    def end_game(self):
        print("Closing Database...")
        self.db.close()
        print("Thank you very much for the game!")


if __name__ == "__main__":
    player = UnoPlayer()
    try:
        player.game_loop()
    except KeyboardInterrupt:
        player.end_game()

