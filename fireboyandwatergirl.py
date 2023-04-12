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
    def __init__(self):
        self.x, self.y = 100, 100
        self.dx = 0
        self.dy = 0

class Terrain:
    def __init__(self, pointlist):
        self.pointlist = pointlist

#-------------------------------------------------------------------
def onAppStart(app):
    app.stepsPerSecond = 30         #Adjust the onStep frequency
    app.bg = Image.open("TP/pics/bg.jpg")
    app.bg = CMUImage(app.bg)
    loadTerrainPieces(app)

#def openImage(fileName):
    #return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
    
def loadTerrainPieces(app):
    # Seven "standard" pieces (tetrominoes)
    points1 = [100, 100, 50, 200, 300, 300, 250, 50]
    points2 = [200, 200, 150, 300, 400, 400, 350, 150]
    terrain1 = Terrain(points1)
    terrain2 = Terrain(points2)
    app.terrainList = [ terrain1, terrain2 ]

'''
def onStep(app):
    #Update the kirb
    app.kirb.doStep()
'''
    
def redrawAll(app):
    #Background
    drawImage(app.bg, 0, 0)
    #draw Terrain
    for terrain in app.terrainList:
        print(terrain.pointlist)
        drawPolygon(*terrain.pointlist, fill='cyan', border='black')

def main():
    runApp(width=1000, height=600)

main()
