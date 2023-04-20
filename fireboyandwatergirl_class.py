from random import randrange, getrandbits, randint 
from cmu_graphics import *
from PIL import Image
import math


class Character:
    def __init__(self, name, property, initx, inity, widthresize, heightresize, midwidth, midheight, adjust):
        #set initial property, position, velocity
        self.name = name
        self.property = property
        self.facedirection = 'middle'
        self.midwidth = midwidth
        self.midheight = midheight
        self.heightresize = heightresize
        self.widthresize = widthresize
        self.ajust = adjust
        self.x = initx
        self.y = inity
        self.dx = 0
        self.dy = 0
        self.ddy = 0
        self._status = "in air"
        self.die = False
        self.diamond = 0
        
        #condition on current direction
        right_filepath = f'pics/{self.name}_right.gif'
        middle_filepath = f'pics/{self.name}_middle.png'
        
        ### Adapted from mdtaylor: KirbleBird starter demo v.1.1 ###
        #Load the left gif
        self.leftspriteList = []
        self.rightspriteList = []
        myGif = Image.open(right_filepath)
        for frame in range(myGif.n_frames):  #For every frame index...
            #Seek to the frame, convert it, add it to our sprite list
            myGif.seek(frame)
            fr = myGif.resize((myGif.size[0]//self.widthresize, myGif.size[1]//self.heightresize))
            fr_flip = fr.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            fr = CMUImage(fr)
            fr_flip = CMUImage(fr_flip)
            self.leftspriteList.append(fr_flip)
            self.rightspriteList.append(fr)
        ##Fix for broken transparency on frame 0
        self.leftspriteList.pop(0)
        self.rightspriteList.pop(0)

        #load the middle png
        self.middle = Image.open(middle_filepath)
        self.middle = self.middle.resize((myGif.size[0]//self.midwidth,myGif.size[1]//self.midheight))
        self.middle = CMUImage(self.middle)
        
        #Set sprite counters
        self.stepCounter = 0
        self.spriteCounter = 0

        #Set size
        self.width = myGif.size[0]//self.widthresize 
        self.height  = myGif.size[1]//self.heightresize - (myGif.size[1]//self.ajust)

    @property
    def status(self):
        """ charecter's move status, items selected from ENUM
        in air: ddy=0.5
        on floor: ddy=0
        on slop: ddy=0
        a setter and getter is used to automatically change the ddy
        """
        return self._status
    
    @status.setter
    def status(self,status):
        if status == "in air":
            self.ddy = 0.5
        elif status == "on floor" or status == "on slop":
            self.ddy = 0
        else:
            raise Exception("value error")
        self._status = status

    def __repr__(self) -> str:
        """define the string shown in debug"""
        return f"{self.name} {self.facedirection} {self.status}"

    def cur_position(self,idx=5):
        """ get the anchor point position with point index, the offest can be 
        manually change to adapt the character shape
        1--2--3
        |  |  |
        4--5--6
        |  |  |
        7--8--9
        """
        x_offset = ((idx-1)%3-1)*self.width/4
        y_offset = ((idx-1)//3-1)*self.height/2
        return Point(self.x+x_offset, self.y+y_offset)

    def next_position(self, idx=5):
        #anchor point position in next frame
        x_offset = ((idx-1)%3-1)*self.width/4
        y_offset = ((idx-1)//3-1)*self.height/2
        return Point(self.x+x_offset+self.dx,self.y+y_offset+self.dy)

    def set_position(self,x=None,y=None,idx=5):
        """set the position of character so that the indexed anchor point moves to the given coordinate"""
        if x is not None:
            x_offset = ((idx-1)%3-1)*self.width/4
            self.x = x-x_offset
        if y is not None:
            y_offset = ((idx-1)//3-1)*self.height/2
            self.y = y-y_offset

    def draw(self):
        #Draw middle sprite
        if self.facedirection == 'middle':
            drawImage(self.middle, 
                    self.x, self.y, align = 'center')
        #Draw left sprite
        if self.facedirection == 'left':
            drawImage(self.leftspriteList[self.spriteCounter], 
                    self.x, self.y, align = 'center')
        #Draw right sprite
        if self.facedirection == 'right':
            drawImage(self.rightspriteList[self.spriteCounter], 
                    self.x, self.y, align = 'center')
        
        # DEBUG: showing the anchor points
        for pos_idx in range(1,10):
            anchor_point = self.cur_position(pos_idx)
            drawCircle(anchor_point.x,anchor_point.y, 2)
        
            
    ### Adapted from mdtaylor: KirbleBird starter demo v.1.1 ###  
    def doStep(self):
        if self.stepCounter >= 1000:
            self.stepCounter = 0
        self.x += self.dx
        self.y += self.dy
        self.dy += self.ddy
        self.stepCounter += 1
        if self.stepCounter >= 10: #Update the sprite every 10th call
            self.spriteCounter = (self.spriteCounter + 1) % len(self.leftspriteList)
            self.stepCounter = 0

    def jump(self):
        if self.status != "in air":
            self.dy = -10
            self.status = "in air"
class Air:
    def __init__(self, app):
        self.x = randrange(480,640)
        self.y1 = randrange(280,310)
        self.length = randrange(30,45)
        self.y2 = self.y1 - self.length
        self.dy = -randrange(2, 3)

    def doStep(self):
        self.y1 += self.dy
        self.y2 += self.dy

    def draw(self):
        drawLine(self.x, self.y2, self.x, self.y1, fill = 'white', opacity = 75, arrowStart=True)
        
        
class Point:
    def __init__(self,x:int,y:int):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

class Line:
    def __init__(self,p1:Point,p2:Point):
        self.p1 = p1
        self.p2 = p2

        self.direct = "undirect!"
        if 0==p1.x-p2.x:
            self.direct = "vertical"
            self.x = self.p1.x
        elif 0==p1.y-p2.y:
            self.direct = "horizon"
            self.y = self.p1.y
        else:
            # for the slop, use y=ax+b
            self.a = (p1.y-p2.y)/(p1.x-p2.x)
            self.b = p1.y-p1.x*self.a
            if (p1.x-p2.x)*(p1.y-p2.y):
                self.direct = "leftslop"
            else:
                self.direct = "rightslop"

    def __repr__(self) -> str:
        return f"{self.p1}->{self.p2}"


class Terrain:
    def __init__(self, point_list):
        self.point_list  = [Point(point[0], point[1]) for point in point_list]

        self.line_list = []
        self.drawing_point_output = []

        # add the lines with give points
        for point_idx in range(len(self.point_list)):
            # connect the last point to the first to clost the geo shape
            cur_point = self.point_list[point_idx]
            next_point = self.point_list[point_idx+1 if (point_idx<len(self.point_list)-1) else 0]
            
            self.line_list.append(Line(cur_point,next_point))

            self.drawing_point_output.append(cur_point.x)
            self.drawing_point_output.append(cur_point.y)
    
    def __repr__(self) -> str:
        return "".join([f"{p}->" for p in self.point_list])[:-2]
    
class SpecialTerrain(Terrain):
    def __init__(self, point_list, property):
        super().__init__(point_list)
        self.property = property
        self.stepCounter = 0
        self.spriteCounter = 0
        self.loadImage()
        self.ischanged = False
        
    def loadImage(self):
        flatpath = f'pics/{self.property}.gif'
        sloppath = f'pics/{self.property}_slop.gif'
        self.flatList = self.getGif(flatpath, False, 20, 20)
        self.leftslopList = self.getGif(sloppath, False, 20, 20)
        self.rightslopList = self.getGif(sloppath, True, 20, 20)
        
    
    def getGif(self, path, flip, resizex, resizey):
            animeList = []
            gif = Image.open(path)
            for frame in range(gif.n_frames):  #For every frame index...
                #Seek to the frame, convert it, add it to our sprite list
                gif.seek(frame)
                fr = gif.resize((resizex, resizey))
                if flip:
                    fr = fr.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                fr = CMUImage(fr)
                animeList.append(fr)
            ##Fix for broken transparency on frame 0
            animeList.pop(0)
            return animeList
        

    def draw(self):
        if self.ischanged:
            self.loadImage()
            self.ischanged = False
        #draw pool with two slops on the side
        #draw left slop
        drawImage(self.leftslopList[self.spriteCounter], 
                    self.point_list[0].x, self.point_list[0].y+8, align = 'center')
        #draw right slop
        drawImage(self.rightslopList[self.spriteCounter], 
                    self.point_list[1].x,self.point_list[0].y+8, align = 'center')
        #draw flat
        for pos in range(self.point_list[0].x+20,self.point_list[1].x,20):
            drawImage(self.flatList[self.spriteCounter], 
                    pos,self.point_list[0].y+8, align = 'center')
    
    def doStep(self):
        if self.stepCounter >= 1000:
            self.stepCounter = 0
        self.stepCounter += 1
        if self.stepCounter >= 10: #Update the animate every 10th call
            self.spriteCounter = (self.spriteCounter + 1) % len(self.flatList)
            self.stepCounter = 0

class Diamond(Terrain):
    def __init__(self, point_list, property):
        super().__init__(point_list)
        self.property = property
        self.isfound = False
        self.x = (self.point_list[0].x + self.point_list[2].x)//2
        self.y = (self.point_list[0].y + self.point_list[1].y)//2
        self.diamonds = Image.open(f'pics/{self.property}Diamond.png')
        self.diamonds = self.diamonds.resize((65, 65))
        self.diamonds = CMUImage(self.diamonds)
        
    def draw(self):
        if not self.isfound:
            drawImage(self.diamonds, 
                    self.x, self.y, align = 'center')

class Door(SpecialTerrain):
    def __init__(self, point_list, property):
        super().__init__(point_list,property)
        self.x = (self.point_list[0].x + self.point_list[2].x)//2
        self.y = (self.point_list[0].y + self.point_list[1].y)//2
        self.isfound = False
        #read in git
        doorpath = f'pics/{self.property}door.gif'
        self.doorList = self.getGif(doorpath, False, 65, 135)
        #read in png
        self.door = Image.open(f'pics/{self.property}door.png')
        self.door = self.door.resize((65, 75))
        self.door = CMUImage(self.door)
               
    def draw(self):
        if not self.isfound:
            drawImage(self.door, 
                        self.x, self.y, align = 'center')
        elif self.isfound:
            drawImage(self.doorList[self.spriteCounter], 
                        self.x, self.y-25, align = 'center')
            
    def doStep(self):
        super().doStep()

class Button(SpecialTerrain):
    def __init__(self, point_list, property):
        super().__init__(point_list,property)
        self.x = (self.point_list[0].x + self.point_list[2].x)//2
        self.y = (self.point_list[0].y + self.point_list[1].y)//2
        self.isfound = False
        self.property = property
        #read in png
        self.button = Image.open(f'pics/button.png')
        self.button = self.button.resize((40, 15))
        self.button = CMUImage(self.button)

    
    def draw(self):
        if self.isfound == False: #if not found, draw png
            if self.property == 'fire':
                drawRect(self.x-8.5, self.y-13, 15, 10, fill='crimson')
                drawImage(self.button, 
                        self.x, self.y, align = 'center')
            else:
                drawRect(self.x-8.5, self.y-13, 15, 10, fill='deepSkyBlue')
                drawImage(self.button, 
                        self.x, self.y, align = 'center')
                
        elif self.isfound == True: #if not found, draw png down place
            drawImage(self.button, 
                        self.x, self.y+10, align = 'center')
 
 #---Gamestart Button class-------------------------------------
class SelectionButton:
    def __init__(self, x, y, level):
        # You'll probably want some more / different parameters
        self.x = x
        self.y = y
        self.width = 160
        self.height = 80
        self.level = level 

    def draw(self):
        # This button looks like garbage
        drawRect(self.x, self.y, self.width, self.height, fill = 'khaki', align = 'center', border='teal',borderWidth=4)
        drawLabel(self.level, self.x, self.y, size = 30, fill = 'darkOliveGreen')

    def checkForPress(self, app, mX, mY):
        # Might want to change this if you want a non-circular button
        if self.withRect(mX, mY):
            if self.level == 'hard':
                #loadGameBoardhard(app) 
                app.level = 'hard'
            elif self.level == 'easy':
                #loadGameBoardeasy(app)
                app.level = 'easy'
                
    def withRect(self, mX, mY):
        return ((self.x-self.width//2)<=mX and mX<=(self.x+self.width//2) and
                (self.y-self.height//2)<=mY and mY<=(self.y+self.height//2))
        