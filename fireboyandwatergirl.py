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
    def __init__(self, name, nature):
        #set property
        self.name = name
        self.nature = nature
        self.facedirection = 'left'
        
        #condition on current direction
        left_filepath = f'TP/pics/{self.name}.gif'
        right_filepath = f'TP/pics/{self.name}_right.gif'
        middle_filepath = f'TP/pics/{self.name}_middle.gif'
        
        ### Adapted from mdtaylor: KirbleBird starter demo v.1.1 ###
        #Load the left gif
        self.leftspriteList = []
        myGif = Image.open(left_filepath)
        for frame in range(myGif.n_frames):  #For every frame index...
            #Seek to the frame, convert it, add it to our sprite list
            myGif.seek(frame)
            fr = myGif.resize((myGif.size[0]//2, myGif.size[1]//2))
            fr = CMUImage(fr)
            self.leftspriteList.append(fr)
        ##Fix for broken transparency on frame 0
        self.leftspriteList.pop(0)
        
        #Load the right gif
        self.rightspriteList = []
        myGif = Image.open(left_filepath)
        for frame in range(myGif.n_frames):  #For every frame index...
            #Seek to the frame, convert it, add it to our sprite list
            myGif.seek(frame)
            fr = myGif.resize((myGif.size[0]//2, myGif.size[1]//2))
            fr = fr.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            fr = CMUImage(fr)
            self.rightspriteList.append(fr)
        ##Fix for broken transparency on frame 0
        self.rightspriteList.pop(0)
        
        #Set sprite counters
        self.stepCounter = 0
        self.spriteCounter = 0

        #Set initial position, velocity, size
        self.x = 100
        self.y = 100
        self.dx = 0
        self.dy = 0
        self.ddy = 0.5
        self.isjumping = False
        self.width = myGif.size[0]//2
        self.height  = myGif.size[1]//2
        
    ### Adapted from mdtaylor: KirbleBird starter demo v.1.1 ###  
    def draw(self):
        #Draw left kirb sprite
        if self.facedirection == 'left':
            drawImage(self.leftspriteList[self.spriteCounter], 
                    self.x, self.y, align = 'center')
        #Draw right kirb sprite
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
            self.dy -= 10

class Terrain:
    def __init__(self, pointlist):
        self.pointlist = pointlist
        self.linelist = self.pointlist + [self.pointlist[0]] + [self.pointlist[1]]
        
        #define line direction
        self.linedirect = []
        for i in range(0, len(self.linelist)-2,2):
            line = self.linelist[i:i+4]
            if line[0]==line[2]:
                self.linedirect.append('horizon')
            elif line[1]==line[3]:
                self.linedirect.append('vertical')
            else:
                self.linedirect.append('slop')
        

#-------------------------------------------------------------------
def onAppStart(app):
    app.stepsPerSecond = 30         #Adjust the onStep frequency
    app.bg = Image.open("TP/pics/bg.jpg")
    app.bg = app.bg.resize((app.width,app.height))
    app.bg = CMUImage(app.bg)
    app.fireboy = Character('kirb', 'left')
    loadTerrainPieces(app)
    
def loadTerrainPieces(app):
    # Seven "standard" pieces (tetrominoes)
    bottomwall = [0,app.height-30, 0,app.height, app.width,app.height, app.width,app.height-30]
    #bottomwall_dir = []
    leftwall = [0,0, 0,app.height, 30,app.height, 30,0]
    #leftwall_dir = []
    rightwall = [app.width-30,0, app.width-30,app.height, app.width,app.height, app.width,0]
    #rightwall_dir = []
    topwall = [0,0, 0,30, app.width,30, app.width,0]
    #topwall_dir = []
    #testslop1 = []
    terrain1 = Terrain(bottomwall)
    terrain2 = Terrain(leftwall)
    terrain3 = Terrain(rightwall)
    terrain4 = Terrain(topwall)
    app.terrainList = [ terrain1, terrain2, terrain3, terrain4]

def onKeyHold(app, keys):
    #hold key to control horizontal move
    if 'd' in keys:
        app.fireboy.dx = 5
        app.fireboy.facedirection = 'right'
    elif 'a' in keys:
        app.fireboy.dx = -5
        app.fireboy.facedirection = 'left'

def onKeyRelease(app, keys):
    #app.fireboy.facedirection = 'middle'
    if 'd' in keys:
        app.fireboy.dx = 0
    if 'a' in keys:
        app.fireboy.dx = 0

def collide(linedir, linepoints, character): # should be modified later
    if linedir == 'horizon':
        #haven't touched and next time will touch
        if (character.y+character.height//2)<=linepoints[1]:
            if (character.y+character.height//2+character.dy)>=linepoints[1]:
                character.y = linepoints[1]-character.height//2
                character.dy = 0
                character.isjumping = False
                return 'floor'
        if (character.y-character.height//2)>=linepoints[1]:
            if (character.y-character.height//2+character.dy)<=linepoints[1]:
                character.y = linepoints[1] + character.height//2
                character.dy = 0
                return 'ceil'
        
    elif linedir == 'vertical':
        leftpos = character.x - character.width//2
        rightpos = character.x + character.width//2
        #haven't touched and next time will touch
        print(leftpos,rightpos,linepoints[0])
        if leftpos >= linepoints[0]:
            if (leftpos+character.dx) <= linepoints[0]:
                character.x = linepoints[0] + character.width//2
                character.dx = 0
                print('hit left wall')
                return 'wall'
        if rightpos <= linepoints[0]:
            if (rightpos+character.dx) >= linepoints[0]:
                character.x = linepoints[0] - character.width//2
                character.dx = 0
                print('hit right wall')
                return 'wall'
        
    elif linedir == 'slop':
        x1 = min(linepoints[0],linepoints[2])
        y1 = min(linepoints[1],linepoints[3])
        x2 = max(linepoints[0],linepoints[2])
        y2 = max(linepoints[1],linepoints[3])
        
        lowerleft_x = character.x - character.width//2
        lower_y = character.y + character.height//2
        lowerright_x = character.x + character.width//2
        #(x1,y1).......
        #....(x,y).....
        #.......(x2,y2)
        if lowerleft_x > x1 and lowerleft_x < x2 and lower_y > y1 and lower_y < y2:
            if (x2-lowerleft_x)==(y2-lower_y) and (lowerleft_x-x1)==(lower_y-y1):
                return 'leftslop'
        #.......(x2,y1)
        #....(x,y).....
        #(x1,y2).......
        if lowerright_x < x2 and lowerright_x > x1 and lower_y > y1 and lower_y < y2:
            if (lowerright_x-x1)==(y2-lower_y) and (x2-lowerright_x)==(lower_y-y1):
                return 'leftslop'
    return None

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
    #charcter on ground, stand still
    status = onLine(app, character) #return a set of current status
    #if 'floor' in status:
        #character.dy = 0
        #character.isjumping = False
        
    #charcter hit ceilling, lose y speed
    #if 'ceil' in status:
        #character.dy = 0
    
    #charcter on a slop, slip slowly
    if 'leftslop' in status:
        character.dx = 1
        character.dy = 1
    if  'rightslop' in status:
        character.dx = -1
        character.dy = 1
    
    #character hit wall
    #if 'wall' in status:
    #    character.dx = 0
    
def onStep(app):
    #Update fireboy status
    updateStatus(app, app.fireboy)
    #Update the fireboy
    app.fireboy.doStep()

   
def onKeyPress(app, key):
    #Jump kirb!
    if key == 'w':
        app.fireboy.jump() 
        app.fireboy.isjumping = True

    
def redrawAll(app):
    #Background
    drawImage(app.bg, 0, 0)
    #draw Terrain
    for terrain in app.terrainList:
        drawPolygon(*terrain.pointlist, fill='saddleBrown',opacity=100)
        
    app.fireboy.draw()
    
def main():
    runApp(width=1150, height=700)

main()
