#Caleb Vanorio
#CSC 339
# cube lab
# cube class
'''  This is the Cube class for modeling the Rubik's cube.
methods:
init: make standard cube
getters for 6 faces: get the 6 faces
isSolved: is it in a goal state
reset: set it back to the initial cube
move: determine face and direction
rotation: rotate the specific face
rotateNonFace: rotate the pieces not on the face that moves
makeCopy: copy lists so that they are independent'''



from graphics import *
import math
import random
class BetterCube:
    def __init__(self):
        self.__front = [[0,0],[0,0]]#white  [[4,2],[5,0]]
        self.__back = [[1,1],[1,1]]#blue [[5,2],[2,3]] #
        self.__left = [[2,2],[2,2]]#red [[5,1],[0,1]] #
        self.__right= [[3,3],[3,3]]#green [[4,1],[3,0]] #
        self.__top = [[4,4],[4,4]]#yellow  [[0,2],[3,1]]#
        self.__bottom = [[5,5],[5,5]]#orange [[3,5],[4,4]]  #
        # the 6 faces
        self.__faces=[self.__front, self.__right, self.__back, self.__left, self.__top, self.__bottom]

    #in order left right for each side front, right, back, left
        self.__topGetTos=[[ [1,0],[1,1] ] , [ [1,1],[0,1]] , [[0,1],[0,0]] , [[0,0],[1,0]] ,  [[0,1],[0,0]] , [[1,0],[1,1]]]
        self.__bottomGetTos = [[ [0,0],[0,1]],[[0,1],[1,1]],[[1,1],[1,0]],[[1,0],[0,0]],[[0,0],[0,1]],[[1,1],[1,0]]]
        #top  then bottom
        self.__rightGetTos = [ [ [0,0],[1,0]], [ [0,0],[1,0]], [ [0,0],[1,0]], [ [0,0],[1,0]], [ [0,1],[0,0]],[ [1,0],[1,1]]]
        self.__leftGetTos = [[ [0,1],[1,1]], [[0,1],[1,1]], [[0,1],[1,1]], [[0,1],[1,1]], [ [0,0],[0,1]], [ [1,1],[1,0]]]

        #for each face the relations in order of what is to the right, top,left and bottom
        self.__frontRel = [self.__right, self.__top, self.__left, self.__bottom]
        self.__rightRel =[self.__back, self.__top, self.__front, self.__bottom]
        self.__leftRel = [self.__front, self.__top, self.__back, self.__bottom]
        self.__backRel = [self.__left, self.__top, self.__right, self.__bottom]
        self.__topRel = [self.__right, self.__back, self.__left, self.__front]
        self.__bottomRel = [self.__right, self.__front, self.__left, self.__back]

        #getters for manipulation in cubeGUI
    def getFront(self):
        return self.__front
    def getBack(self):
        return self.__back
    def getLeft(self):
        return self.__left
    def getRight(self):
        return self.__right
    def getTop(self):
        return self.__top
    def getBottom(self):
        return self.__bottom

    def getFaces(self):
        return self.__faces

    def copy(self):
        #input: the cube you wish to solve, BetterCube object
        #output: a deepcopy of the cube
        # makes new cube then modifies each sticker so that it matches the cube in its correct state
        newCube = BetterCube()
        for side in range(6):
            curNewFace = newCube.getFaces()[side]
            curOldFace = self.__faces[side]
            for row in range(2):
                for col in range(2):
                    curNewFace[row][col] = curOldFace[row][col]
        return newCube

    # boolean solved if all faces on each side are the same, doesnt care
    #which side the faces are all the same
    def isSolved(self):
        #input: None
        #output: bolean
        #side effects: none
        #if same as initialized returns true
        solved=True
        #init true
        for face in self.__faces:
            for row in range(2):
                for col in range(2):
                    if face[0][0]!=face[row][col]:
                        #if ever it finds a place where it doesnt match: false
                        solved=False
        return solved


    def reset(self):
        #input: none
        #output: none
        #side effect: all the moves that had been made are deleted
        self.__front = [[0,0],[0,0]]#white
        self.__back = [[1,1],[1,1]]#blue
        self.__left = [[2,2],[2,2]]#red
        self.__right= [[3,3],[3,3]]#green
        self.__top = [[4,4],[4,4]]#yellow
        self.__bottom = [[5,5],[5,5]]#orange


    ### For each move you need to know the face, the move direction
    ### and the tuple or if rotation
    ## based on the arguments given at the line
    ## make the move and update new positions of squares
    def move(self, face, direction):
        #input: the face you wish to move, string
        #the direction you wish to rotate, string
        #output: none
        #side effect: the rotated cube with updated representation in GUI
        faceUsing=0
        relation=0
        ### determine face to set as main one moving
        if face=="front":
            faceUsing = self.__front
            relation=self.__frontRel
        elif face=="back":
            faceUsing = self.__back
            relation=self.__backRel
        elif face=="left":
            faceUsing = self.__left
            relation=self.__leftRel
        elif face=="right":
            faceUsing = self.__right
            relation=self.__rightRel
        elif face=="top":
            faceUsing = self.__top
            relation=self.__topRel
        elif face=="bottom":
            faceUsing = self.__bottom
            relation=self.__bottomRel
        #rotate main face
        self.rotation(faceUsing, direction)
        #rotate the other pieces
        self.rotateNonFace(face, faceUsing, direction,relation)

##        print(self.__top)
##        print(self.__left, self.__front, self.__right,self.__back)
##        print(self.__bottom)




    def rotateNonFace(self, face, faceUsing, direction,relation):
        #input: face that is being rotated, array
        # direction that the rotation is, string
        #output: none
        # side effect:  is the rotation of those pieces that rotate but arent part of the face
        # "front cc" would rotate the top, bottom, right, and left pieces that are touching the
        #front to rotate counter clockwise
        #      1 1                                  1 1
        #      1 1                                  4 4
        #2 2 3 3 4 4       ===>    2 1 3 3 5 4
        #2 2 3 3 4 4                      2 1 3 3 5 4
        #      5 5                                  2 2
        #      5 5                                  5 5

        # encapsulate which side it actually is
        right=relation[0]
        top = relation[1]
        left= relation[2]
        bottom = relation[3]

        #determine for that face which indecies to use for the 4 relations
        whichTopTags = self.__topGetTos[self.__faces.index(faceUsing)]
        whichBottomTags = self.__bottomGetTos[(self.__faces.index(faceUsing))]
        whichRightTags = self.__rightGetTos[self.__faces.index(faceUsing)]
        whichLeftTags = self.__leftGetTos[(self.__faces.index(faceUsing))]

        #get the 8 sides
        topLeft = top[whichTopTags[0][0]][whichTopTags[0][1]]
        topRight = top[whichTopTags[1][0]][whichTopTags[1][1]]
        rightTop =right[whichRightTags[0][0]][whichRightTags[0][1]]
        rightBottom = right[whichRightTags[1][0]][whichRightTags[1][1]]
        leftTop = left[whichLeftTags[0][0]][whichLeftTags[0][1]]
        leftBottom = left[whichLeftTags[1][0]][whichLeftTags[1][1]]
        bottomLeft = bottom[whichBottomTags[0][0]][whichBottomTags[0][1]]
        bottomRight = bottom[whichBottomTags[1][0]][whichBottomTags[1][1]]

        if direction=="clockWise":
             ## with the 4 other sides left right top and bottom always being the same
             ## you can encapsulate which side is actually each side
             ## then these relations exist for clockwise
            top[whichTopTags[0][0]][whichTopTags[0][1]] = leftBottom #topLeft
            top[whichTopTags[1][0]][whichTopTags[1][1]] = leftTop #topRight
            right[whichRightTags[0][0]][whichRightTags[0][1]] = topLeft#rightTop
            right[whichRightTags[1][0]][whichRightTags[1][1]] = topRight#rightBottom
            bottom[whichBottomTags[0][0]][whichBottomTags[0][1]] = rightBottom #bottomLeft
            bottom[whichBottomTags[1][0]][whichBottomTags[1][1]] = rightTop #bottomRight
            left[whichLeftTags[0][0]][whichLeftTags[0][1]] = bottomLeft#leftTop
            left[whichLeftTags[1][0]][whichLeftTags[1][1]] = bottomRight#leftBottom

        elif direction=="cc":
            #same as clockWise except that you assign everything to its inverse
            # if it was for topRight its now bottomLeft
            top[whichTopTags[0][0]][whichTopTags[0][1]] = rightTop #topLeft
            top[whichTopTags[1][0]][whichTopTags[1][1]] = rightBottom #topRight
            right[whichRightTags[0][0]][whichRightTags[0][1]] = bottomRight#rightTop
            right[whichRightTags[1][0]][whichRightTags[1][1]] = bottomLeft#rightBottom
            bottom[whichBottomTags[0][0]][whichBottomTags[0][1]] = leftTop  #bottomLeft
            bottom[whichBottomTags[1][0]][whichBottomTags[1][1]] = leftBottom  #bottomRight
            left[whichLeftTags[0][0]][whichLeftTags[0][1]] = topRight #leftTop
            left[whichLeftTags[1][0]][whichLeftTags[1][1]] = topLeft #leftBottom


    def rotation(self, face, direction):
        # input is the face to rotate, array
        # direction is direction of rotation, string
        # output: none
        # side effect: rotates the face in the model
        # "front cc" would rotate the front counter clockwise
        if direction=="clockWise":
            tempArray = self.makeCopy(face)
            #print(tempArray)
            #print(face)
            #the positions after the rotation
            face[0][0]=tempArray[1][0]
            face[0][1]=tempArray[0][0]
            face[1][0]=tempArray[1][1]
            face[1][1]=tempArray[0][1]

        elif direction=="cc": #counter clockwise
            tempArray = self.makeCopy(face)
            face[0][0]=tempArray[0][1]
            face[0][1]=tempArray[1][1]
            face[1][0]=tempArray[0][0]
            face[1][1]=tempArray[1][0]


    def makeCopy(self, faceArray):
        #Input: array to make a independent copy of
        #output: copy of array
        #
        copy =[[10,10],[10,10]]
        for ind in range(len(faceArray)):
            for md in range(len(faceArray[0])):
                copy[ind][md]=faceArray[ind][md]
        return copy
