#Caleb Vanorio
#CSC 339
# cube lab
# cube class
from graphics import *
import math
import random
class Cube:
    def __init__(self):
        self.__front =[[4,2],[5,0]]# [[0,0],[0,0]]#white
        self.__back = [[5,2],[2,3]] #[[1,1],[1,1]]#blue
        self.__left = [[5,1],[0,1]] #[[2,2],[2,2]]#red
        self.__right= [[4,1],[3,0]] #[[3,3],[3,3]]#green
        self.__top = [[0,2],[3,1]]#[[4,4],[4,4]]#yellow
        self.__bottom = [[3,5],[4,4]]  #[[5,5],[5,5]]#orange
        self.__faces=[self.__front, self.__right, self.__back, self.__left, self.__top, self.__bottom]

    #in order left right for each side front, right, back, left
        self.__topBottomGetTos=[[ [1,0],[1,1]] , [[1,1],[0,1]] , [[0,1],[0,0]] , [[0,0],[1,0]],\
                                [[0,0],[0,1],[[1,0],[1,1]]]
        self.__bottomGetTos = [[ [0,0],[0,1]],[[0,1],[1,1]],[[1,1],[1,0]],[[1,0],[0,0]]]

        
        self.__frontRel = [self.__right, self.__top, self.__left, self.__bottom]
        self.__rightRel =[self.__back, self.__top, self.__front, self.__bottom] 
        self.__leftRel = [self.__front, self.__top, self.__back, self.__bottom]
        self.__backRel = [self.__left, self.__top, self.__right, self.__bottom]
        self.__topRel = [self.__right, self.__back, self.__left, self.__front]
        self.__bottomRel = [self.__right, self.__front, self.__left, self.__back]

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


    def isSolved(self):
        #input: None
        #output: bolean
        #side effects: none
        #if same as initialized returns true
        solved=True
        for face in self.__faces:
            for row in face:
                for col in row:
                    if face[0][0]==face[row][col]:
                        solved=False

        return solved

    def drawIt(self,win):
        #input none
        #output GUI representation of cube
        #side effect: no changes made to cube
        pass


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
        self.rotation(faceUsing, direction)
        self.rotateNonFace(face, faceUsing, direction,relation)
        print(self.__top)
        print(self.__left, self.__front, self.__right,self.__back)
        print(self.__bottom)
        



    def rotateNonFace(self, face, faceUsing, direction,relation):
        #input: face that is being rotated, array
        # direction that the rotation is, string
        #output: none
        # side effect:  is the rotation of those pieces that rotate but arent part of the face
        # "front cc" would rotate the top, bottom, right, and left pieces that are touching the
        #front to rotate counter clockwise
        # encapsulate which side it actually is
        right=relation[0]
        top = relation[1]
        left= relation[2]
        bottom = relation[3]
        ## inits
        topLeft =0
        topRight =0 
        rightTop=0
        rightBottom=0
        leftTop=0
        leftBottom=0
        bottomLeft=0
        bottomRight=0
        if face!="top" and face!="bottom":
            whichTopTags = self.__topBottomGetTos[self.__faces.index(faceUsing)]
            whichBottomTags = self.__bottomGetTos[(self.__faces.index(faceUsing))]
            #if it is not the top or bottom piece
            #whichTopTags allows you to know which indexies for the top and bottom
            #should be used based on the face you are rotating
            topLeft = top[whichTopTags[0][0]][whichTopTags[0][1]]
            topRight = top[whichTopTags[1][0]][whichTopTags[1][1]]
            rightTop =right[0][0]
            rightBottom = right[1][0]
            leftTop = left[0][1]
            leftBottom = left[1][1]
            bottomLeft = bottom[whichBottomTags[0][0]][whichBottomTags[0][1]]
            print("bottom left  "+str(bottomLeft))
            bottomRight = bottom[whichBottomTags[1][0]][whichBottomTags[1][1]]
            print("bottom right  "+str(bottomRight))

        elif face=="top":
            #if top all the other side indecies are the top two
            topLeft = top[0][1]
            topRight = top[0][0]
            rightTop =right[0][1]
            rightBottom = right[0][0]
            leftTop = left[0][0]
            leftBottom = left[0][1]
            bottomLeft = bottom[0][0]
            bottomRight = bottom[0][1]
        elif face=="bottom":
             #to the bottom everything is the bottom 2 of the left right front and back
             # then for some you have to invert the right from the left
            topLeft = top[1][0]
            topRight = top[1][1]
            rightTop =right[1][0]
            rightBottom = right[1][1]
            leftTop = left[1][1]
            leftBottom = left[1][0]
            bottomLeft = bottom[1][1]
            bottomRight = bottom[1][0]
        else:
            print("wrong face")
        if direction=="clockWise":
             ## with the 4 other sides left right top and bottom always being the same
             ## you can encapsulate which side is actually each side
             ## then these relations exist for clockwise
            if face!="top" and face!="bottom":
                top[whichTopTags[0][0]][whichTopTags[0][1]] = leftBottom
                top[whichTopTags[1][0]][whichTopTags[1][1]] = leftTop
                right[0][0] = topLeft
                right[1][0] = topRight
                bottom[whichBottomTags[0][0]][whichBottomTags[0][1]] = rightBottom
                bottom[whichBottomTags[1][0]][whichBottomTags[1][1]] = rightTop
                left[0][1] = bottomLeft
                left[1][1] = bottomRight
                #print(self.__front)
                #print(self.__right)
                #print(self.__top)
            elif face=="bottom":
                #bottom ones
                top[1][0] = leftBottom
                top[1][1] = leftTop
                right[1][0] = topLeft
                right[1][1] = topRight
                bottom[1][1] = rightBottom
                bottom[1][0] = rightTop
                left[1][1] = bottomLeft
                left[1][0] = bottomRight
            elif face=="top":
                ##### fix here
                top[0][1] = leftBottom
                top[0][0] = leftTop
                right[0][1] = topLeft
                right[0][0] = topRight
                bottom[0][0] = rightBottom
                bottom[0][1] = rightTop
                left[0][0] = bottomLeft
                left[0][1] = bottomRight

        elif direction=="cc":
            if face!="bottom" and face!="top":
             # and these exist for counterclockwise
                top[whichTopTags[0][0]][whichTopTags[0][1]] = rightTop
                top[whichTopTags[1][0]][whichTopTags[1][1]] = rightBottom
                right[0][0] = bottomRight
                right[1][0] = bottomLeft
                bottom[whichTopTags[1][0]][whichTopTags[1][1]] = leftTop
                bottom[whichTopTags[0][0]][whichTopTags[0][1]] = leftBottom
                left[0][1] = topRight
                left[1][1] = topLeft
            elif face=="bottom":
                #bottom ones
                top[1][0] = rightTop 
                top[1][1] = rightBottom 
                right[1][0] = bottomRight
                right[1][1] = bottomLeft
                bottom[1][1] = leftTop
                bottom[1][0] = leftBottom
                left[1][1] = topRight 
                left[1][0] = topLeft 
            elif face=="top":
                ##### fix here
                top[0][1] = rightTop
                top[0][0] = rightBottom
                right[0][1] = bottomRight
                right[0][0] = bottomLeft 
                bottom[0][0] = leftTop 
                bottom[0][1] = leftBottom 
                left[0][0] = topRight
                left[0][1] = topLeft 
        else:
            print("wrong direction")
        
         

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
        copy =[[10,10],[10,10]]
        for ind in range(len(faceArray)):
            for md in range(len(faceArray[0])):
                print(ind,md)
                copy[ind][md]=faceArray[ind][md]
        return copy
                           
