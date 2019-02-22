#Caleb Vanorio
#Cube Node
# this is designed to be the Nodes that we will use for the tree search A*

class CubeNode:
    def __init__(cube,theParent,theAction,costFromStart):
        self.__curState = cube
        self.__parent = theParent
        self.__actionToCur = theAction
        self.__pathCost = costFromStart
        if theAction!=None:
            self.__splitMove = actionToCur.split(" ")
            #each component of the move, face and direction
            #does the action to make it into the new current state
            self.__curState.move(splitMove[0],splitMove[1])
        self.__heuristic = heurFunc(curState)
        self.__score = self.__heuristic+pathCost
    def getCurState(self):
        return self.__curState
    def getParent(self):
        return self.__parent
    def getActionToCur(self):
        return self.__actionToCur
    def getPathCost(self):
        return self.__pathCost
    def getScore(self):
        return self.__score()

    def heurFunc(rubik):
        #This is the heuristic evaluator for each state
        #Input: the cube to be evaluated
        #output: the heuristic based on the number of spots out of place
        wrongSpots=0
        for side in range(6):
            faces = rubik.getFaces()
            curFace = faces[side]
            curCount = dict()
            for row in range(2):
                for col in range(2):
                    if curFace[row][col] in curCount:
                        curCount[curFace[row][col]] +=1
                    else:
                        curCount[curFace[row][col]] = 1
                        
            mostSpaces=0    
            for key in curCount.keys():
                if curCount[key]>mostSpaces:
                    mostSpaces = curCount[key]

            wrongSpots+=4-mostSpaces

        heur = wrongSpots//8
        return heur
                
                                 
                                
                    




                        
                    
