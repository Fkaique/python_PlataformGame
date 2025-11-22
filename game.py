# pgzero_config

WIDTH = 800
HEIGHT = 600
SPEED = 3
RIGHT_BORDER = 600
LEFT_BORDER = 200

camera_x=0
level_width = 2000

# World
grav = 0.8

# Player
player = Actor("player", (400, 300))
hspd = 0
vspd = 0
on_ground = False
jump_force=-14

def place_meeting(x,y,blocks):
    for b in blocks:
        if (x + player.width/2 > b.x - b.width/2 and
            x - player.width/2 < b.x + b.width/2 and
            y + player.height/2 > b.y - b.height/2 and
            y - player.height/2 < b.y + b.height/2):
            return b
    return None

def move_and_collide():
    global hspd, vspd, on_ground

    blocks = levels[current_level].blocks

    player.x +=hspd
    block = place_meeting(player.x,player.y,blocks)

    if block:
        if hspd>0:
            player.x = block.x - block.width/2 - player.width/2
        elif hspd < 0:  # indo pra esquerda
            player.x = block.x + block.width/2 + player.width/2
        hspd = 0
    player.y += vspd
    block = place_meeting(player.x,player.y,blocks)

    if block:
        if vspd>0:
            player.y = block.y - block.height/2 - player.height/2
            on_ground = True
        elif vspd < 0:  # indo pra esquerda
            player.y = block.y + block.height/2 + player.height/2
        vspd = 0
    else:
        on_ground = False

def draw_actor(actor):
    screen.blit(actor.image,
        (actor.x - camera_x - actor.width/2,
         actor.y - actor.height/2)            
    )

def load_level(path):
    blocks = []
    with open(path) as f:
        lines = f.readlines()

    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if char == "#":
                blocks.append(Actor("block", (x*16, y*16)))
            if char == "@":
                player.pos = (x*16, y*16)

    return blocks

class Level:
    def __init__(self, map_file):
        self.blocks = load_level(map_file)
        self.start_pos = player.pos

# Levels

levels = [
    Level("lvl_1.txt"),
    Level("lvl_2.txt"),
    Level("lvl_3.txt"),
]
current_level = 0

def draw():
    screen.clear()
    screen.blit("bg", (-camera_x, 0))
    draw_actor(player)

    for b in levels[current_level].blocks:
        screen.blit("block", (b.x - camera_x - 8, b.y - 8))

def update():
    global camera_x, hspd, vspd, on_ground
    
    hspd = (int(keyboard.right)-int(keyboard.left))*SPEED

    if keyboard.up and on_ground:
        vspd = jump_force
        on_ground = False
    
    if not on_ground:
        vspd += grav
        if vspd > 10:
            vspd = 10

    move_and_collide()

    blocks = levels[current_level].blocks
    # suavização (quanto menor o número, mais suave)
    player_screen_x = player.x - camera_x
    
    if player_screen_x > RIGHT_BORDER:
        camera_x += player_screen_x - RIGHT_BORDER
    
    if player_screen_x < LEFT_BORDER:
        camera_x -= LEFT_BORDER - player_screen_x
    
    camera_x = max(0, min(camera_x, level_width - WIDTH))
