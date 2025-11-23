from pgzero.builtins import Actor
from enemy import Enemy
from moeda import Moeda
from player import Player
from princess import Princess

def load_level(path, player):
    blocks = []
    coins = []
    enemys = []
    fatals = []
    wins = []
    princess = []
    with open(path) as f:
        lines = f.readlines()

    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if char == "#":
                blocks.append(Actor("block", (x*32, y*32)))
            if char == "F":
                fatals.append(Actor("invisible", (x*32, y*32)))
            if char == "@":
                player.body.pos = (x*32, y*32)
            if char == "*":
                coins.append(Moeda("moeda_1",x*32,y*32))
            if char == "E":
                enemys.append(Enemy("enemy_left_1",x*32,y*32))
            if char == "W":
                wins.append(Actor("invisible",(x*32,y*32)))
            if char == "P":
                princess.append(Princess("princess_1",x*32,y*32))
                
    return blocks,coins,enemys,fatals,wins,princess

class Level:
    def __init__(self, map_file, body):
        self.blocks, self.coins, self.enemys, self.fatals, self.wins, self.princess = load_level(map_file, body)

def restart_level(levels, current_level):

    new_player = Player("player_idle_right_1", 400, 300)
    
    levels[current_level] = Level(f"lvl_{current_level+1}.txt", new_player)
    
    return new_player

def next_level(levels, current_level, player):
    (player.body.x,player.body.y) = (400, 300)
    
    levels[current_level] = Level(f"lvl_{current_level+1}.txt", player)
    
        