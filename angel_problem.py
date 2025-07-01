import pygame
import time
import random

pygame.init()

pygame.font.init()

def dummy(params):
    # this is used for buttons where all of the functionality is in the calling subroutine
    return dummy,params

class Label:
    def __init__(self,x,y,w,h,colour=(255,0,0),drawtext=""):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.clickTime = time.time()-1
        self.drawtext = drawtext
        self.colours = colour

    def move(self,vector=(0,0)):
        self.x += vector[0]
        self.y += vector[1]
        return (self.x,self.y,self.w,self.h)
    
    def rescale(self,transformation=(0,0)):
        self.w += transformation[0]
        self.h += transformation[1]
        return (self.x,self.y,self.w,self.h)

    def draw(self,screen,scale):
        scale = scale/800   # dividing by the original scale to resize relative to it
        font = pygame.font.Font('freesansbold.ttf', int(self.h*scale/2))


        pygame.draw.rect(screen,pygame.Color(self.colours),pygame.Rect(self.x*scale,self.y*scale,self.w*scale,self.h*scale))

        drawtext = font.render(self.drawtext, True, "black", self.colours).convert_alpha()

        screen.blit(drawtext, (self.x*scale,int((self.y*scale*2+self.h*scale)/2)-5))

    def setText(self,text):
        self.drawtext = text 

    def setColour(self,colour):
        self.colours = colour



class Button(Label):
    def __init__(self,x,y,w,h,func=dummy,colours=((255,0,0),(0,255,0),(0,0,255)),drawtext=("","","")):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.clickTime = time.time()-1
        self.colours = colours    
        self.func = func
        self.drawtext = drawtext
    
    def draw(self,screen,mx,my,scale):
        scale = scale/800   # dividing by the original scale to resize relative to it
        font = pygame.font.Font('freesansbold.ttf', int(self.h*scale/2))

        if time.time()-self.clickTime <= 0.35:
            pygame.draw.rect(screen,pygame.Color(self.colours[2]),pygame.Rect(self.x*scale,self.y*scale,self.w*scale,self.h*scale))
            drawtext = font.render(self.drawtext[2], True, "black", self.colours[2])
        else:
            hover = self.hoverCheck(mx/scale,my/scale)
            if hover:
                pygame.draw.rect(screen,pygame.Color(self.colours[1]),pygame.Rect(self.x*scale,self.y*scale,self.w*scale,self.h*scale))
                drawtext = font.render(self.drawtext[1], True, "black", self.colours[1])
            else:
                pygame.draw.rect(screen,pygame.Color(self.colours[0]),pygame.Rect(self.x*scale,self.y*scale,self.w*scale,self.h*scale))
                drawtext = font.render(self.drawtext[0], True, "black", self.colours[0])
        screen.blit(drawtext, (self.x*scale,int((self.y*scale*2+self.h*scale)/2)-5))

    def hoverCheck(self,mx,my):
        if self.x < mx and self.x+self.w > mx and self.y < my and self.y+self.h > my:
            hover = True 
        else:
            hover = False
        return hover
    
    def clickAttempt(self,mx,my,scale,params=""):
        scale = scale/800
        hover = self.hoverCheck(mx/scale,my/scale)
        if hover:
            self.func, params = self.func(params)
            self.clickTime = time.time()
        return params, hover





def angelMovementCheck(pos,blocks,power):
    validMoves = []
    for x in range(pos[0]-power,pos[0]+power+1):
        for y in range(pos[1]-power,pos[1]+power+1):
            if (x,y) not in blocks and (x,y) != pos:
                validMoves.append((x,y))
    return validMoves


def reset(blocks):
    blocks = []
    return reset, blocks

def addPower(power):
    if power < 99:
        power += 1
    return addPower, power

def subPower(power):
    if power > 1:
        power -= 1
    return subPower, power

def makeAngelTurn(params):
    return makeDevilTurn, "A"

def makeDevilTurn(params):
    return makeNormalTurn, "D"

def makeNormalTurn(params):
    return makeAngelTurn, "N"




def apply_overlay(screen,screenWidth,screenHeight):
    tempScreen = pygame.Surface((screenWidth,screenHeight))
    tempScreen.set_alpha(150)
    tempScreen.fill((0,0,0))
    screen.blit(tempScreen, (0,0))

def screenReize(screen,prevWidth,prevHeight):
    change = False 
    screenWidth = pygame.display.Info().current_w
    screenHeight = pygame.display.Info().current_h
    if screenWidth != prevWidth and screenHeight != prevHeight:
        change = True
        if abs(screenWidth-prevWidth) > abs(screenHeight-prevHeight):
            screen = pygame.display.set_mode((screenWidth, screenWidth),pygame.RESIZABLE)
            screenHeight = screenWidth
        else:
            screen = pygame.display.set_mode((screenHeight, screenHeight),pygame.RESIZABLE)
            screenWidth = screenHeight
    elif screenWidth != prevWidth:
        change = True
        screen = pygame.display.set_mode((screenWidth, screenWidth),pygame.RESIZABLE)
        screenHeight = screenWidth
    elif screenHeight != prevHeight:
        change = True
        screen = pygame.display.set_mode((screenHeight, screenHeight),pygame.RESIZABLE)
        screenWidth = screenHeight
    return screen, screenWidth, screenHeight, change

def main():
    prevAngelPoses = []
    angelRandomWalk = False
    fpsCounter = {"fps":0,"timeOfMeasure":0,"framesSinceMeasure":0} 

    screenWidth = 800
    screenHeight = 800

    #infoObject = pygame.display.Info()
    forceTurnButton = Button(10,700,300,60,makeAngelTurn,colours=((100,100,100),(150,150,150),(90,90,90)),drawtext=("Force Angel Turn","Force Angel Turn","Force Angel Turn"))

    resetButton = Button(10,10,450,100,reset,colours=((100,100,100),(200,0,0),(90,90,90)),drawtext=("Reset","Are you sure?","Simulation Reset"))

    findAngelButton = Button(10,120,450,100,colours=((255,255,0),(255,255,100),(200,200,0)),drawtext=("Jump to Angel","Jump to Angel","Jumped to Angel"))

    powerText = Label(10,500,630,100,colour=(150,150,150),drawtext=f"Current Angel Power: 1")

    angelAutoButton = Button(10,240,450,60,colours=((255,255,0),(255,255,100),(200,200,0)),drawtext=("Enable Automatic Angel","Enable Automatic Angel","Enable Automatic Angel"))

    powerSubtractButton = Button(10,610,50,50,colours=((100,100,100),(150,150,150),(90,90,90)),drawtext=("-","-","-"),func=subPower)
    powerAddButton = Button(70,610,50,50,colours=((100,100,100),(150,150,150),(90,90,90)),drawtext=("+","+","+"),func=addPower)

    tutorialText = Label(520,762,270,35,colour=(190,190,190),drawtext="Press esc to return to simulation")

    buttons = [forceTurnButton,resetButton,findAngelButton,powerSubtractButton,powerAddButton,angelAutoButton]

    turn = "A"

    cameraOrigin = [0,0]
    cameraOriginDecimal = [0,0]
    cameraWidth = 20
    cameraWidthDecimal = 20

    blocks = []

    keysDown = [0,0,0,0,0,0] # [R,L,D,U,ZOOM,UNZOOM]


    screen = pygame.display.set_mode((screenHeight-100, screenHeight-100),pygame.RESIZABLE)
    multiplier = screenWidth/cameraWidth
    pygame.display.set_caption("Angel Problem")

    power = 1
    if power == 1:
        powerSubtractButton.rescale((-3,-3))
        powerSubtractButton.setColour(((70,70,70),(70,70,70),(70,70,70)))

    angelPos = [-1,-1]
        

    firstIteration = True

    mode = "game"
    firstMenuFrame = True
    turnLock = "N"

    prevWidth = screenWidth
    prevHeight = screenHeight
    #main game loop
    cont = True 
    while cont:
        screen, screenWidth, screenHeight, screenChange = screenReize(screen,prevWidth,prevHeight)
        if screenChange:
            mode = "game"
            firstIteration = True

        if mode == "game":   # set up default screen of game so that the menu has a background
            click = False
            if turnLock in ["A","D"]:
                turn = turnLock
            screen.fill(pygame.Color(100,100,100))
            if turn == "A":
                angelMoves = angelMovementCheck(angelPos,blocks,power)
                if angelRandomWalk:
                    weightedMoves = []
                    distance = lambda a,b: (a**2 + b**2)**(1/2)
                    for move in angelMoves:
                        if distance(angelPos[0],angelPos[1]) <= distance(move[0],move[1]) and move not in prevAngelPoses:
                            weightedMoves.append(move)
                            weightedMoves.append(move)
                            weightedMoves.append(move)
                        if move not in prevAngelPoses:
                            weightedMoves.append(move)
                            weightedMoves.append(move)
                            weightedMoves.append(move)
                            weightedMoves.append(move)

                    for move in weightedMoves:
                        angelMoves.append(move)

                    moveTo = angelMoves[random.randint(0,len(angelMoves)-1)]
                    if moveTo not in prevAngelPoses:
                        prevAngelPoses.append(moveTo)

                    mx, my = moveTo[0], moveTo[1]
                    click = True

            else:
                angelMoves = []

            events = pygame.event.get()
            
            decimal_mx,decimal_my = pygame.mouse.get_pos()
            for event in events:
                if event.type == pygame.QUIT:
                    cont = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        keysDown[5] = 1
                    elif event.key == pygame.K_z:
                        keysDown[4] = 1
                    elif event.key == pygame.K_RIGHT:
                        keysDown[0] = 1
                    elif event.key == pygame.K_LEFT:
                        keysDown[1] = 1
                    elif event.key == pygame.K_DOWN:
                        keysDown[2] = 1
                    elif event.key == pygame.K_UP:
                        keysDown[3] = 1
                    elif event.key == pygame.K_ESCAPE:
                        firstMenuFrame = True
                        mode = "menu"

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_x:
                        keysDown[5] = 0
                    elif event.key == pygame.K_z:
                        keysDown[4] = 0
                    elif event.key == pygame.K_RIGHT:
                        keysDown[0] = 0
                    elif event.key == pygame.K_LEFT:
                        keysDown[1] = 0
                    elif event.key == pygame.K_DOWN:
                        keysDown[2] = 0
                    elif event.key == pygame.K_UP:
                        keysDown[3] = 0

                if event.type == pygame.MOUSEBUTTONDOWN and not firstIteration:
                    mx = (decimal_mx/multiplier) - int(cameraWidth/2) - cameraOrigin[0]
                    my = (decimal_my/multiplier) - int(cameraWidth/2) - cameraOrigin[1]
                    if mx >= 0:
                        mx = int(mx)
                    else:
                        mx = int(mx)-1
                    if my >= 0:
                        my = int(my)
                    else:
                        my = int(my)-1
                    click = True
                    
            if click:
                if turn == "A":
                    if angelPos != [mx,my] and (mx,my) not in blocks and (mx,my) in angelMoves:
                        angelPos = [mx,my]
                        turn = "D"
                else:
                    if (mx,my) not in blocks and angelPos != [mx,my]:
                        blocks.append((mx,my))
                        turn = "A"
                        
            fpsMultiplier = 100/(fpsCounter["fps"]+1)

            if keysDown[0] == 1:
                cameraOriginDecimal[0] -= 0.005*cameraWidth*fpsMultiplier
            if keysDown[1] == 1:
                cameraOriginDecimal[0] += 0.005*cameraWidth*fpsMultiplier
            if keysDown[2] == 1:
                cameraOriginDecimal[1] -= 0.005*cameraWidth*fpsMultiplier
            if keysDown[3] == 1:
                cameraOriginDecimal[1] += 0.005*cameraWidth*fpsMultiplier


            maybeCameraWidth = lambda cameraWidth: 10 if cameraWidth > 100 else 1 if cameraWidth < 10 else cameraWidth/10
            
            if keysDown[4] == 1 and cameraWidthDecimal > 1:
                cameraWidthDecimal -= 0.15*fpsMultiplier*maybeCameraWidth(cameraWidth)
                cameraWidth = round(cameraWidthDecimal)
            if keysDown[5] == 1:
                cameraWidthDecimal += 0.15*fpsMultiplier*maybeCameraWidth(cameraWidth)
                cameraWidth = round(cameraWidthDecimal)
            
            cameraOrigin = [round(cameraOriginDecimal[0]),round(cameraOriginDecimal[1])]
                        
            
            multiplier = screenWidth/cameraWidth
            
            



            for x in range(-cameraOrigin[0]-int(cameraWidth/2),-cameraOrigin[0]+cameraWidth-int(cameraWidth/2)):
                for y in range(-cameraOrigin[1]-int(cameraWidth/2),-cameraOrigin[1]+cameraWidth-int(cameraWidth/2)):
                    if (x,y) in blocks:
                        pygame.draw.rect(screen,pygame.Color((255,0,0)),pygame.Rect((cameraOrigin[0]+x+int(cameraWidth/2))*multiplier,(cameraOrigin[1]+y+int(cameraWidth/2))*multiplier,multiplier+1,multiplier+1))
                    if (x,y) in angelMoves:
                        pygame.draw.rect(screen,pygame.Color((200,200,255)),pygame.Rect((cameraOrigin[0]+x+int(cameraWidth/2))*multiplier,(cameraOrigin[1]+y+int(cameraWidth/2))*multiplier,multiplier+1,multiplier+1))
                    if [x,y] == angelPos:
                        pygame.draw.rect(screen,pygame.Color((255,255,0)),pygame.Rect((cameraOrigin[0]+x+int(cameraWidth/2))*multiplier,(cameraOrigin[1]+y+int(cameraWidth/2))*multiplier,multiplier+1,multiplier+1))
            
            for x in range(cameraWidth):
                pygame.draw.rect(screen,pygame.Color(0,0,0),pygame.Rect(x*multiplier,0,1,screenWidth))
            for y in range(cameraWidth):
                    pygame.draw.rect(screen,pygame.Color(0,0,0),pygame.Rect(0,y*multiplier,screenWidth,1))
                
            prevWidth = screenWidth
            prevHeight = screenHeight
            
            if firstIteration:
                mode = "menu"
                firstIteration = False
                firstMenuFrame = True
            else:
                pygame.display.update()

        elif mode == "menu":
            frameReset = False
            if firstMenuFrame:
                apply_overlay(screen,screenWidth,screenHeight)
                firstMenuFrame = False
            
            events = pygame.event.get()
            
            decimal_mx,decimal_my = pygame.mouse.get_pos()

            for event in events:
                click = False
                if event.type == pygame.QUIT:
                    cont = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mode = "game"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    blocks, clicked = resetButton.clickAttempt(decimal_mx,decimal_my,screenWidth,blocks)
                    if clicked:
                        frameReset = True
                        turn = "A"
                        cameraOrigin = [0,0]
                        cameraOriginDecimal = [0,0]
                        cameraWidth = 20
                        cameraWidthDecimal = 20
                        angelPos = [-1,-1]

                    temp, clicked = findAngelButton.clickAttempt(decimal_mx,decimal_my,screenWidth)
                    if clicked:
                        cameraOrigin = [-angelPos[0]-1,-angelPos[1]-1]
                        cameraOriginDecimal = [-angelPos[0]-1,-angelPos[1]-1]
                        frameReset = True
                    
                    temp, clicked = angelAutoButton.clickAttempt(decimal_mx,decimal_my,screenWidth)
                    if clicked:
                        if angelRandomWalk:
                            angelRandomWalk = False
                            angelAutoButton.setText(("Enable Automatic Angel","Enable Automatic Angel","Enable Automatic Angel"))
                        else:
                            angelRandomWalk = True 
                            angelAutoButton.setText(("Disable Automatic Angel","Disable Automatic Angel","Disable Automatic Angel"))
                        

                    newPower, clicked = powerAddButton.clickAttempt(decimal_mx,decimal_my,screenWidth,power)
                    if clicked:
                        if power == 1:
                            powerSubtractButton.setColour(((100,100,100),(150,150,150),(90,90,90)))
                            powerSubtractButton.rescale((3,3))
                        if power == 98:
                            powerAddButton.setColour(((70,70,70),(70,70,70),(70,70,70)))
                            powerAddButton.rescale((-3,-3))
                        if turn == "A":
                            frameReset = True
                    power = newPower

                    newPower, clicked = powerSubtractButton.clickAttempt(decimal_mx,decimal_my,screenWidth,power)
                    if clicked:
                        if power == 2:
                            powerSubtractButton.setColour(((70,70,70),(70,70,70),(70,70,70)))
                            powerSubtractButton.rescale((-3,-3))
                        if power == 99:
                            powerAddButton.setColour(((100,100,100),(150,150,150),(90,90,90)))
                            powerAddButton.rescale((3,3))
                        if turn == "A":
                            frameReset = True
                    power = newPower


                    newTurnLock, clicked = forceTurnButton.clickAttempt(decimal_mx,decimal_my,screenWidth)
                    if clicked:
                        turnLock = newTurnLock
                        if turnLock == "A":
                            forceTurnButton.setText(("Force Devil Turn","Force Devil Turn","Force Devil Turn"))
                        elif turnLock == "D":
                            forceTurnButton.setText(("Remove Turn Force","Remove Turn Force","Remove Turn Force"))
                        else:
                            forceTurnButton.setText((("Force Angel Turn","Force Angel Turn","Force Angel Turn")))
                        frameReset = True
            if frameReset:
                firstIteration = True
                mode = "game"


            for button in buttons:
                button.draw(screen,decimal_mx,decimal_my,screenWidth)

            powerText.setText(f"Current Angel Power: {power}")
            powerText.draw(screen,screenWidth)

            tutorialText.draw(screen,screenWidth)

            prevWidth = screenWidth
            prevHeight = screenHeight

            pygame.display.update()
        else:
            raise(Exception("Unexpected mode found - only 'menu' and 'game' are allowed"))
    
        fpsCounter["framesSinceMeasure"] += 1
        if time.time() - fpsCounter["timeOfMeasure"] >= 0.1:
            fpsCounter["timeOfMeasure"] = time.time()
            fpsCounter["fps"] = fpsCounter["framesSinceMeasure"]*10
            fpsCounter["framesSinceMeasure"] = 0
            #print(fpsCounter["fps"])


if __name__ == "__main__":
    main()

