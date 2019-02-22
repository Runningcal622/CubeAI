#Caleb Vanorio
#CSC 339
# cube GUI
''' This operates as a driver for the Rubik cube. Allowing for manipulating the cube through
the 12 moves: clockwise and counterclockwise on each face. It displays the Cube and allows
for users to enter in moves and directions and models those.
valid moves are "front cc" or "back clockWise"
Functions:
makeWindow: initialize the window
drawCube: draws the current state of the cube
randomMoves: does a specific amount of random turns'''


from graphics import *
import math
import random
from BetterCube import *
from queue import PriorityQueue

def main():
    # initialize lists to use for random moves and for conversion from number to color
    numToColor = ["green","blue","orange" ,"red","white","yellow"]
    faces = ["front","left","right","back","top","bottom"]
    direct = ["cc","clockWise"]
    rubik = BetterCube()
    diffCopy=0
    #get the lists for the rectangles representing the specific sides
    win, lefts,fronts,rights,backs,tops,bottoms = makeWindow(rubik,numToColor)
    useRand = input("Do you want to use the random generator? ")
    if useRand=="yes" or useRand=="Yes":
        howMany = int(input("How many moves should I do? "))
        randomMoves(rubik, howMany,faces,direct,lefts,fronts,backs,rights,
                    tops,bottoms,numToColor)
        diffCopy = rubik.copy()

    # move Dets to get which move in for  "face direction"
    moveDets = Entry(Point(500,100),10)
    moveDets.draw(win)
    stop=False
    #while user has not said to close
    while stop!=True:
        p = win.getMouse()
        # inside the exit box 
        if p.getX()>50 and p.getX()<100 and p.getY()>50 and p.getX()<100:
            win.close()
            stop=True
        ### new addition
        elif p.getX()>575 and p.getX()<675 and p.getY()>50 and p.getX()<100:
            solveWithAStar(rubik)
        if stop==False:
            text = moveDets.getText()
            faceDir = text.split(" ")
            # while there is not at least one space in the text
            while len(faceDir)<2:
                win.getMouse()
                text = moveDets.getText()
                moveDets.setText("")
                faceDir = text.split(" ")
            while len(faceDir)!=2 and faceDir[0] in faces and faceDir[1] in direct:
                faceDir = text.split(" ")
            moveDets.setText("")

            rubik.move(faceDir[0],faceDir[1])
            drawCube(rubik,lefts,fronts,backs,rights,tops,bottoms,numToColor)
            #print(diffCopy.getTop()[1][1])
    #print(rubik.isSolved())

    # use setFill("Color")

def solveWithAStar(rubik):
    startNode = CubeNode(rubik,None,None,0)
    pQueue = PriorityQueue()
    pQueue.put((startNode.getScore(),startNode))
    while len(pQueue)!=0:
        curNode = 
    

    
def randomMoves(rubik, howMany,faces,direct,lefts,fronts,
                backs,rights,tops,bottoms,numToColor):
    #takes the cube, how many random moves to make all the squares to draw
    #and the color converter
    #performs howMany random moves on the cube
    #
    lastFace = ""
    lastDir =""
    for turn in range(howMany):
        #gets random face and direction
        curFace = random.choice(faces)
        curDir = random.choice(direct)
        while curFace==lastFace and curDir!=lastDir:
            #if the move it was going to do was the inverse of the last move re get random move
            curFace = random.choice(faces)
            curDir = random.choice(direct)
            
        rubik.move(curFace,curDir)
        drawCube(rubik,lefts,fronts,backs,rights,tops,bottoms,numToColor)
        print(curFace,curDir)
        #reset last moves to the move that was just done
        lastFace=curFace
        lastDir = curFace
        time.sleep(1)
        

def makeWindow(rubik, numToColor):
    #Input: the cube and a num to color converter list
    #OutPut: a win object and lists of recangles for each side
    #sideEffects: new window with rubik cube layed out in inital form
    #init
    win = GraphWin("rubik",800,600)
    #make exit button
    exitButton = Rectangle(Point(50,50),Point(100,100))
    exitText = Text(Point(75,75),"Exit")
    exitButton.draw(win)
    exitText.draw(win)

    ## add solve a* button
    aButton = Rectangle(Point(575,50),Point(675,100))
    aText = Text(Point(625,75),"Solve with A*")
    aButton.draw(win)
    aText.draw(win)
    
    colorContainers=[]
    tops = []
    bottoms= []
    #make rectangles
    #for each of the 6 sides not including top and bottom
    for side in range(4):
        for row in range(2):
            for col in range(2):
                #this is all 16 rectangles for the 4 faces
                topLeft = Rectangle(Point(150+110*side+55*col, 200+55*row),
                                    Point(200+110*side+55*col,250+55*row))
                topLeft.draw(win)
                colorContainers.append(topLeft)
                if side==1:
                    #top rectangles
                    top4= Rectangle(Point(260+55*col, 90+55*row),
                                    Point(310+55*col,140+55*row))
                    top4.draw(win)
                    #bottom rectangles
                    bottom4 = Rectangle(Point(260+55*col, 200+55*(row+2)),
                                        Point(310+55*col,250+55*(2+row)))
                    bottom4.draw(win)
                    tops.append(top4)
                    bottoms.append(bottom4)
    #divide the list into its components
    lefts = colorContainers[:4]
    fronts = colorContainers[4:8]
    rights = colorContainers[8:12]
    backs = colorContainers[12:]
    #draw the initial cube
    drawCube(rubik,lefts,fronts,backs,rights,tops,bottoms,numToColor)
    return win, lefts,fronts,rights,backs,tops,bottoms



def drawCube(rubik,lefts,fronts,backs,rights,tops,bottoms,numToColor):
    #input is the cube, Cube class object
    #output is a layed out cube GUI
    #side effect: no changes done to the model
    #example: the initailized cube will render as
    #      4 4
    #      4 4
    #2 2 0 0 3 3 1 1
    #2 2 0 0 3 3 1 1
    #      5 5
    #      5 5
    for c in range(2):
        for r in range(2):
            use = c+r
            if c==1 and r==0:
                use=2
            elif c==1 and r==1:
                use=3
                ## fill each of the quares in each face with the color corresponding in
                #the numtocolor list
            lefts[use].setFill(numToColor[rubik.getLeft()[c][r]])
            fronts[use].setFill(numToColor[rubik.getFront()[c][r]])
            rights[use].setFill(numToColor[rubik.getRight()[c][r]])
            backs[use].setFill(numToColor[rubik.getBack()[c][r]])
            tops[use].setFill(numToColor[rubik.getTop()[c][r]])
            bottoms[use].setFill(numToColor[rubik.getBottom()[c][r]])

main()
