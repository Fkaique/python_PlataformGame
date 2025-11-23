from pgzero.builtins import Actor

class Enemy:
    def __init__(self, image, x, y):
        self.body = Actor(image, (x, y))
        self.spd_h=0
        self.spd_v=0
        self.spd=2
        self.on_ground=False 
        self.direction=-1
        self.sprites = {
            "right" : ["enemy_right_1","enemy_right_2"],
            "left" : ["enemy_left_1","enemy_left_2"],
        }
        self.frame_index=0
        self.frame_counter=0
        
    def animate(self, state, fps):
        frames = self.sprites[state]
        update_per_frame = int(60/fps)
        self.frame_counter+=1
        if self.frame_counter>=update_per_frame:
            self.frame_counter=0
            frames = self.sprites[state]
            self.frame_index = (self.frame_index+1)%len(self.sprites[state])
            self.body.image = frames[self.frame_index]
            return True
        return False
        