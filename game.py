from level import *
from player import Player
from utils import Utils

WIDTH = 800
HEIGHT = 600
SPEED = 3
RIGHT_BORDER = 600
LEFT_BORDER = 200

# Audio

on_music = True
on_sound = True
icon_music = images.load("icon_music_on")
icon_sound = images.load("icon_sound_on")
music.play("music")
rect_music = Rect((WIDTH-icon_music.get_width()-50,50),(32,32))
rect_sound = Rect((WIDTH-icon_sound.get_width()-100,50),(32,32))

game_state = "menu"

camera_x=0
level_width = 32*70

# World
grav = 0.8

# Player
player = Player("player_idle_right_1", 400, 300)
current_player=0

# Levels
levels = [
    Level("lvl_1.txt",player),
    Level("lvl_2.txt",player),
    Level("lvl_3.txt",player),
]

current_level = 0

frame = 0

# Controller
start = Rect((300,250),(200,80))
end = Rect((320,350),(160,60))
restart = Rect((300,250),(200,80))

def draw_actor(actor):
    screen.blit(actor.image,
        (actor.x - camera_x - actor.width/2,
         actor.y - actor.height/2)            
    )

def on_mouse_up(pos):
    global game_state, on_music, on_sound, current_level, player
    if restart.collidepoint(pos) and game_state=="theend":
        current_level=0
        game_state="menu"
        player = restart_level(levels,current_level)
    if start.collidepoint(pos):
        game_state="start"
    if end.collidepoint(pos) and (game_state=="menu" or game_state=="theend"):
        exit()
    if rect_music.collidepoint(pos) and game_state=="menu":
        if on_music:
            music.stop()
        elif game_state=="menu":
            music.play("music")
        on_music = False if on_music else True
    if rect_sound.collidepoint(pos) and game_state=="menu":
        on_sound = False if on_sound else True
def on_key_down(key):
    global player, game_state, on_music, on_sound
    if key == keys.R:
        player = restart_level(levels,current_level)
        game_state="menu"
    if key == keys.P:
        game_state = "menu"
def draw():
    global game_state, icon_music, icon_sound, on_music
    screen.clear()
    if game_state=="menu":
        screen.fill("#B8A13C")
        screen.draw.filled_rect(start, "white")
        screen.draw.rect(start, "black")
        screen.draw.filled_rect(end, "white")
        screen.draw.rect(end, "black")
        img = images.load("player")
        screen.blit("player", ((WIDTH - img.get_width())//2, 50))
        screen.draw.text("Ghost Chase",center=(400,170), color="#2b2e02",fontsize=100)
        screen.draw.text("Iniciar",center=(400,290), color="black", fontsize=35)
        screen.draw.text("Sair",center=(400,380), color="red", fontsize=30)
        icon_music = images.load("icon_music_on") if on_music else images.load("icon_music_off")
        screen.blit(icon_music, (WIDTH-icon_music.get_width()-50,45))
        icon_sound = images.load("icon_sound_on") if on_sound else images.load("icon_sound_off")
        screen.blit(icon_sound, (WIDTH-icon_sound.get_width()-100,45))
    elif game_state=="theend":
        if on_music:
            on_music=False
            music.stop()
        screen.fill("#B8A13C")
        img = images.load("player")
        screen.blit(img, ((WIDTH - img.get_width())//2-25, 100))
        img = images.load("princess_win")
        screen.blit(img, ((WIDTH - img.get_width())//2+25, 100))
        screen.draw.filled_rect(restart, "white")
        screen.draw.rect(restart, "black")
        screen.draw.text("Reiniciar",center=(400,290), color="black")
        
        screen.draw.filled_rect(end, "white")
        screen.draw.rect(end, "black")
        screen.draw.text("Sair",center=(400,380), color="red", fontsize=30)
    elif game_state=="start":
        screen.fill("#63BDD6")
        draw_actor(player.body)
        screen.draw.text(f"${player.score}", (50,50),fontsize=30, color="yellow")
        screen.draw.text(f"P - Pause R - Restart", center=(WIDTH//2,60), color="black")
        for b in levels[current_level].blocks:
            screen.blit("block", (b.x - camera_x - 16, b.y - 16))
        for f in levels[current_level].fatals:
            screen.blit("invisible", (f.x - camera_x - 16, f.y - 16))
        for c in levels[current_level].coins:
            screen.blit(c.body.image, (c.body.x - camera_x - 16, c.body.y - 16))
        for e in levels[current_level].enemys:
            screen.blit(e.body.image, (e.body.x - camera_x - 16, e.body.y - 16))
        if current_level>=2:
            for p in levels[current_level].princess:
                screen.blit(p.body.image, (p.body.x - camera_x - 16, p.body.y - 16))
            
def update():
    global camera_x, on_ground, frame, player, game_state, current_level
    wins = levels[current_level].wins
    win = Utils.place_meeting(player.body.x,player.body.y,wins, player)
    if current_level>=2:
        ps = levels[current_level].princess
        princess = Utils.place_meeting(player.body.x,player.body.y,ps, player)
        for p in ps:
            p.animate(2)
        if princess:
            game_state="theend"
    if win:
        if current_level< len(levels)-1:
            current_level+=1
            next_level(levels, current_level, player)
    if keyboard.escape:
        exit()
    if game_state=="menu":
        pass
    elif game_state=="theend":
        pass
    elif game_state=="start":
        coins = levels[current_level].coins
        for c in coins:
            if abs(player.body.x-c.body.x)<800:
                c.animate(8)
        coin = Utils.place_meeting(player.body.x,player.body.y,coins, player)
        if coin:
            if on_sound:
                sounds.coin.play()
            coins.remove(coin)
            player.score+=1
            
        enemys = levels[current_level].enemys
        enemy = Utils.place_meeting(player.body.x,player.body.y,enemys, player)
        if enemy:
            if player.body.y<enemy.body.y-10:
                if on_sound:
                    sounds.kick.play()
                enemys.remove(enemy)
            else:
                player = restart_level(levels,current_level)
        player.spd_h = (int(keyboard.right)-int(keyboard.left))*player.spd
        
        if player.spd_h!=0:
            if frame%20==0:
                if on_sound:
                    sounds.step.play()
            if player.spd_h>0:
                player.animate("run_right",7)
                player.direction=0
            else:
                player.animate("run_left",7)
                player.direction=1
        else:
            if player.direction==0:
                player.animate("idle_right",5)
            else:
                player.animate("idle_left",5)
        Utils.move_and_collide(player,levels,current_level)
        if keyboard.up and player.on_ground:
            player.spd_v = player.jump_force
            player.on_ground = False
        
        if not player.on_ground:
            player.spd_v += grav
            if player.spd_v > 10:
                player.spd_v = 10
        blocks = levels[current_level].blocks
        for e in enemys:
            e.spd_h=e.direction*e.spd
            if e.direction==-1:
                e.animate("left",5)
            else:
                e.animate("right",5)
            Utils.move_and_collide(e,levels,current_level)
            
            block = Utils.place_meeting(e.body.x,e.body.y,blocks,e)
                       
            if block:
                e.direction *= -1
                
        fatals = levels[current_level].fatals
        fatal = Utils.place_meeting(player.body.x,player.body.y,fatals,player)
        if fatal:
            player = restart_level(levels,current_level)
        player_screen_x = player.body.x - camera_x 
        if player_screen_x > RIGHT_BORDER:
            camera_x += player_screen_x - RIGHT_BORDER
        
        if player_screen_x < LEFT_BORDER:
            camera_x -= LEFT_BORDER - player_screen_x
        
        camera_x = max(0, min(camera_x, level_width - WIDTH))
        frame=(frame+1)%60
