#----------------------------------------
#    Fireboy and watergirl starter demo v.1.0
#    4/12/2023
#    ID: zhiweny
#    figures are collected from: 
#    https://www.4399.com/   'watergirl & fireboy in forest 5'
#    https://github.com/Hakimos7777/Fireboy_and_watergirl_game
#----------------------------------------

from fireboyandwatergirl_class import *
from cmu_graphics import *
from PIL import Image
import random, time

#-------------------------------------------------------------------
def onAppStart(app):
    reset(app, 'not select')
    
    
def reset(app, level):
    app.gameover = False
    app.gamewin = False
    app.stepsPerSecond = 30         #Adjust the onStep frequency
    app.airs = []                   #Make an empty orb list
    app.lastAirTime = time.time()   #Set an initial orb timer
    #app.level = 'not select'
    app.level = level
    app.myButton = SelectionButton(650, 400, 'hard')
    app.myOtherButton = SelectionButton(500, 400, 'easy')
    #load initial image
    app.bg = Image.open("pics/bg.jpg")
    app.bg = app.bg.resize((app.width,app.height))
    app.bg = CMUImage(app.bg)
    app.hintboard = Image.open("pics/board.jpg")
    app.hintboard = app.hintboard.resize((500,300))
    app.hintboard = CMUImage(app.hintboard)


def loadGameBoardeasy(app):
    app.fireboy = Character('fireboy','fire',925,500,5,5,8,5,10000)
    app.watergirl = Character('watergirl','water',225,500,5,5,9,9,12)
    # "standard" Terrains 
    bottomwall = Terrain([(0,app.height-100), (0,app.height), 
                          (app.width,app.height), (app.width,app.height-100)])
    leftwall = Terrain([(0,0), (0,app.height), (100,app.height), (100,0)])
    rightwall = Terrain( [(app.width-100,0), (app.width-100,app.height), 
                          (app.width,app.height), (app.width,0)])
    topwall = Terrain( [(0,0), (0,100), (app.width,100), (app.width,0)])
    testslop1 = Terrain( [(100,550), (100,600), (150,600)])
    testslop2 = Terrain([(1050,550), (1000,600), (1050,600)])
    terrain1 = Terrain([(0,325),(0,350),(325,350),(325,325)]) #325
    terrain2 = Terrain([(825,325),(825,350),(1150,350),(1150,325)]) #325
    terrain3 = Terrain([(400,400),(275,525),(300,525),(400,425),(750,425),(850,525),(875,525),(750,400)])
    terrain4 = Terrain([(562,425),(562,700),(588,700),(588,425)])
    app.terrainList = [ bottomwall, leftwall, rightwall, topwall,
                        testslop1, testslop2,
                        terrain1,terrain2,terrain3,terrain4] 
    #special terrian
    fire1= SpecialTerrain([(460,400),(560,400)],'fire')
    water1= SpecialTerrain([(580,400),(680,400)],'water')
    app.specialterrainList =[fire1,water1]
    #diamonds
    firediamond1 = Diamond([(110,280),(110,320),(150,320),(150,280)],'fire') #325
    firediamond2 = Diamond([(650,555),(650,595),(690,595),(690,555)],'fire') #600
    waterdiamond1 = Diamond([(1000,280),(1000,320),(1040,320),(1040,280)],'water')#325
    waterdiamond2 = Diamond([(450,555),(450,595),(490,595),(490,555)],'water')#600
    app.diamondList=[firediamond1,firediamond2,waterdiamond1,waterdiamond2]
    #door
    firedoor = Door([(200,260),(200,325),(250,325),(250,260)],'fire')
    waterdoor = Door([(900,260),(900,325),(950,325),(950,260)],'water')
    app.doorList = [waterdoor,firedoor]
    #button
    app.buttonList = []
    
def loadGameBoardhard(app):
    app.fireboy = Character('fireboy','fire',200,600,5,5,8,5,10000)
    app.watergirl = Character('watergirl','water',250,600,5,5,9,9,12)
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
    firedoor = Door([(300,85),(300,150),(350,150),(350,85)],'fire')
    waterdoor = Door([(800,85),(800,150),(850,150),(850,85)],'water')
    app.doorList = [waterdoor,firedoor]
    
    #bottom
    botton1 = Button([(105,450),(105,535),(145,535),(145,450)],'fire') #500+35-85
    botton2 = Button([(600,275),(600,360),(640,360),(640,275)],'water') #325+35
    botton3 = Button([(900,225),(900,310),(940,310),(940,225)],'fire') #275
    botton4 = Button([(700,100),(700,185),(740,185),(740,100)],'water') #150+35-85
    app.buttonList = [botton1,botton2,botton3,botton4]

def onMousePress(app, mouseX, mouseY):
    if app.level == 'not select':
        app.myButton.checkForPress(app, mouseX, mouseY)
        app.myOtherButton.checkForPress(app, mouseX, mouseY)
        if app.level == 'hard':
            loadGameBoardhard(app) 
        elif app.level == 'easy':
            loadGameBoardeasy(app) 
        
def onKeyHold(app, keys):
    if not app.gameover and not app.gamewin:
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
    if not app.gameover and not app.gamewin:
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
        reset(app, 'not select')
        
    if key == 'n':
        if app.level == 'easy':
            reset(app, 'easy')
            loadGameBoardeasy(app) 
        elif app.level == 'hard':
            reset(app, 'hard')
            loadGameBoardhard(app) 

def cross_product(a,b,p):
    """
    judge whether the point p is on the outside of line [a,b] of the geo 
    shape with cross_product
    The line of a shape goes in anti-clockwise direct, if point p lies outside 
    of geo shape, ap x ab < 0
    """
    return (b.x-a.x)*(p.y-a.y)-(p.x-a.x)*(b.y-a.y)


def collide(line:Line, character): 
    
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

def onLine(app, character): 
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
    
def updateStatus(app, character):
    #if in up air! before checking each line collision
    if app.level == 'hard':
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
    if not app.gameover and not app.gamewin and app.level != 'not select':
        #Update fireboy status 
        #Update all terrain, special terrain, diamond, door, button status
        updateStatus(app, app.fireboy)
        updateStatus(app, app.watergirl)
        
        #update door if its been found
        doorcount = 0
        for door in app.doorList:
            if door.isfound:
                doorcount += 1
                door.doStep()
        if doorcount == len(app.doorList) and doorcount != 0:
            app.gamewin = True  
            
        #Update the fireboy
        app.fireboy.doStep()
        app.watergirl.doStep()
        
        #check if character is alive
        if app.fireboy.die or app.watergirl.die:
            app.gameover = True
        
        #additional step for hard level
        if app.level == 'hard':
            #update fire and water pool
            if app.buttonList[0].isfound:
                app.specialterrainList[1].property = 'water'
                app.specialterrainList[1].ischanged = True
            if app.buttonList[1].isfound:
                app.specialterrainList[3].property = 'fire'
                app.specialterrainList[3].ischanged = True
            for sp_terrain in app.specialterrainList: 
                sp_terrain.doStep()
                    
            #update air bubbles
            for air in app.airs:
                air.doStep()

            #Add another air each second
            if (time.time() - app.lastAirTime > 1):
                app.airs.append(Air(app))
                app.lastAirTime = time.time()
                if len(app.airs) >= 20:
                    app.airs = app.airs[-10:]
            
    
def redrawAll(app):
    #Background
    drawImage(app.bg, 0, 0)
    if app.level == 'not select':
        drawRect(575,350,600,300,align='center',fill='salmon',border='yellow',borderWidth=4)
        drawLabel("Welcome to Fireboy & Watergirl!", 575,250, size=30, font='sacramento')
        drawLabel("please choose your level", 575,300, size=20, font='sacramento')
        drawLabel(">>>>>*( >  u  o )<<<<", 575,330, size=20, font='sacramento')
        drawLabel("ALWAYS: press r to reset all and press n to reload current map", 575,475, size=20, font='sacramento')
        app.myButton.draw()
        app.myOtherButton.draw()
    else:
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
        #draw character 
        app.fireboy.draw()
        app.watergirl.draw()
            
        #draw up additional level air for hard level
        if app.level == 'hard':
            if app.buttonList[2].isfound or app.buttonList[3].isfound:
                for air in app.airs:
                    air.draw()
        
        if app.gameover:
            drawRect(575,350,600,300,align='center',fill='salmon',border='yellow',borderWidth=4)
            drawLabel("You died! Please press r to restart", 575,350, size=30, font='sacramento') #font can not be shown correctly
        if app.gamewin:
            drawRect(575,350,600,300,align='center',fill='salmon',border='yellow',borderWidth=4)
            drawLabel(f"Good job, you win!!", 
                    575,275, size=35, font='sacramento')
            drawLabel(f"watergirl score is {app.watergirl.diamond}/{len(app.diamondList)//2}", 
                    575,325, size=30, font='sacramento')
            drawLabel(f"fireboy score is {app.fireboy.diamond}/{len(app.diamondList)//2}", 
                    575,375, size=30, font='sacramento')
            drawLabel('Please press r to restart', 
                    575,425, size=30, font='sacramento')
        
def main():
    runApp(width=1150, height=700)

if __name__ == '__main__':
    main()
