from pgzero.actor import Actor

from enemy import Enemy

class Utils:
    @staticmethod
    def place_meeting(x, y, blocks, player):
        for b in blocks:
            if isinstance(b,Actor):
                if (x + player.body.width/2 > b.x - b.width/2 and
                    x - player.body.width/2 < b.x + b.width/2 and
                    y + player.body.height/2 > b.y - b.height/2 and
                    y - player.body.height/2 < b.y + b.height/2):
                    return b
            elif player!=None:
                if (x + player.body.width/2 > b.body.x - b.body.width/2 and
                    x - player.body.width/2 < b.body.x + b.body.width/2 and
                    y + player.body.height/2 > b.body.y - b.body.height/2 and
                    y - player.body.height/2 < b.body.y + b.body.height/2):
                    return b
            
        return None
    
    @staticmethod
    def point_in_button(px, py, btn):
        return (px > btn.x - btn.width/2 and
                px < btn.x + btn.width/2 and
                py > btn.y - btn.height/2 and
                py < btn.y + btn.height/2)
    @staticmethod
    def move_and_collide(player, levels, current_level):
        blocks = levels[current_level].blocks

        player.body.x +=player.spd_h
        block = Utils.place_meeting(player.body.x,player.body.y,blocks,player)

        if block:
            if isinstance(player,Enemy):
                player.direction*=-1
            if player.spd_h>0:
                player.body.x = block.x - block.width/2 - player.body.width/2
            elif player.spd_h < 0:
                player.body.x = block.x + block.width/2 + player.body.width/2
            player.spd_h = 0
            
        player.body.y += player.spd_v
        block = Utils.place_meeting( player.body.x, player.body.y, blocks,player)

        if block:
            if player.spd_v>0:
                player.body.y = block.y - block.height/2 - player.body.height/2
                player.on_ground = True
            elif player.spd_v < 0:
                player.body.y = block.y + block.height/2 + player.body.height/2
            player.spd_v = 0
        else:        
            player.on_ground = False
        
    