from pgzero.builtins import Actor

class Moeda:
    def __init__(self, image, x, y):
        self.body = Actor(image, (x, y))
        self.frames = ["moeda_1","moeda_2","moeda_3","moeda_4","moeda_5","moeda_6"]
        self.frame_index=0
        self.frame_counter=0
        
    def animate(self,fps):
        update_per_frame = int(60/fps)
        self.frame_counter+=1
        if self.frame_counter>=update_per_frame:
            self.frame_counter=0
            frames = self.frames
            self.frame_index = (self.frame_index+1)%len(self.frames)
            self.body.image = frames[self.frame_index]
