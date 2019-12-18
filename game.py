# Program Name: Mazin Shaaeldin
# Developer Names: Mazin & Tom
# Date Published: June 2019
# Date Edited: December 2019
# Description: Drihili Forest presents Abebi (a Nigerian man) who attempts to reunite with his lost family.
#              He is forced to tread the dark, maze like forest while avoiding the trees, being wary of his health, and
#              escaping in a timely manner.

import pygame
import random 
import time
from pygame.locals import *
path = 'highScore.txt'
#------------------------------------------------------------------
#Always must have to play music
pygame.mixer.init(44100, -16,2,2048)

#Play Background music
pygame.mixer.music.load("Madagascar Escape.mp3") # setting music
pygame.mixer.music.set_volume(0.5) #setting volume(from 0 to 1)
pygame.mixer.music.play(-1) #playing it...-1 means loop endlessely
#-------------------------------------------------------------------

#Set game caption
pygame.display.set_caption('Computer Science ISU: Drihili Forest')
#Initialize of game and import of pictures
path = 'highScore.txt'
barracade = pygame.Rect(10, 10, 10, 10)
WIDTH = 1300
HEIGHT = 700
gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))                                                   # Set Game Screen size
characterImage = pygame.transform.scale(pygame.image.load('possible.png').convert_alpha(),(25,25))      # Scaled Images
mazeBackground = pygame.image.load('mazeBackground.jpg')
wallImage = pygame.transform.scale(pygame.image.load('wall.jpg').convert_alpha(),(50, 50))
emptyImage = pygame.transform.scale(pygame.image.load('empty.jpg').convert_alpha(),(50,50))
powerUp = pygame.transform.scale(pygame.image.load('powerup.png').convert_alpha(),(50,50))

pygame.init()
white = 255,255,255                                                                                     # Set colors
red = 255, 0 ,0
blue = 0,0,128
clockobject = pygame.time.Clock()

#message to screen
def messageToScreen(msg,color,x,y,fontSize):                                                            # Created message to screen function
    '''
    messageToScreen is a function that outputs to the screen
    ---param
    msg: string
    color: tuple
    x:int(x coordinate)
    y:int(y coordinate)
    z:int(size of input text)
    ---return:none
    '''
    fontOne = pygame.font.Font('freesansbold.ttf',fontSize)
    screenText = fontOne.render(msg, True, color) #set message
    gameDisplay.blit(screenText,[x,y])
#end of messageToScreen
        
#Power Ups
class powerUps(pygame.sprite.Sprite):                                                                  # Created a class powerup that inhirits sprite properties.
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH),random.randint(50,HEIGHT))
    #end of initialization
#end of powerUps
        
#Chasing police officer
class movingPolice(pygame.sprite.Sprite):
    def __init__(self, image, initialX, initialY):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (initialX, initialY)
        self.x = initialX
        self.y = initialY
        self.__vy = 1
        self.__vx = 1
    #end of init

    def update(self):
        self.rect.y += (self.__vy)
        self.rect.x += (self.__vx)
    #end of update

    def changeSpeed(self, inputLocation):
        locationX = inputLocation[0]
        locationY = inputLocation[1]
        if self.rect.x > locationX:
            self.__vx = -1
        else:
            self.__vx = 1
        #end of if
        if self.rect.y > locationY:
            self.__vy = -1
        else:
            self.__vy = 1
        #end of if
    #end of changeSpeed

    def resetPosition(self):
        self.rect.center = (self.x, self.y)
    #end of resetPosition
#Character Class

class character(pygame.sprite.Sprite):
    '''
    character class used to gather information about character in the game
    '''
    def __init__(self, name, charImage, score = 0, health = 3, time = 20):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.score = score
        self.image = charImage
        self.health = health
        self.rect = self.image.get_rect()
        self.rect.center = (100, 150)
        self.time = 20
    #end of __init__
    
    def update(self):
        start = time.time()
        self.__speedx = 0
        self.__speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] and self.rect.left > -50:
            self.__speedx = -10
        if keystate[pygame.K_RIGHT] and self.rect.right < WIDTH+30:
            self.__speedx = 10
        if keystate[pygame.K_UP] and self.rect.top > 50:
            self.__speedy = -10
        if keystate[pygame.K_DOWN] and self.rect.bottom < HEIGHT+30:
            self.__speedy = +10
        self.rect.x += self.__speedx
        self.rect.y += self.__speedy
        end = time.time()
    #end of update

    def getPosition(self):
        #this returns the current position of the character
        return(self.rect.x, self.rect.y)
    #end of getPostion

    def plusScore(self):
        self.score += 1
    #end of plusScore

    def displayScore(self):
        messageToScreen("Your score is: " + str(self.score), red, 10, 10, 50)
    #end of displayScore

    def getScore(self):
        return(self.score)
    #end of getScore

    def loseHealth(self):
        self.health -= 1
    #end of loseHealth

    def displayHealth(self):
        messageToScreen("Health: " + str(self.health), red, 800, 10, 50)
    #end of displayHealth

    def getHealth(self):
        return(self.health)
    #end of getHealth

    def resetPosition(self):
        self.rect.center = (100,150)
    #end of resetPosition

    def getTime(self):
        return(self.time)
    #end of getTime

    def increaseTime(self, amount):
        self.time += amount
    #end of increaseTime

    def decreaseTime(self):
        self.time -= 1
    #end of decreaseTime

    def displayTime(self):
        messageToScreen("Time: " + str(self.time), red, 900, 400, 50)
    #end of displayTime 
#end of character

class cell(pygame.sprite.Sprite):
    ''' cell classes creates a 2D surface with a 2D array in order to conduct Breadth First Search Algorithm
    '''
    w, h = 50, 50
    def __init__(self, locationX, locationY, isWall, isPowerUp, image, rowPosition = None, columnPosition = None):
        pygame.sprite.Sprite.__init__(self)
        self.isWall = isWall
        if locationX == 100 and locationY == 150:
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.center = (locationX, locationY)
            self.origin = True
            self.rowPosition = rowPosition
            self.columnPosition = columnPosition
        elif isWall:
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.center = (locationX, locationY)
            self.rowPosition = rowPosition
            self.columnPosition = columnPosition
        else:
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.center= (locationX, locationY)
            self.rowPosition = rowPosition
            self.columnPosition = columnPosition
        #end of if
    #end of initialization

    def getLocation(self):
        return(self.rowPosition, self.columnPosition)
    #end of getLocation

    def checkWall(self):
        return(self.isWall)
    #end of checkWall(self):
#end of cell

def mapGeneration():
    ''' map generation generates a solvable maze viable the Breadth First Search Algorithm
    ---param: none
    ---return: tuple of sprite groups and array
    '''
    def createMap():
        ''' creates a random map both graphically and in the form of a 2D array
        --- param: none
        --- return: tuple of sprites and array
        '''
        myX = list(range(600, 800,50))
        myY = list(range(400, 650,50))
        setA = random.choice(myX)
        setB = random.choice(myY)
        cells = []
        emptySpace = pygame.sprite.Group()
        specialSpace = pygame.sprite.Group()
        blockedWalls = pygame.sprite.Group()
        rowPosition = 0
        columnPosition = 0
        for counter in range(100, 800,50):
            columnPosition = 0
            row = []
            for value in range(150,650,50):
                check = random.randint(0,1)
                if counter == 100 and value == 150:
                    temp = cell(counter, value, False, False, emptyImage, rowPosition, columnPosition)
                    emptySpace.add(temp)
                elif counter == setA and value == setB:
                    temp = cell(counter, value, False, True, powerUp, rowPosition, columnPosition)
                    temp.isWall = "Score"
                    specialSpace.add(temp)
                elif (check):
                    temp = cell(counter,value, True, False, wallImage, rowPosition, columnPosition)
                    blockedWalls.add(temp)
                else:
                    temp = cell(counter,value, False, False, emptyImage, rowPosition, columnPosition)
                    emptySpace.add(temp)
                row.append(temp)
                columnPosition += 1
            #end of for
            rowPosition += 1
            cells.append(row)
        #end of for
        
        yConstant = [100,650]
        for counter in range (100, 800, 50):
            tempOne = cell(counter, yConstant[0], True, False, wallImage)
            tempTwo = cell(counter, yConstant[1], True, False, wallImage)
            blockedWalls.add(tempOne)
            blockedWalls.add(tempTwo)
        #end of for
        xConstant = [50, 800]
        for counter in range(100, 700, 50):
            tempOne = cell(xConstant[0], counter, True, False, wallImage)
            tempTwo = cell(xConstant[1], counter, True, False, wallImage)
            blockedWalls.add(tempOne)
            blockedWalls.add(tempTwo)
        #end for
        return(emptySpace, specialSpace, blockedWalls, cells)
    #end of createMap

    def checkMap(cells):
        ''' uses BFS algorithm checks if a maze is actually solvable
        ---param: 2D Array
        ---return: Boolean
        '''
        checkList = cells.copy()
        start = checkList[0][0]
        queueList = [start]
        visitedList = [[0,0]]
        found = False
        moveCoordinates = [[1,0],[0,1],[-1,0],[0,-1]]
        while len(queueList) > 0 and not(found):
            check = queueList.pop(0)
            tempX,tempY = check.getLocation()
            for move in moveCoordinates:
                row = tempX + move[0]
                column = tempY + move[1]
                if (row > -1 and row <14) and (column > -1 and column < 10):
                    wallCheck = checkList[row][column].checkWall()
                    if not(wallCheck) and [row,column] not in visitedList:
                        queueList.append(checkList[row][column])
                        visitedList.append([row,column])
                    elif (wallCheck == "Score"):
                        found = True
                    #print(queueList)
                #end of if
            #end of for
        #end of while
        return(found)
    #end of checkMap
    
    notMatched = True
    while notMatched:
        emptySpace, specialSpace, blockedWalls, cells = createMap()
        if checkMap(cells):
            return(emptySpace, specialSpace, blockedWalls, cells)
#end of mapGenearation

def readsortScore(path):
    output = {}
    scoreFile = open(path, 'r')
    allScore = scoreFile.read()
    allScore = allScore.split(" ")
    counter = 0
    for value in allScore:
        if counter == 0:
            tempValue = value
            counter += 1
        elif counter == 1:
            tempValue += value
            counter += 1
        elif counter == 2:
            output[tempValue] = int(value)
            counter = 0
            tempValue = ""
        #end of if   
    #end of for
    return(output)
#end of readsortScore

#Get character name
def getCharacterName():
    '''
    getCharacterName gets the name of the player
    ---param:none
    ---return:string
    '''
    output = ""
    gameDisplay.blit(mazeBackground, [0,0])
    messageToScreen("Please enter your name:", red, 300, 80, 50)
    pygame.display.update()
    endEvent = False
    while not(endEvent):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    endEvent = True
                elif event.key == pygame.K_SPACE:
                    output += chr(event.key)
                elif chr(event.key).isalpha():
                    output+=chr(event.key)
                    gameDisplay.blit(mazeBackground, [0,0])
                    messageToScreen("Please enter your name:", red, 300, 80, 50)
                    messageToScreen(output, red, 300, 150, 50)
                    pygame.display.update()
                elif event.key == pygame.K_BACKSPACE:
                    output = output[:len(output)-1]
                    gameDisplay.blit(mazeBackground, [0,0])
                    messageToScreen("Please enter your name:", red, 300, 80, 50)
                    messageToScreen(output, red, 300, 150, 50)
                    pygame.display.update()
                #end of if
            #end of if
        #end of for
    #end of while
    gameDisplay.blit(mazeBackground, [0,0])
    messageToScreen("Welcome " + output, red, 200, 200, 100)
    messageToScreen("Game starts in 3 seconds", red, 200, 400, 50)
    pygame.display.update()
    time.sleep(3)
    return(output)
#end of getCharacterName

#Start game       
def startGame():
    emptySpace, specialSpace, blockedWalls, cells = mapGeneration()
    playerSprite = pygame.sprite.Group()
    exitGame = False
    ''' sets up game character and sprites '''
    name = getCharacterName()
    person = character(name, characterImage)
    playerSprite.add(person)
    startTime = time.time()
    # collision detection and update screen
    def updateScreen():  
        gameDisplay.fill(white)
        playerSprite.update()
        emptySpace.draw(gameDisplay)
        playerSprite.draw(gameDisplay)
        blockedWalls.draw(gameDisplay)
        specialSpace.draw(gameDisplay)
        person.displayHealth()
        person.displayScore()
        person.displayTime()
        pygame.display.flip()
        currentPosition = person.getPosition()
    #end of updateScreen
    
    def collisionProcessing(blockedWalls, specialSpace):
        hit = pygame.sprite.spritecollide(person, blockedWalls, False) #False here means block doesn't get removed
        endMaze = pygame.sprite.spritecollide(person, specialSpace, False)
        if hit:
            person.loseHealth()
            person.increaseTime(20)
            person.resetPosition()
            hit = False
            updateScreen()
            time.sleep(1)
        #end of if
        return (endMaze) 
    #end of collision Processing

    while not(exitGame):
        endTime = time.time()
        if endTime - startTime > 1:
            startTime = time.time()
            person.decreaseTime()
        #end of if
        time.sleep(0.005)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exitGame = True
            #end of if
        #end of for
        endMaze = collisionProcessing(blockedWalls, specialSpace)
        if endMaze:
            person.plusScore()
            person.increaseTime(5)
            emptySpace, specialSpace, blockedWalls, cells = mapGeneration()
            person.resetPosition()
            time.sleep(1)
            updateScreen()
            endMaze = False
        #end of if
        if not(person.getHealth()):
            exitGame = True
        #end of if
        updateScreen()

        if person.getTime() < 0:
            person.loseHealth()
            person.resetPosition()
            person.increaseTime(20)
            updateScreen()
            time.sleep(1)
        #end of if
    #end of while
    return(person.getScore())
#end of startGame

def highScore(path, currentScore):
    def readsortScore(path):
        output = {}
        scoreFile = open(path, 'r')
        allScore = scoreFile.read()
        allScore = allScore.split(" ")
        counter = 0
        for value in allScore:
            if counter == 0:
                tempValue = value
                counter += 1
            elif counter == 1:
                output[tempValue] = int(value)
                counter = 0
                tempValue = ""
            #end of if   
        #end of for
        scoreFile.close()
        return(output)
    #end of readsortScore

    currentHighScore = readsortScore(path)

    def sortHighScore(currentHighScore, currentScore):
        currentValues = list(currentHighScore.values())
        if currentScore > currentValues [2] and currentScore < currentValues[1]:
            currentValues[2] = currentScore
        elif currentScore > currentValues[1] and currentScore < currentValues[0]:
            currentValues[2] = currentValues[1]
            currentValues[1] = currentScore
        elif currentScore > currentValues[0]:
            currentValues[2] = currentValues[1]
            currentValues[1] = currentValues[0]
            currentValues[0] = currentScore
         #end of if
        return(currentValues)
    #end of sortHighScore


    currentValues = sortHighScore(currentHighScore, currentScore)

    def writeHighScore(currentValues, currentHighScore):
        scoreFile = open(path, 'w')
        scoreFile.truncate(0)
        currentKeys = list(currentHighScore.keys())
        for counter in range(3):
            scoreFile.write(str(currentKeys[counter]) + " ")
            scoreFile.write(str(currentValues[counter]) + " ")
        #end of for
        scoreFile.close()
    #end of def

    writeHighScore(currentValues, currentHighScore)
    print("ran")
    return(list(currentHighScore.keys()), currentValues)
#end of highScore

#main menu
def mainMenu():
    '''
    mainMenu displays the main menu of the game
    no param and no return
    '''
    gameDisplay.blit(mazeBackground, [0,0]) #Sets backgound
    messageToScreen("Drihili Forest", red, 230, 80, 150)
    messageToScreen("Survive the longest you can!", red, 100, 300, 30)
    messageToScreen("Grab the Cubes!", red, 100, 400, 30)
    messageToScreen("Press C to Play, q to exit!", red, 100, 500, 30)
    pygame.display.update()
    gotEvent = False #Used to keep the while loop running
    while not(gotEvent):
        events = pygame.event.get() #Records events happening in the game
        for event in events:
            if event.type == pygame.QUIT: #If presses x button
                pygame.quit()
                gotEvent = True
            elif event.type == KEYDOWN and (event.key == K_x):
                pygame.quit()
                gotEvent = True
            elif event.type == KEYDOWN and (event.key == K_c):
                score = startGame()
                gotEvent = True
            #end of if
        #end of for
    #end of while
    return(score)
#end of mainMenu

def endGame(player, score):
    gameDisplay.blit(mazeBackground, [0,0])
    location = 100
    for counter in range(3):
        messageToScreen(player[counter] + " " + str(score[counter]), red, 200, location, 50)
        location += 100
    #end of for
    messageToScreen("Thanks for playing", red, 200, location + 100, 100)
    pygame.display.update()
#end of endGame  
    
def runProgram():
    currentScore = mainMenu()
    player, score = (highScore(path, currentScore))
    endGame(player, score)
#end of runProgram

runProgram()
