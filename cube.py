# ---KEY---
'''
values order
L 0-7
R 8-15
B 16-23
U 24-31
D 32-39
F 40-47

Unfolded cube value indices
-- -- -- 16 17 18 -- -- --
-- -- -- 23 BB 19 -- -- --
-- -- -- 22 21 20 -- -- --
00 01 02 24 25 26 08 09 10
07 LL 03 31 UU 27 15 RR 11
06 05 04 30 29 28 14 13 12
-- -- -- 40 41 42 -- -- --
-- -- -- 47 FF 43 -- -- --
-- -- -- 46 45 44 -- -- --
-- -- -- 32 33 34 -- -- --
-- -- -- 39 DD 35 -- -- --
-- -- -- 38 37 36 -- -- --
'''

# constants to increase readability
NUM_COLORS = 8
NUM_SIDES = 6

# a cube object that stores the colors on a cube in a list with 48 elements


class Cube:
    
    sides = ("L", "R", "B", "U", "D", "F")
    edges = {"L": [24, 31, 30, 40, 47, 46, 32, 39, 38, 16, 23, 22],
             "R": [28, 27, 26, 20, 19, 18, 36, 35, 34, 44, 43, 42],
             "B": [26, 25, 24, 2, 1, 0, 38, 37, 36, 10, 9, 8],
             "U": [4, 3, 2, 22, 21, 20, 8, 15, 14, 42, 41, 40],
             "D": [0, 7, 6, 46, 45, 44, 12, 11, 10, 18, 17, 16],
             "F": [30, 29, 28, 14, 13, 12, 34, 33, 32, 6, 5, 4]}
    eLayer = [47, 43, 13, 9, 19, 23, 1, 5]      # Equatorial Layer, between U and D, reference D
    mLayer = [25, 29, 41, 45, 33, 37, 17, 21]   # Middle Layer, between R and L, reference L
    sLayer = [31, 27, 15, 11, 35, 39, 7, 3]     # Standing Layer, between F and B, reference F
    edgePieces = {"UL":(31,3), "UR":(27,15), "UB":(25,21), "UF":(29,41),
                  "FL":(47,5), "FR":(43,13), "BL":(23,1), "BR":(19,9),
                  "DL":(39,7), "DR":(35,11), "DB":(37,17), "DF":(33,45)}
    
    edgeToFrontCommand = {"L":{"BL":"L2", "DL":"L'", "UL":"L", "FL":""},
                          "R":{"UR":"R'", "FR":"", "BR":"R2", "DR":"R"},
                          "B":{"UB":"U2", "BL":"L2", "BR":"R2", "DB":"D2"},
                          "U":{"UL":"U'", "UR":"U", "UB":"U2", "UF":""},
                          "D":{"DL":"D", "DR":"D'", "DB":"D2", "DF":""},
                          "F":{"UF": "", "FL": "",  "FR": "", "DF": ""}}
    edgeToBackCommand = {"L":{"BL":"", "DL":"L", "UL":"L'", "FL":"L2"},
                         "R":{"UR":"R", "FR":"R2", "BR":"", "DR":"R'"},
                         "B":{"UB":"", "BL":"", "BR":"", "DB":""},
                         "U":{"UL":"U", "UR":"U'", "UB":"", "UF":"U2"},
                         "D":{"DL":"D'", "DR":"D", "DB":"", "DF":"D2"},
                         "F":{"UF":"U2", "FL": "L2","FR":"R2", "DF":"D2"}}
    
    cornerPieces = {"UFL":(30,40,4), "URF":(28,14,42), "UBR":(26,20,8), "ULB":(24,2,22),
                    "DLF":(32,6,46), "DFR":(34,44,12), "DBL":(38,16,0), "DRB":(36,10,18)}
    
    def __init__(self):
        self.values = [0, 0, 0, 0, 0, 0, 0, 0,
                       1, 1, 1, 1, 1, 1, 1, 1,
                       2, 2, 2, 2, 2, 2, 2, 2,
                       3, 3, 3, 3, 3, 3, 3, 3,
                       4, 4, 4, 4, 4, 4, 4, 4,
                       5, 5, 5, 5, 5, 5, 5, 5]
        self.sideToValue = {"L": 0, "R": 1, "B": 2, "U": 3, "D": 4, "F": 5}
        self.colors = {0: "r", 1: "o", 2: "y", 3: "g", 4: "b", 5: "w"}
        self.edgePiecesState = {"UL": True, "UR": True, "UB": True, "UF": True,
                           "FL": True, "FR": True, "BL": True, "BR": True,
                           "DL": True, "DR": True, "DB": True, "DF": True}
        self.edgesPerFace = {"L": 0, "R": 0, "B": 0, "U": 0, "D": 0, "F": 0}
        self.numBadEdges = 0
        self.edgesOriented = False
        self.moves = ""
        self.badEdges = []

    def set(self, values, colors):
        self.values = values
        if type(colors) != "default":
            for i in range(NUM_SIDES):
                self.colors[i] = colors[i]

    def chartString(self):
        string = ""
        for i in range(NUM_SIDES):
            side = self.sides[i]
            color = self.colors[i]

            string += f"{side} {color} \t"
            if color == "red" or color == "blue":
                string += "\t"

            for j in range(NUM_COLORS):
                value = self.values[i*NUM_COLORS + j]
                character = self.colors[value]
                string += f"{character} "
            string += "\n"

        return str(string)

    def cubeVariablesString(self):
        pass

    def unfoldedCubeString(self):
        string = ""
        file = open("unfoldedCubeKey.txt")
        content = file.readlines()
        
        SIDE_KEYWORDS = ["LL", "RR", "BB", "UU", "DD", "FF"]

        for line in content:
            values = line.split()

            for val in values:
                val = val.strip()
                if val == "--":
                    string += " "
                elif val in SIDE_KEYWORDS:
                    side = val[0]
                    sideValue = self.sideToValue[side]
                    string += self.colors[sideValue]
                else:
                    index = self.values[int(val)]
                    string += self.colors[index]
                string += " "
            string += "\n"

        return str(string)

    def __str__(self):
        string = "\n"
        # string += self.chartString()
        # string += "\n"
        string += self.unfoldedCubeString()
        return str(string)
    
    def shiftValues(self, indices, step, prime):
        pivot = step
        copyValues = self.values.copy()
        for i in range(len(indices)):
            if prime:
                oldIndex = indices[i]
                newIndex = indices[pivot]
            else:
                oldIndex = indices[pivot]
                newIndex = indices[i]
            self.values[oldIndex] = copyValues[newIndex]
            pivot = (pivot + 1) % len(indices)
    
    def shiftCenters(self, sides, prime):
        copySideToValues = self.sideToValue.copy()
        pivot = 1
        for i in range(len(sides)):
            if prime:
                old = sides[i]
                new = sides[pivot]
            else:
                old = sides[pivot]
                new = sides[i]
            self.sideToValue[old] = copySideToValues[new]
            pivot = (pivot + 1) % len(sides)
    
    def rotations(self, algorithm):
        commands = algorithm.split()
        for command in commands:
            command = command.strip()
            self.rotation(command)

    def rotation(self, command):
        #print(command, end=" ")
        self.moves += command + " "
        if len(command) == 1:
            self.rotate(command, False)
        elif len(command) == 2:
            if command[1] == "'":
                self.rotate(command[0], True)
            elif command[1] == "2":
                self.rotate(command[0], False)
                self.rotate(command[0], False)
        
        # update which edges are oriented from an F or B turn
        #if not self.edgesOriented:
            #self.updateBadEdges()

    def rotate(self, side, prime):
        if side == "x" or side == "y"or side == "z":
            self.rotateCube(side,prime)
        elif side == "M" or side == "E" or side == "S":
            self.rotateSlice(side,prime)
        else:
            self.rotateEdge(side,prime)

    def rotateSlice(self, side, prime):
        if side == "M":
            self.shiftValues(self.mLayer, 2, prime)
            sides = ["U", "F", "D", "B"]
            self.shiftCenters(sides, prime)
        elif side == "E":
            self.shiftValues(self.eLayer, 2, prime)
            sides = ["L", "F", "R", "B"]
            self.shiftCenters(sides, prime)
        elif side == "S":
            self.shiftValues(self.sLayer, 2, prime)
            sides = ["U", "R", "D", "L"]
            self.shiftCenters(sides, prime)
        else:
            print("Input error with self.rotateSlice({}, {}). Expected M, E or S".format(side,prime))

    def rotateCube(self, side, prime):
        if side == "x":
            self.rotateSlice("M", not prime)
            self.rotateEdge("L",not prime)
            self.rotateEdge("R",prime)
        elif side == "y":
            self.rotateSlice("E", not prime)
            self.rotateEdge("D", not prime)
            self.rotateEdge("U", prime)
        elif side == "z":
            self.rotateSlice("S", prime)
            self.rotateEdge("B", not prime)
            self.rotateEdge("F", prime)
        else:
            print("Input error with self.rotateCube({}, {}). Expected x, y or z".format(side,prime))

    def rotateEdge(self, side, prime):
        # rotate face
        start = self.sideToValue[side]*NUM_COLORS
        indices = [start+i for i in range(NUM_COLORS)]
        self.shiftValues(indices, 2, prime)
            
        # rotate edges touching the face
        indices = self.edges[side].copy()
        self.shiftValues(indices, 3, prime)
            
    def checkerBoard(self):
        self.rotation("R2")
        self.rotation("L2")
        self.rotation("F2")
        self.rotation("B2")
        self.rotation("U2")
        self.rotation("D2")
        
    def colorAt(self, index):
        return self.values[index]
    
    def getValues(self):
        return self.values
    
    def getColorsOrder(self):
        return self.colors
    
    def oppositeSide(self, referenceSide):
        if referenceSide == "L":
            return "R"
        elif referenceSide == "R":
            return "L"
        elif referenceSide == "D":
            return "U"
        elif referenceSide == "U":
            return "D"
        elif referenceSide == "F":
            return "B"
        elif referenceSide == "B":
            return "F"
        
    '''
    edgePieces = {"UL":(31,3), "UR":(27,15), "UB":(25,21), "UF":(29,41),
                "FL":(47,5), "FR":(43,13), "BL":(23,1), "BR":(19,9),
                "DL":(39,7), "DR":(35,11), "DB":(37,17), "DF":(33,45)}
    '''
    def updateBadEdges(self):
        total = 0
        lColor = self.sideToValue["L"]
        rColor = self.sideToValue["R"]
        uColor = self.sideToValue["U"]
        dColor = self.sideToValue["D"]
        fColor = self.sideToValue["F"]
        bColor = self.sideToValue["B"]
        
        self.badEdges.clear()
        
        for edge in self.edgesPerFace:
            self.edgesPerFace[edge] = 0
        
        for edge in self.edgePieces:
            
            self.edgePiecesState[edge] = True
            
            indices = self.edgePieces[edge]
            initialColor = self.values[indices[0]]
            secondColor = self.values[indices[1]]
            
            if initialColor == lColor or initialColor == rColor:
                total += 1
                self.edgePiecesState[edge] = False
                self.badEdges.append(edge)
                self.edgesPerFace[edge[0]] += 1
                self.edgesPerFace[edge[1]] += 1
            if initialColor == fColor or initialColor == bColor:
                if secondColor == uColor or secondColor == dColor:
                    total += 1
                    self.edgePiecesState[edge] = False
                    self.badEdges.append(edge)
                    self.edgesPerFace[edge[0]] += 1
                    self.edgesPerFace[edge[1]] += 1

        self.numBadEdges = total
        return total
    
    def isFrontOrBack(self, face):
        return (face == "F" or face == "B")
    
    def isOriented(self, edge):
        return self.edgePiecesState[edge]
    
    # sets L,R,U, or D faces to front. Ignores B
    def setToFront(self, face):
        if face == "L":
            self.rotation("y'")
        elif face == "R":
            self.rotation("y")
        elif face == "U":
            self.rotation("x'")
        elif face == "D":
            self.rotation("x")
            
    def edgeOrientationAlgorithm(self, primaryFace, faceEdges, frontCondition, numbersOnFace):
        for faceEdge in faceEdges:
            side = ""
            if faceEdge[0] == primaryFace:
                side = faceEdge[1]
            else:
                side = faceEdge[0]

            if self.isOriented(faceEdge) == frontCondition and self.edgesPerFace[side] == numbersOnFace:
                edge = ""
                for e in self.badEdges:
                    if side in e and primaryFace not in e:
                        edge = e
                if primaryFace == "F":
                    command = self.edgeToFrontCommand[side][edge]
                    if numbersOnFace == 2 and "2" in command:
                        command = command[0]
                    self.rotation(command)
                    return True
                if primaryFace == "B":
                    command = self.edgeToBackCommand[side][edge]
                    if numbersOnFace == 2 and "2" in command:
                        command = command[0]
                    self.rotation(command)
                    return True
                
        return False
    
    def moveOrientedToFront(self, primaryFace, faceEdges):
        for edge in faceEdges:
            side = ""
            if edge[0] == primaryFace:
                side = edge[1]
            else:
                side = edge[0]

            if self.edgesPerFace[side] < 4:
                sideEdges = []
                for e in self.edgePieces:
                    if side in e:
                        sideEdges.append(e)
                
                for e in sideEdges:
                    if self.edgePiecesState[e] == True:
                        if primaryFace == "F":
                            command = self.edgeToFrontCommand[side][e]
                        else:
                            command = self.edgeToBackCommand[side][e]
                        self.rotation(command)
                        return True
                    
        return False
                
    def specialCase(self, primaryFace, faceEdges):
        emptyFaceEdge = ""
        emptyFaceSide = ""
        if self.edgesPerFace[primaryFace] == 3:
            for edge in faceEdges:
                if self.edgePiecesState[edge] == True:
                    emptyFaceEdge = edge
                    break
                    
            if emptyFaceEdge[0] == primaryFace:
                emptyFaceSide = emptyFaceEdge[1]
            else:
                emptyFaceSide = emptyFaceEdge[0]
                
            if self.edgesPerFace[emptyFaceSide] == 0:
                oppositeSide = self.oppositeSide(emptyFaceSide)
                if self.edgesPerFace[oppositeSide] == 2:
                    return True
                
        return False
    
    def twoEdgeOrientation(self):
                
        if self.edgesPerFace["F"] == 1:
            self.rotation("F")
        elif self.edgesPerFace["B"] == 1:
            self.rotation("B")
        else:
            for face in self.edgesPerFace:
                if self.edgesPerFace[face] == 1:
                    self.rotation(face)
                    return self.orientEdges()
                    
        return self.orientEdges()
    
    def fourEdgeOrientation(self):
        
        primaryFace = "F"
        if self.edgesPerFace["B"] > self.edgesPerFace["F"]:
            primaryFace = "B"

        numEdgesPerSides = []
        for edge in self.edgesPerFace:
            if edge != "F" and edge != "B":
                numEdgesPerSides.append(self.edgesPerFace[edge])

        faceEdges = []
        for edge in self.edgePiecesState:
            if primaryFace in edge:
                faceEdges.append(edge)
        
        # base case where all edges are in the front
        if self.edgesPerFace[primaryFace] == 4:
            self.rotation(primaryFace)
            return self.orientEdges()
        
        # special case where three in front and the fourth isn't in the open layer
        if self.specialCase(primaryFace, faceEdges):
            self.rotation(primaryFace + "2")
            return self.orientEdges()
        
        # algorithm that handles all cases or puts it to the special case
        if self.edgeOrientationAlgorithm(primaryFace, faceEdges, True, 1):
            return self.orientEdges()
        elif self.edgeOrientationAlgorithm(primaryFace, faceEdges, True, 2):
            return self.orientEdges()
        elif self.edgeOrientationAlgorithm(primaryFace, faceEdges, True, 3):
            return self.orientEdges()
        elif self.edgeOrientationAlgorithm(primaryFace, faceEdges, False, 2):
            return self.orientEdges()
        elif self.edgeOrientationAlgorithm(primaryFace, faceEdges, False, 3):
            return self.orientEdges()
        else:
            return self.orientEdges()
    
    def sixEdgeOrientation(self):
        
        primaryFace = "F"
        if self.edgesPerFace["B"] > self.edgesPerFace["F"]:
            primaryFace = "B"

        faceEdges = []
        for edge in self.edgePiecesState:
            if primaryFace in edge:
                faceEdges.append(edge)
                
        if self.edgesPerFace[primaryFace] == 3:
            self.rotation(primaryFace)
            return self.orientEdges()
        elif self.edgesPerFace[primaryFace] < 3:
            if self.edgeOrientationAlgorithm(primaryFace, faceEdges, True, 1):
                return self.orientEdges()
            elif self.edgeOrientationAlgorithm(primaryFace, faceEdges, True, 2):
                return self.orientEdges()
            elif self.edgeOrientationAlgorithm(primaryFace, faceEdges, True, 3):
                return self.orientEdges()
            elif self.edgeOrientationAlgorithm(primaryFace, faceEdges, False, 2):
                return self.orientEdges()
            elif self.edgeOrientationAlgorithm(primaryFace, faceEdges, False, 3):
                return self.orientEdges()
            else:
                return self.orientEdges()
        elif self.moveOrientedToFront(primaryFace, faceEdges):
            return self.orientEdges()
        else:
            print("There was an error in the sixEdgeOrientationAlgorithm")
            return False
    
    def tenEdgeOrientation(self):
        frontOriented = (self.edgesPerFace["F"] == 4)
        backOriented = (self.edgesPerFace["B"] == 4)
        if frontOriented and backOriented:
            self.rotation("F")
            self.rotation("B")
            return self.orientEdges()
        else:
            return self.fourEdgeOrientation()
    
    def twelveEdgeOrientation(self):
        self.rotation("F")
        self.rotation("B")
        return self.orientEdges()
    
    def orientEdges(self):
        self.updateBadEdges()
        
        if self.numBadEdges == 0:
            self.edgesOriented = True
            return True
        elif self.numBadEdges == 2:
            return self.twoEdgeOrientation()
        elif self.numBadEdges == 4:
            return self.fourEdgeOrientation()
        elif self.numBadEdges == 6:
            return self.sixEdgeOrientation()
        elif self.numBadEdges == 8:
            return self.fourEdgeOrientation()
        elif self.numBadEdges == 10:
            return self.fourEdgeOrientation()
        elif self.numBadEdges == 12:
            return self.fourEdgeOrientation()
        
    def solution(self):
        self.moves = ""
        self.orientEdges()
        return self.moves
        
            
