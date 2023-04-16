#----------------------------------------
#    Fireboy and watergirl starter demo v.1.0
#    4/12/2023
#    ID: zhiweny
#----------------------------------------

import os
import pathlib
from cmu_graphics import *
from PIL import Image
import random, time

class Character:
    def __init__(self, name, nature, initx, inity):
        #set property
        self.name = name
        self.nature = nature
        self.facedirection = 'middle'
        
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
            fr = myGif.resize((myGif.size[0]//5, myGif.size[1]//5))
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
        self.middle = self.middle.resize((myGif.size[1]//8,myGif.size[1]//5))
        self.middle = CMUImage(self.middle)
        
        #Set sprite counters
        self.stepCounter = 0
        self.spriteCounter = 0

        #Set initial position, velocity, size
        self.x = initx
        self.y = inity
        self.dx = 0
        self.dy = 0
        self.ddy = 0.5
        self.isjumping = False
        self.onground = False
        self.onslop = 'no'
        self.width = myGif.size[0]//5
        self.height  = myGif.size[1]//5
        self.rotation = 0
        
    ### Adapted from mdtaylor: KirbleBird starter demo v.1.1 ###  
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
        
            
    ### Adapted from mdtaylor: KirbleBird starter demo v.1.1 ###  
    def doStep(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += self.ddy
        self.stepCounter += 1
        if self.stepCounter >= 10: #Update the sprite every 10th call
            self.spriteCounter = (self.spriteCounter + 1) % len(self.leftspriteList)
            self.stepCounter = 0

    def jump(self):
        if self.isjumping == False:
            self.dy -= 11

class Terrain:

    def __init__(self, pointlist):
        self.pointlist = pointlist
        self.linelist = self.pointlist + [self.pointlist[0]] + [self.pointlist[1]]
        
        #define line direction
        self.linedirect = []
        range(-2, len(), 2)
        for i in range(0, len(self.linelist)-2,2):
            line = self.linelist[i:i+4]
            if line[1]==line[3]:
                self.linedirect.append('horizon')
            elif line[0]==line[2]:
                self.linedirect.append('vertical')
            elif (line[0]-line[2])*(line[1]-line[3])>0:
                self.linedirect.append('leftslop')
            elif (line[0]-line[2])*(line[1]-line[3])<0:
                self.linedirect.append('rightslop')

#-------------------------------------------------------------------
def onAppStart(app):
    app.stepsPerSecond = 30         #Adjust the onStep frequency
    app.bg = Image.open("TP/pics/bg.jpg")
    app.bg = app.bg.resize((app.width,app.height))
    app.bg = CMUImage(app.bg)
    app.fireboy = Character('fireboy','fire',300,400)
    app.watergirl = Character('watergirl','water',400,600)
    loadTerrainPieces(app)
    
def loadTerrainPieces(app):
    # "standard" Terrains 
    bottomwall = Terrain([0,app.height-30, 0,app.height, app.width,app.height, app.width,app.height-30])
    leftwall = Terrain([0,0, 0,app.height, 30,app.height, 30,0])
    rightwall = Terrain( [app.width-30,0, app.width-30,app.height, app.width,app.height, app.width,0])
    topwall = Terrain( [0,0, 0,30, app.width,30, app.width,0])
    testslop1 = Terrain( [30,570, 30,670, 130,670])
    testslop2 = Terrain([1120,570, 1020,670, 1120,670])
    #add more terrins, hard code for three layer
    terrain1 = Terrain([0,525, 0,550, 600,550, 650,500, 800,500, 800,475, 650,475, 600,525])
    terrain2 = Terrain([900,525, 1150,525, 1150,500, 925,500])
    #terrain3 = Terrain([])
    terrain4 = Terrain([0,175, 500,175, 500,150, 50,150, 0,100])
    terrain5 = Terrain([650,175, 1150,175, 1150,100, 1100,150, 650,150])
    terrain6 = Terrain([675,610, 850,610, 825,585, 700,585])
    app.terrainList = [ bottomwall, leftwall, rightwall, topwall,
                        testslop1, testslop2,
                        terrain1,terrain2,terrain4,terrain5,terrain6]

def onKeyHold(app, keys):
    #hold key to control horizontal move
    if 'd' in keys:
        app.fireboy.dx = 4
        app.fireboy.facedirection = 'right'
    elif 'a' in keys:
        app.fireboy.dx = -4
        app.fireboy.facedirection = 'left'
        
    elif 'right' in keys:
        app.watergirl.dx = 4
        app.watergirl.facedirection = 'right'
    elif 'left' in keys:
        app.watergirl.dx = -4
        app.watergirl.facedirection = 'left'

def onKeyRelease(app, keys):
    #app.fireboy.facedirection = 'middle'
    if 'd' in keys:
        app.fireboy.dx = 0
    if 'a' in keys:
        app.fireboy.dx = 0
    if 'right' in keys:
        app.watergirl.dx = 0
    if 'left' in keys:
        app.watergirl.dx = 0

#compute the vector of three points
def lineVector(x1,y1,x2,y2,x3,y3):
    return  (x1-x3)*(y2-y3)-(y1-y3)*(x2-x3)
#print(lineVector(1,3,3,1,1,1))

def collide(linedir, linepoints, character): # should be modified later
    if linedir == 'horizon':
        start = min(linepoints[0],linepoints[2])
        end = max(linepoints[0],linepoints[2])
        #haven't touched and next time will touch -floor
        lowerbound = character.y+character.height//2
        if lowerbound<=linepoints[1]:
            if (lowerbound+character.dy)>=linepoints[1]:
                #also x should with this range
                if character.x <= end and character.x >= start:
                    character.y = linepoints[1]-character.height//2
                    character.dy = 0
                    character.isjumping = False
                    return 'floor'
        #haven't touched and next time will touch -ceil
        if (character.y-character.height//2)>=linepoints[1]:
            if (character.y-character.height//2+character.dy)<=linepoints[1]:
                #also x should with this range
                if character.x <= end and character.x >= start:
                    character.y = linepoints[1] + character.height//2
                    character.dy = 0
                    return 'ceil'
        
    elif linedir == 'vertical':
        start = min(linepoints[1],linepoints[3])
        end = max(linepoints[1],linepoints[3])
        leftpos = character.x - character.width//2
        rightpos = character.x + character.width//2
        #haven't touched and next time will touch -leftwall
        if leftpos >= linepoints[0]:
            if (leftpos+character.dx) <= linepoints[0]:
                #also y should with this range
                if character.y <= end and character.y >= start:
                    character.x = linepoints[0] + character.width//2
                    character.dx = 0
                    print('hit left wall')
                    return 'wall'
        #haven't touched and next time will touch -rightwall
        if rightpos <= linepoints[0]:
            if (rightpos+character.dx) >= linepoints[0]:
                #also y should with this range
                if character.y <= end and character.y >= start:
                    character.x = linepoints[0] - character.width//2
                    character.dx = 0
                    print('hit right wall')
                    return 'wall'
    
    #elif linedir == 'leftslop':
    else:
        #(x1,y1).......
        #....(x,y).....
        #.......(x2,y2)
        x1 = min(linepoints[0],linepoints[2])
        y1 = min(linepoints[1],linepoints[3])
        x2 = max(linepoints[0],linepoints[2])
        y2 = max(linepoints[1],linepoints[3])
        
        lowerleft_x = character.x #x
        lower_y = character.y + character.height//2 #y
        lowerright_x = character.x #x
        
        if linedir == 'leftslop':
            vector = lineVector(x1,y1,x2,y2,lowerleft_x,lower_y)
            nextvector = lineVector(x1,y1,x2,y2,lowerleft_x+character.dx,lower_y+character.dy)
            #haven't touched and next time will touch -leftslop 
            if vector < 0 and nextvector > 0:
                if lowerright_x>=x1 and lowerright_x<=x2 and lower_y >= y1 and lower_y <= y2:
                    print('hit left slop')
                    #put x,y on the slop
                    character.dy = character.dx
                    return 'leftslop'
            #already on the slop
            if vector == 0:
                #and within range
                if lower_y >= y1 and lower_y <= y2 :
                    print('on left slop')
                    #next step for x is (character.d+character.dx)
                    character.dy = character.dx
                    return 'leftslop'

            
        elif linedir == 'rightslop':
            #.......(x2,y1)
            #....(x,y).....
            #(x1,y2).......
            
            vector = lineVector(x1,y2,x2,y1,lowerright_x,lower_y)
            nextvector = lineVector(x1,y2,x2,y1,lowerright_x+character.dx,lower_y+character.dy)
            
            #haven't touched and next time will touch -leftslop 
            if vector < 0 and nextvector > 0:
                if lower_y >= y1 and lower_y <= y2:
                    print('hit right slop')
                    #put x,y on the slop
                    character.dy = -character.dx
                    return 'rightslop'
            #already on the slop
            if vector == 0:
                #and within range
                if lowerright_x >= x1 and lowerright_x <= x2 and lower_y >= y1 and lower_y <= y2:
                    print('on right slop')
                    #next step for x is (character.d+character.dx)
                    character.dy = -character.dx
                    return 'rightslop'
                
        else: return None
    #return None

def onLine(app, character:Character): 
    status = set()
    for terrain in app.terrainList:
        #cheack each line if collide
        for l in range(len(terrain.linedirect)):
            linedir = terrain.linedirect[l]
            linepoints = terrain.linelist[l*2:l*2+4]
            #add current collide line
            collide_status = collide(linedir,linepoints,character)
            if collide_status != None:
                status.add(collide_status)
    return status

def updateStatus(app, character:Character):
    status = onLine(app, character) #return a set of current status
    print(f'current status is {status}')


    
def onStep(app):
    #Update fireboy status
    updateStatus(app, app.fireboy)
    #updateStatus(app, app.watergirl)
    
    #Update the fireboy
    app.fireboy.doStep()
    app.watergirl.doStep()

   
def onKeyPress(app, key):
    #Jump kirb!
    if key == 'w':
        app.fireboy.jump() 
        app.fireboy.isjumping = True
        
    if key == 'up':
        app.watergirl.jump() 
        app.watergirl.isjumping = True

    
def redrawAll(app):
    #Background
    drawImage(app.bg, 0, 0)
    #draw Terrain
    for terrain in app.terrainList:
        drawPolygon(*terrain.pointlist, fill='saddleBrown',opacity=100)
    #draw character
    app.fireboy.draw()
    app.watergirl.draw()
    
def main():
    runApp(width=1150, height=700)

main()
