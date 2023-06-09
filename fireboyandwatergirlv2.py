#----------------------------------------
#    Fireboy and watergirl starter demo v.2.0
#    4/16/2023
#    ID: zhiweny
#    figures are collected from https://www.4399.com/ 'watergirl & fireboy in forest 5'
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
            next_point = self.point_list[point_idx+1 if point_idx<len(self.point_list)-1 else 0]
            
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
        #draw pool with two slops on the side
        #draw left slop
        drawImage(self.leftslopList[self.spriteCounter], 
                    self.point_list[0].x, self.point_list[0].y+8, align = 'center')
        #draw right slop
        drawImage(self.rightslopList[self.spriteCounter], 
                    self.point_list[1].x,self.point_list[0].y+8, align = 'center')
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
            
#-------------------------------------------------------------------
def onAppStart(app):
    reset(app)
    
def reset(app):
    app.gameover = False
    app.stepsPerSecond = 30         #Adjust the onStep frequency
    app.bg = Image.open("TP/pics/bg.jpg")
    app.bg = app.bg.resize((app.width,app.height))
    app.bg = CMUImage(app.bg)
    app.fireboy = Character('fireboy','fire',200,400,5,5,8,5,10000)
    app.watergirl = Character('watergirl','water',250,600,5,5,9,9,12)
    loadTerrainPieces(app)
    
def loadTerrainPieces(app):
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

    app.terrainList = [ bottomwall, leftwall, rightwall, topwall,
                        testslop1, testslop2,
                        terrain1,terrain2,terrain3,terrain4,terrain5,terrain6]
    #fire and water pool
    fire1= SpecialTerrain([(300,app.height-30),(375,app.height-30)],'fire')
    fire2= SpecialTerrain([(200,500),(460,500)],'fire')
    fire3= SpecialTerrain([(200,500),(460,500)],'fire')
    water1= SpecialTerrain([(450,app.height-30),(525,app.height-30)],'water')
    water2= SpecialTerrain([(325,325),(565,325)],'water')
    app.specialterrainList =[fire1,fire2,fire3,water1,water2]
    
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
                if y_start <= character.y and character.y <= y_end:
                    if pos_idx in [4,6]:
                        character.dx = 0
                        character.set_position(line.x+(5-pos_idx), None, pos_idx)
                        return 'wall'
                    
            elif line.direct=="horizon":
                if x_start <= character.x and character.x <= x_end:
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
                if x_start <= character.x and character.x <= x_end:
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
    for terrain in app.terrainList:
        #cheack each line if collide
        for line in terrain.line_list:
            collide_status = collide(line,character)
            if collide_status != None:
                status.add(collide_status)
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
    status = onLine(app, character) #return a set of current status
    #print(f'current status is {status}, {character.cur_position(9)}')
    if 'on floor' in status:
        #check if the character has come across waterpool or firepool
        if onPool(app, character) == 'died':
            character.die = True


def onStep(app):
    if not app.gameover:
        #Update fireboy status
        updateStatus(app, app.fireboy)
        updateStatus(app, app.watergirl)
        
        #update fire and  water pool
        for sp_terrain in app.specialterrainList: 
            sp_terrain.doStep()
        
        #Update the fireboy
        app.fireboy.doStep()
        app.watergirl.doStep()
        
        if app.fireboy.die or app.watergirl.die:
            app.gameover = True
    
def redrawAll(app):
    #Background
    drawImage(app.bg, 0, 0)
    #draw Terrain
    for terrain in app.terrainList:
        drawPolygon(*terrain.drawing_point_output, fill='black',opacity=100)
    #draw special terrain
    for sp_terrain in app.specialterrainList:
        sp_terrain.draw()
    #draw character 
    app.fireboy.draw()
    app.watergirl.draw()
    
    if app.gameover:
        drawRect(575,350,600,300,align='center',fill='salmon',border='yellow',borderWidth=2)
        drawLabel("You died! Please press r to restart", 575,350, size=30, font='sacramento') #font can not be shown correctly
    
def main():
    runApp(width=1150, height=700)

main()
