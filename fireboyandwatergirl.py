#----------------------------------------
#    Fireboy and watergirl starter demo v.1.1
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
        #Load the kirb gif
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
        
        #Load the kirb gif
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

        #Set initial position, velocity
        self.x = 100
        self.y = 100
        self.dx = 0
        self.dy = 0
        self.ddy = 0.5
        self.isjumping = False
        
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

#-------------------------------------------------------------------
def onAppStart(app):
    app.stepsPerSecond = 30         #Adjust the onStep frequency
    app.bg = Image.open("TP/pics/bg.jpg")
    app.bg = CMUImage(app.bg)
    app.fireboy = Character('kirb', 'left')
    loadTerrainPieces(app)
    
def loadTerrainPieces(app):
    # Seven "standard" pieces (tetrominoes)
    points1 = [100, 100, 50, 200, 300, 300, 250, 50]
    points2 = [200, 200, 150, 300, 400, 400, 350, 150]
    terrain1 = Terrain(points1)
    terrain2 = Terrain(points2)
    app.terrainList = [ terrain1, terrain2 ]

def onKeyHold(app, keys):
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
        
def onGound(app): # should be modified later
    if app.fireboy.y >= 500:
        app.fireboy.isjumping = False
        return True
    return False

def onStep(app):
    #Update the kirb
    app.fireboy.doStep()
    if onGound(app):
        app.fireboy.y = 500
        app.fireboy.dy = 0

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
        drawPolygon(*terrain.pointlist, fill='saddleBrown',opacity=90)
        
    app.fireboy.draw()
    
def main():
    runApp(width=1000, height=600)

main()
