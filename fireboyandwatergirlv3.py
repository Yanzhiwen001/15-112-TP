#----------------------------------------
#    Fireboy and watergirl starter demo v.1.0
#    4/12/2023
#    ID: zhiweny
#    figures are collected from: 
#    https://www.4399.com/   'watergirl & fireboy in forest 5'
#    https://github.com/Hakimos7777/Fireboy_and_watergirl_game
#----------------------------------------

import os
import pathlib
from cmu_graphics import *
from PIL import Image
import random, time
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
        right_filepath = f'TP/pics/{self.name}_right.gif'
        middle_filepath = f'TP/pics/{self.name}_middle.png'
        
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
        self.x = random.randrange(480,640)
        self.y1 = random.randrange(280,310)
        self.length = random.randrange(30,45)
        self.y2 = self.y1 - self.length
        self.dy = -random.randrange(2, 3)

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
        flatpath = f'TP/pics/{self.property}.gif'
        sloppath = f'TP/pics/{self.property}_slop.gif'
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
        self.diamonds = Image.open(f'TP/pics/{self.property}Diamond.png')
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
        doorpath = f'TP/pics/{self.property}door.gif'
        self.doorList = self.getGif(doorpath, False, 65, 135)
        #read in png
        self.door = Image.open(f'TP/pics/{self.property}door.png')
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
        self.button = Image.open(f'TP/pics/button.png')
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
        
        
#-------------------------------------------------------------------
def onAppStart(app):
    reset(app)
    
def reset(app):
    app.gameover = False
    app.gamewin = False
    app.stepsPerSecond = 30         #Adjust the onStep frequency
    app.bg = Image.open("TP/pics/bg.jpg")
    app.bg = app.bg.resize((app.width,app.height))
    app.bg = CMUImage(app.bg)
    app.fireboy = Character('fireboy','fire',200,600,5,5,8,5,10000)
    app.watergirl = Character('watergirl','water',250,600,5,5,9,9,12)
    app.airs = []                   #Make an empty orb list
    app.lastAirTime = time.time()   #Set an initial orb timer
    loadGameBoard(app)
    
def loadGameBoard(app):
    # "standard" Terrains 
    bottomwall = Terrain([(0,app.height-30), (0,app.height), 
                          (app.width,app.height), (app.width,app.height-30)])
    leftwall = Terrain([(0,0), (0,app.height), (30,app.height), (30,0)])
    rightwall = Terrain( [(app.width-30,0), (app.width-30,app.height), 
                          (app.width,app.height), (app.width,0)])
    topwall = Terrain( [(0,0), (0,30), (app.width,30), (app.width,0)])
    testslop1 = Terrain( [(30,570), (30,670), (130,670)])
    testslop2 = Terrain([(1120,570), (1020,670), (1120,670)])
    #add more terrins, hard code for three layers
    terrain1 = Terrain([(0,500), (0,525), (610,525), (660,465), 
                        (800,465), (825,440), (650,440), (600,500)])
    terrain2 = Terrain([(900,500), (1150,500), (1150,475), (925,475)])
    terrain3 = Terrain([(100,425),(125,425),(200,350),(675,350),(725,300),(1150,300),
                        (1150,275),(725,275),(675,325),(200,325)])
    terrain4 = Terrain([(0,175), (475,175), (475,150), (50,150), (0,100)])
    terrain5 = Terrain([(650,175), (1150,175), (1150,100), (1100,150), (650,150)])
    terrain6 = Terrain([(675,600), (925,600), (900,575), (700,575)])
    terrain7 = Terrain([(520,200),(520,225),(600,225),(600,200)])
    app.terrainList = [ bottomwall, leftwall, rightwall, topwall,
                        testslop1, testslop2,
                        terrain1,terrain2,terrain3,terrain4,terrain5,terrain6,terrain7]
    
    #fire and water pool
    fire1= SpecialTerrain([(300,app.height-30),(375,app.height-30)],'fire')
    fire2= SpecialTerrain([(200,500),(460,500)],'fire')
    #fire3= SpecialTerrain([(200,500),(460,500)],'fire')
    water1= SpecialTerrain([(450,app.height-30),(525,app.height-30)],'water')
    water2= SpecialTerrain([(325,325),(565,325)],'water')
    app.specialterrainList =[fire1,fire2,water1,water2]
    
    #diamonds
    firediamond1 = Diamond([(1000,425),(1000,465),(1040,465),(1040,425)],'fire')
    firediamond2 = Diamond([(400,275),(400,315),(440,315),(440,275)],'fire')
    firediamond3 = Diamond([(990,100),(990,140),(1030,140),(1030,100)],'fire')
    waterdiamond1 = Diamond([(780,530),(780,570),(820,570),(820,530)],'water')
    waterdiamond2 = Diamond([(220,450),(220,490),(260,490),(260,450)],'water')
    waterdiamond3 = Diamond([(120,100),(120,140),(160,140),(160,100)],'water')
    app.diamondList=[firediamond1,firediamond2,firediamond3,
                     waterdiamond1,waterdiamond2,waterdiamond3]
    
    #door
    waterdoor = Door([(300,85),(300,150),(350,150),(350,85)],'fire')
    firedoor = Door([(800,85),(800,150),(850,150),(850,85)],'water')
    app.doorList = [waterdoor,firedoor]
    
    #bottom
    botton1 = Button([(105,450),(105,535),(145,535),(145,450)],'fire') #500+35-85
    botton2 = Button([(600,275),(600,360),(640,360),(640,275)],'water') #325+35
    botton3 = Button([(900,225),(900,310),(940,310),(940,225)],'fire') #275
    botton4 = Button([(700,100),(700,185),(740,185),(740,100)],'water') #150+35-85
    app.buttonList = [botton1,botton2,botton3,botton4]
    
    
def onKeyHold(app, keys):
    if not app.gameover:
        #hold key to control horizontal move
        if 'd' in keys:
            app.fireboy.dx = 5
            app.fireboy.facedirection = 'right'
        elif 'a' in keys:
            app.fireboy.dx = -5
            app.fireboy.facedirection = 'left'

        elif 'right' in keys:
            app.watergirl.dx = 5
            app.watergirl.facedirection = 'right'
        elif 'left' in keys:
            app.watergirl.dx = -5
            app.watergirl.facedirection = 'left'

def onKeyRelease(app, keys):
    if not app.gameover:
        if 'd' in keys:
            app.fireboy.dx = 0
            app.fireboy.facedirection = 'middle'
        if 'a' in keys:
            app.fireboy.dx = 0
            app.fireboy.facedirection = 'middle'
        if 'right' in keys:
            app.watergirl.dx = 0
            app.watergirl.facedirection = 'middle'
        if 'left' in keys:
            app.watergirl.dx = 0
            app.watergirl.facedirection = 'middle'

def onKeyPress(app, key):
    #Jump kirb!
    if key == 'w':
        app.fireboy.jump() 
        
    if key == 'up':
        app.watergirl.jump()
        
    if key == 'r':
        reset(app)

def cross_product(a,b,p):
    """
    judge whether the point p is on the outside of line [a,b] of the geo 
    shape with cross_product
    The line of a shape goes in anti-clockwise direct, if point p lies outside 
    of geo shape, ap x ab < 0
    """
    return (b.x-a.x)*(p.y-a.y)-(p.x-a.x)*(b.y-a.y)


def collide(line:Line, character:Character): # should be modified later
    
    x_start, x_end = sorted([line.p1.x,line.p2.x])
    y_start, y_end = sorted([line.p1.y,line.p2.y])

    # check all anchor point with the line
    for pos_idx in range(1,10):
        cur_anchor_point = character.cur_position(pos_idx)
        
        # if the points is out of the valid region, additional padding region (+-1) is added
        if (x_start-1 >= cur_anchor_point.x or cur_anchor_point.x >= x_end+1)\
            and (y_start-1 >= cur_anchor_point.y or cur_anchor_point.y >= y_end+1):
            continue
        
        next_anchor_point = character.next_position(pos_idx) # in the next frame, temporal "next", not spacial "next"
        cur_status = cross_product(line.p1,line.p2,cur_anchor_point)
        next_status = cross_product(line.p1,line.p2,next_anchor_point)
        
        # it will collide in the next frame, avoid it
        
        if cur_status>=0 and next_status<0: 
            if line.direct=="vertical":
                if y_start <= character.y and character.y <= y_end: #within range
                    if pos_idx in [4,6]:
                        character.dx = 0
                        character.set_position(line.x+(5-pos_idx), None, pos_idx)
                        return 'wall'
                    
            elif line.direct=="horizon":
                if x_start <= character.x and character.x <= x_end: #within range
                    # middle bottom point collides with the floor
                    if pos_idx in [8]:
                        character.dy = 0
                        character.set_position(None, line.y, pos_idx)
                        character.status = "on floor"
                        return 'hit floor'

                    # middle top point collides with the ceil
                    elif pos_idx in [2]: 
                        character.dy = 0
                        character.set_position(None, line.y, pos_idx)
                        print('hit ceil')
                        return 'hit ceil'
        
            elif "slop" in line.direct:
                if (pos_idx in [1,2] and line.direct=="leftslop") or (pos_idx in [2,3] and line.direct=="rightslop"):
                    character.dy = 0
                elif (pos_idx in [8,9] and line.direct=="leftslop") or (pos_idx in [7,8] and line.direct=="rightslop"):
                    character.set_position(cur_anchor_point.x, cur_anchor_point.x*line.a+line.b, pos_idx)
                    character.dy = character.dx*line.a
                    character.status = "on slop"
                    return "hit slop"
                    
        elif cur_status == 0: # already on the line
            if line.direct == "horizon":
                if x_start <= character.x and character.x <= x_end: #within range
                    if pos_idx in [7,8,9]:
                        if character.status!="on floor":
                            character.set_position(None, line.y, pos_idx)
                            character.status = "on floor"
                        return 'on floor'
            
            if "slop" in line.direct:
                if x_start <= cur_anchor_point.x and cur_anchor_point.x <= x_end:
                    if (pos_idx in [8,9] and line.direct=="leftslop") or (pos_idx in [7,8] and line.direct=="rightslop"):
                        if character.status!="on slop":
                            character.status = "on slop"
                        character.dy = character.dx*line.a
                    return 'on slop'

def onLine(app, character:Character): 
    status = set()
    #check if collide with static terrin
    for terrain in app.terrainList:
        #cheack each line if collide
        for line in terrain.line_list:
            collide_status = collide(line,character)
            if collide_status != None:
                status.add(collide_status)
    #check if collide with diamonds
    for diamond in app.diamondList:
        for diamondline in diamond.line_list:
            if not diamond.isfound:
                if diamond.property == character.property:
                    if collide(diamondline,character) != None:
                        diamond.isfound = True
                        character.diamond += 1
    #check if collide with exit door
    for door in app.doorList:
        if door.property == character.property:
            for doorline in door.line_list:
                #if character havent reach the door, check collision
                if not door.isfound:
                    if collide(doorline,character) != None:
                        door.isfound = True
                #if character leaves or far away, door close regradless of door status
                if (door.x-45)>=character.x or (door.x+45)<=character.x:
                    door.isfound = False
    #check if collide with button
    for bu in app.buttonList:
        if bu.property == character.property:
            for buline in bu.line_list:
                #if character havent reach the door, check collision
                if not bu.isfound:
                    if collide(buline,character) != None:
                        bu.isfound = True
                #if character leaves or far away, door close regradless of door status
                if (bu.x-42)>=character.x or (bu.x+42)<=character.x:
                    bu.isfound = False
                    
    if len(status)==0:
        character.status = "in air"
        return "in air"
    return status

def onPool(app, character):
    for sp_terrain in app.specialterrainList:
        # if the terrain property does no match char property
        if sp_terrain.property != character.property:
            #cheack each line if collide
            for line in sp_terrain.line_list:
                collide_status = collide(line, character)
                if collide_status != None:
                    return 'died'
    return 'safe'
    
def updateStatus(app, character:Character):
    #if in up air! before checking each line collision
    if app.buttonList[2].isfound or app.buttonList[3].isfound:
        if 475<=character.x and character.x<=650:
            if 0<= character.y and character.y<=300:
                character.dy = -2

    status = onLine(app, character) #return a set of current status
    #print(f'current status is {status}, {character.cur_position(9)}')
    #check if the character has come across waterpool or firepool
    if 'on floor' in status:
        if onPool(app, character) == 'died':
            character.die = True


def onStep(app):
    if not app.gameover:
        #Update fireboy status 
        #Update all terrain, special terrain, diamond, door, button status
        updateStatus(app, app.fireboy)
        updateStatus(app, app.watergirl)
        
        #update fire and water pool
        if app.buttonList[0].isfound:
            app.specialterrainList[1].property = 'water'
            app.specialterrainList[1].ischanged = True
        if app.buttonList[1].isfound:
            app.specialterrainList[3].property = 'fire'
            app.specialterrainList[3].ischanged = True
        for sp_terrain in app.specialterrainList: 
            sp_terrain.doStep()
                
        #update door if its been found
        doorcount = 0
        for door in app.doorList:
            if door.isfound:
                doorcount += 1
                door.doStep()
        if doorcount == len(app.doorList):
            app.gamewin = True
                
        #update air bubbles
        for air in app.airs:
            air.doStep()

        #Add another orb each second
        if (time.time() - app.lastAirTime > 1):
            app.airs.append(Air(app))
            app.lastAirTime = time.time()
            if len(app.airs) >= 20:
                app.airs = app.airs[-10:]
                
        #Update the fireboy
        app.fireboy.doStep()
        app.watergirl.doStep()
        
        if app.fireboy.die or app.watergirl.die:
            app.gameover = True
            
    
def redrawAll(app):
    #Background
    drawImage(app.bg, 0, 0)
    #draw botton
    for bu in app.buttonList:
        bu.draw()
    #draw Terrain
    for terrain in app.terrainList:
        drawPolygon(*terrain.drawing_point_output, fill='black',opacity=100)
    #draw special terrain
    for sp_terrain in app.specialterrainList:
        sp_terrain.draw()
    #draw diamonds:
    for dia in app.diamondList:
        dia.draw()
    #draw doors
    for door in app.doorList:
        door.draw()
    #draw up level air
    if app.buttonList[2].isfound or app.buttonList[3].isfound:
        for air in app.airs:
            air.draw()
    #draw character 
    app.fireboy.draw()
    app.watergirl.draw()
    
    if app.gameover:
        drawRect(575,350,600,300,align='center',fill='salmon',border='yellow',borderWidth=2)
        drawLabel("You died! Please press r to restart", 575,350, size=30, font='sacramento') #font can not be shown correctly
    if app.gamewin:
        drawRect(575,350,600,300,align='center',fill='salmon',border='yellow',borderWidth=2)
        drawLabel(f"Good job, you win!!", 
                  575,275, size=35, font='sacramento')
        drawLabel(f"watergirl score is {app.watergirl.diamond}/3", 
                  575,325, size=30, font='sacramento')
        drawLabel(f"fireboy score is {app.fireboy.diamond}/3", 
                  575,375, size=30, font='sacramento')
        
def main():
    runApp(width=1150, height=700)

main()
