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


NUM_SIDE_PIECES = 8
NUM_SIDES = 6

CORRECT = 0
CLOCKWISE = 1
COUNTER_CLOCKWISE = -1
WRONG_POSITION = 2

CRISS_CROSS = 8
ZIGZAG = 7

NORMAL = 0
PRIME = 1
DOUBLE = 2

ERROR = 666

# a cube object that stores the colors on a cube in a list with 48 elements


class Cube:

    sides = ("L", "R", "B", "U", "D", "F")
    edges = {"L": [24, 31, 30, 40, 47, 46, 32, 39, 38, 16, 23, 22],
             "R": [28, 27, 26, 20, 19, 18, 36, 35, 34, 44, 43, 42],
             "B": [26, 25, 24, 2, 1, 0, 38, 37, 36, 10, 9, 8],
             "U": [4, 3, 2, 22, 21, 20, 8, 15, 14, 42, 41, 40],
             "D": [0, 7, 6, 46, 45, 44, 12, 11, 10, 18, 17, 16],
             "F": [30, 29, 28, 14, 13, 12, 34, 33, 32, 6, 5, 4]}
    faceStartIndex = {"L": 0, "R": 8, "B": 16, "U": 24, "D": 32, "F": 40}
    # Equatorial Layer, between U and D, reference D
    eLayer = [47, 43, 13, 9, 19, 23, 1, 5]
    # Middle Layer, between R and L, reference L
    mLayer = [25, 29, 41, 45, 33, 37, 17, 21]
    # Standing Layer, between F and B, reference F
    sLayer = [31, 27, 15, 11, 35, 39, 7, 3]
    edgePieces = {"UL": (31, 3), "UR": (27, 15), "UB": (25, 21), "UF": (29, 41),
                  "FL": (47, 5), "FR": (43, 13), "BL": (23, 1), "BR": (19, 9),
                  "DL": (39, 7), "DR": (35, 11), "DB": (37, 17), "DF": (33, 45)}

    # [toFace][fromFace][edgeLabel] => command
    edgeToFaceCommand = {"L": {"L": {"BL": "", "DL": "", "UL": "", "FL": ""},
                               "R": {"UR": "U2", "FR": "F2", "BR": "B2", "DR": "D2"},
                               "B": {"UB": "B", "BL": "", "BR": "B2", "DB": "B'"},
                               "U": {"UL": "", "UR": "U2", "UB": "U'", "UF": "U"},
                               "D": {"DL": "", "DR": "D2", "DB": "D", "DF": "D'"},
                               "F": {"UF": "F'", "FL": "", "FR": "F2", "DF": "F"}},
                         "R": {"L": {"BL": "B2", "DL": "D2", "UL": "U2", "FL": "F2"},
                               "R": {"UR": "", "FR": "", "BR": "", "DR": ""},
                               "B": {"UB": "B'", "BL": "B2", "BR": "", "DB": "B"},
                               "U": {"UL": "U2", "UR": "", "UB": "U", "UF": "U'"},
                               "D": {"DL": "D2", "DR": "", "DB": "D'", "DF": "D"},
                               "F": {"UF": "F", "FL": "F2", "FR": "", "DF": "F'"}},
                         "B": {"L": {"BL": "", "DL": "L", "UL": "L'", "FL": "L2"},
                               "R": {"UR": "R", "FR": "R2", "BR": "", "DR": "R'"},
                               "B": {"UB": "", "BL": "", "BR": "", "DB": ""},
                               "U": {"UL": "U", "UR": "U'", "UB": "", "UF": "U2"},
                               "D": {"DL": "D'", "DR": "D", "DB": "", "DF": "D2"},
                               "F": {"UF": "U2", "FL": "L2", "FR": "R2", "DF": "D2"}},
                         "U": {"L": {"BL": "L", "DL": "L2", "UL": "", "FL": "L'"},
                               "R": {"UR": "", "FR": "R", "BR": "R'", "DR": "R2"},
                               "B": {"UB": "", "BL": "B'", "BR": "B", "DB": "B2"},
                               "U": {"UL": "", "UR": "", "UB": "", "UF": ""},
                               "D": {"DL": "L2", "DR": "R2", "DB": "B2", "DF": "F2"},
                               "F": {"UF": "", "FL": "F", "FR": "F'", "DF": "F2"}},
                         "D": {"L": {"BL": "L'", "DL": "", "UL": "L2", "FL": "L"},
                               "R": {"UR": "R2", "FR": "R'", "BR": "R", "DR": ""},
                               "B": {"UB": "B2", "BL": "L'", "BR": "R", "DB": ""},
                               "U": {"UL": "L2", "UR": "R2", "UB": "B2", "UF": "F2"},
                               "D": {"DL": "", "DR": "", "DB": "", "DF": ""},
                               "F": {"UF": "F2", "FL": "L", "FR": "R'", "DF": ""}},
                         "F": {"L": {"BL": "L2", "DL": "L'", "UL": "L", "FL": ""},
                               "R": {"UR": "R'", "FR": "", "BR": "R2", "DR": "R"},
                               "B": {"UB": "U2", "BL": "L2", "BR": "R2", "DB": "D2"},
                               "U": {"UL": "U'", "UR": "U", "UB": "U2", "UF": ""},
                               "D": {"DL": "D", "DR": "D'", "DB": "D2", "DF": ""},
                               "F": {"UF": "", "FL": "",  "FR": "", "DF": ""}}}

    cornerPieces = {"UFL": (30, 40, 4), "URF": (28, 14, 42), "UBR": (26, 20, 8), "ULB": (24, 2, 22),
                    "DLF": (32, 6, 46), "DFR": (34, 44, 12), "DBL": (38, 16, 0), "DRB": (36, 10, 18)}

    movements = {"L": "UFDB", "R": "FUBD", "B": "RULD",
                 "U": "FLBR", "D": "LFRB", "F": "LURD"}

    cubies = ["UFL", "URF", "UBR", "ULB", "DLF", "DFR", "DBL", "DRB",
              "UL", "UR", "UB", "UF", "FL", "FR", "BL", "BR", "DL", "DR", "DB", "DF"]

    # [faceThatGetsTurned][faceThatGetsChange][newFaceName]
    # newFaceName = "{nameIfClockwiseRotation}{nameIfCounterClockwiseRotation}{nameIfDoubleRotation}"
    faceOrder = {"L": {"F": "UBD", "U": "BDF", "B": "DFU", "D": "FUB"},
                 "R": {"F": "DBU", "D": "BUF", "B": "UFD", "U": "FDB"},
                 "B": {"D": "LUR", "L": "URD", "U": "RDL", "R": "DLU"},
                 "U": {"F": "RBL", "R": "BLF", "B": "LFR", "L": "FRB"},
                 "D": {"F": "LBR", "L": "BRF", "B": "RFL", "R": "FLB"},
                 "F": {"R": "ULD", "U": "LDR", "L": "DRU", "D": "RUL"}}

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
        self.leftCubies = []
        self.rightCubies = []
        self.upCubies = []
        self.possibilities = []
        self.visitedCorners = []

    def set(self, values, colors):
        self.values = values
        if type(colors) != "default":
            for i in range(NUM_SIDES):
                self.colors[i] = colors[i]

    def isSolved(self):
        start = 0
        end = 8
        for face in self.faceStartIndex:
            subList = self.values.copy()[start:end]

            if (len(set(subList)) != 1) or (subList[0] != self.sideToValue[face]):
                return False
            start += 8
            end += 8

        return True

    def chartString(self):
        string = ""
        for i in range(NUM_SIDES):
            side = self.sides[i]
            color = self.colors[i]

            string += f"{side} {color} \t"
            if color == "red" or color == "blue":
                string += "\t"

            for j in range(NUM_SIDE_PIECES):
                value = self.values[i*NUM_SIDE_PIECES + j]
                character = self.colors[value]
                string += f"{character} "
            string += "\n"

        return str(string)

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

    def rotation(self, command:str):
        command = command.strip()
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
        # if not self.edgesOriented:
            # self.updateBadEdges()

    def rotate(self, side, prime):
        if side == "x" or side == "y" or side == "z":
            self.rotateCube(side, prime)
        elif side == "M" or side == "E" or side == "S":
            self.rotateSlice(side, prime)
        else:
            self.rotateEdge(side, prime)

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
            print("Input error with self.rotateSlice({}, {}). Expected M, E or S".format(
                side, prime))

    def rotateCube(self, side, prime):
        if side == "x":
            self.rotateSlice("M", not prime)
            self.rotateEdge("L", not prime)
            self.rotateEdge("R", prime)
        elif side == "y":
            self.rotateSlice("E", not prime)
            self.rotateEdge("D", not prime)
            self.rotateEdge("U", prime)
        elif side == "z":
            self.rotateSlice("S", prime)
            self.rotateEdge("B", not prime)
            self.rotateEdge("F", prime)
        else:
            print("Input error with self.rotateCube({}, {}). Expected x, y or z".format(
                side, prime))

    def rotateEdge(self, side, prime):
        # rotate face
        start = self.faceStartIndex[side]
        indices = [start+i for i in range(NUM_SIDE_PIECES)]
        self.shiftValues(indices, 2, prime)

        # rotate edges touching the face
        indices = self.edges[side].copy()
        self.shiftValues(indices, 3, prime)

    def areCubiesSolved(self, cubies: list):
        for cubie in cubies:
            if not self.isCubieSolved(cubie):
                return False
        return True

    def isCubieSolved(self, cubie):

        if (len(cubie) == 2):
            return self.isEdgeCorrect(cubie)

        if (len(cubie) == 3):
            return self.isCornerCorrect(cubie)

    def isEdgeCorrect(self, edge):
        desired1 = self.sideToValue[edge[0]]
        desired2 = self.sideToValue[edge[1]]

        index1 = self.edgePieces[edge][0]
        index2 = self.edgePieces[edge][1]

        actual1 = self.values[index1]
        actual2 = self.values[index2]

        return (desired1 == actual1 and desired2 == actual2)

    def isCornerCorrect(self, corner):
        desired1 = self.sideToValue[corner[0]]
        desired2 = self.sideToValue[corner[1]]
        desired3 = self.sideToValue[corner[2]]

        index1 = self.cornerPieces[corner][0]
        index2 = self.cornerPieces[corner][1]
        index3 = self.cornerPieces[corner][2]

        actual1 = self.values[index1]
        actual2 = self.values[index2]
        actual3 = self.values[index3]

        return (desired1 == actual1 and
                desired2 == actual2 and
                desired3 == actual3)

    def isDesiredCubie(self, position, cubie):

        if len(cubie) == 2:
            return self.isDesiredEdge(position, cubie)

        if len(cubie) == 3:
            return self.isDesiredCorner(position, cubie)

    def isDesiredEdge(self, position, edge):
        desired1 = self.sideToValue[edge[0]]
        desired2 = self.sideToValue[edge[1]]

        index1 = self.edgePieces[position][0]
        index2 = self.edgePieces[position][1]

        actual1 = self.values[index1]
        actual2 = self.values[index2]

        if desired1 == actual1 and desired2 == actual2:
            return True
        elif desired1 == actual2 and desired2 == actual1:
            return True
        else:
            return False

    def isDesiredCorner(self, position, corner):
        desired1 = self.sideToValue[corner[0]]
        desired2 = self.sideToValue[corner[1]]
        desired3 = self.sideToValue[corner[2]]

        index1 = self.cornerPieces[position][0]
        index2 = self.cornerPieces[position][1]
        index3 = self.cornerPieces[position][2]

        position = self.values[index1]
        actual2 = self.values[index2]
        actual3 = self.values[index3]

        if desired1 == position and desired2 == actual2 and desired3 == actual3:
            return True
        elif desired1 == actual3 and desired2 == position and desired3 == actual2:
            return True
        elif desired1 == actual2 and desired2 == actual3 and desired3 == position:
            return True
        else:
            return False
        
    def stickersMatch(self, index1, index2):
        return self.values[index1] == self.values[index2]

    def correctCubieName(self, name):
        if len(name) == 2:
            ch1 = name[0]
            ch2 = name[1]

            for edge in self.edgePieces:
                if ch1 in edge and ch2 in edge:
                    return edge

        if len(name) == 3:
            ch1 = name[0]
            ch2 = name[1]
            ch3 = name[2]

            for corner in self.cornerPieces:
                if ch1 in corner and ch2 in corner and ch3 in corner:
                    return corner

    """ 
    Tells whether a corner is rotated incorrectly. Returns 0 for correct, 1 for rotated incorrectly once 
    clockwise, 2 for rotated incorrectly once counter-clockwise. Note that it does not require being the
    corner in the correct location, it just is based off of the reference face and colorVal
    """

    def isCornerRotated(self, corner: str, face: str, colorVal: int):

        stickerIndices = self.cornerPieces[corner]
        pivotIndex = corner.find(face)

        if pivotIndex == -1:
            raise ValueError(
                "Face label:{} not found in the corner:{}".format(face, corner))
        else:
            counter = 0
            for i in range(len(corner)):
                index = stickerIndices[pivotIndex]
                if self.values[index] == colorVal:
                    break
                else:
                    counter += 1
                pivotIndex = (pivotIndex + 1) % 3

        if counter == 0:
            return CORRECT
        elif counter == 1:
            return CLOCKWISE
        elif counter == 2:
            return COUNTER_CLOCKWISE
        else:
            raise ValueError(
                "Color:{} not found on this corner:{}".format(colorVal, corner))
            
    def getCubieLocation(self, cubie):
        if len(cubie) == 3:
            lst = self.cornerPieces.keys()
        if len(cubie) == 2:
            lst = self.edgePieces.keys()
        for x in lst:
           if self.isDesiredCubie(x, cubie):
               return x 

    def colorOfSideOfCubie(self, side: str, cubie: str):

        index = cubie.find(side)
        if index == -1:
            raise ValueError(
                "Side:{} not found in cubie:{}".format(side, cubie))
        else:
            if len(cubie) == 2:
                cubieIndices = self.edgePieces[cubie]
            if len(cubie) == 3:
                cubieIndices = self.cornerPieces[cubie]

            return self.values[cubieIndices[index]]
        
    def cubiesMatch(self, cubie1:str, cubie2:str):
        if len(cubie1) == 2 and len(cubie2) == 3:
            edge = cubie1
            corner = cubie2
        elif len(cubie1) == 3 and len(cubie2) == 2:
            corner = cubie1
            edge = cubie2
        else:
            raise ValueError("{} and {} can't match. One needs to be an edge and other needs to be a corner")
        
        touching = True
        cornerIndices = []
        for ch in edge:
            if ch not in corner:
                touching = False
            else:
                cornerIndices.append(corner.find(ch))
        if not touching:
            raise ValueError("{} and {} can't match since they need to be next to eachother")
        
        for i in range(len(cornerIndices)):
            cornerIndices[i] = self.cornerPieces[corner][cornerIndices[i]]
        
        edgeIndices = self.edgePieces[edge]
        
        for index in edgeIndices:
            for i in cornerIndices:
                if index + 1 == i or index - 1 == i:
                    if self.values[index] != self.values[i]:
                        return False
                    
        return True
                

    def getCommandFromIndices(self, fromIndex, toIndex, face):
        toIndex = toIndex if toIndex > fromIndex else toIndex+4
        result = toIndex - fromIndex

        command = ""
        if result == 1:
            command = face
        elif result == 2:
            command = face + "2"
        elif result == 3:
            command = face + "'"

        return command

    def algorithmEfficiency(self, algorithm: str):
        algorithm = algorithm.split()
        algorithm = [x.strip() for x in algorithm]

        val = 0
        for x in algorithm:
            if "2" in x:
                val += 0.5
            if "'" in x:
                val += 0.1
            if "F" in x or "B" in x:
                val += 2.0
            val += 1.0

        return val

    def getPossibility(self, fromPosition, toPosition, previousCommand: str, visitedCubies: list = [], offlimitsFaces: list = ["F", "B", "D"]):

        visitedCubies = visitedCubies.copy()
        visitedCubies.append(fromPosition)

        if len(toPosition) == 1 and toPosition in fromPosition:
            return previousCommand

        if fromPosition == toPosition:
            return previousCommand

        for ch in fromPosition:

            previousMoveCheck = False
            if len(previousCommand) == 0:
                previousMoveCheck = True
            else:
                previousMove = previousCommand.split().pop()
                if ch not in previousMove:
                    previousMoveCheck = True

            if ch not in offlimitsFaces and previousMoveCheck:
                cubies = {}

                order = self.movements[ch]
                fromIndex = 0
                for i in range(len(order)):
                    nextIndex = (i + 1) % len(order)
                    cubie = ch + order[i]
                    if len(fromPosition) == 3:
                        cubie += order[nextIndex]
                    cubie = self.correctCubieName(cubie)
                    if cubie == fromPosition:
                        fromIndex = i
                    if cubie not in visitedCubies:
                        cubies[cubie] = i

                if len(cubies) == 0:
                    return False

                for cubie in cubies:
                    rotation = self.getCommandFromIndices(
                        fromIndex, cubies[cubie], ch)
                    command = previousCommand + rotation + " "
                    result = self.getPossibility(
                        cubie, toPosition, command, visitedCubies, offlimitsFaces)
                    if result != False and result != None:
                        self.possibilities.append(result)

    def moveCubie(self, fromPosition, toPosition, desiredFace="", offlimitCommands=[], offlimitsFaces: list = ["F", "B", "D"], getList=False):
        if fromPosition == toPosition:
            return ""
        
        self.possibilities.clear()

        visitedCubies = []

        self.getPossibility(fromPosition, toPosition, "",
                            visitedCubies, offlimitsFaces)

        if len(self.possibilities) == 0:
            raise ValueError(
                "Not possible to move {} at location {} to {} with given offlimits faces={}"
                .format(fromPosition, self.getCubieLocation(fromPosition), toPosition, offlimitsFaces))

        #print(self.possibilities)

        if desiredFace != "":
            updatedPossibilities = []
            for possibility in self.possibilities:
                if desiredFace in possibility:
                    updatedPossibilities.append(possibility)
            self.possibilities = updatedPossibilities.copy()

        if len(offlimitCommands) != 0:
            updatedPossibilities = []
            for possibility in self.possibilities:
                for command in offlimitCommands:
                    if command not in possibility:
                        updatedPossibilities.append(possibility)
            self.possibilities = updatedPossibilities.copy()

        if getList:
            return self.possibilities

        bestCase = self.algorithmEfficiency(self.possibilities[0])
        bestPossibility = self.possibilities[0]
        for possibility in self.possibilities:
            currentCase = self.algorithmEfficiency(possibility)
            if currentCase < bestCase:
                bestCase = currentCase
                bestPossibility = possibility
        return bestPossibility

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
                    command = self.edgeToFaceCommand["F"][side][edge]
                    if numbersOnFace == 2 and "2" in command:
                        command = command[0]
                    self.rotation(command)
                    return True
                if primaryFace == "B":
                    command = self.edgeToFaceCommand["B"][side][edge]
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
                            command = self.edgeToFaceCommand["F"][side][e]
                        else:
                            command = self.edgeToFaceCommand["B"][side][e]
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

    def updateLineEdges(self):
        total = 0

        self.badEdges.clear()

        for face in self.edgesPerFace:
            self.edgesPerFace[face] = 0

        for edge in self.edgePieces:

            if self.isDesiredCubie(edge, "DF"):
                self.edgePiecesState[edge] = "DF"
                self.badEdges.append(edge)
                self.edgesPerFace[edge[0]] += 1
                self.edgesPerFace[edge[1]] += 1
                if edge != "DF":
                    total += 1
            elif self.isDesiredCubie(edge, "DB"):
                self.edgePiecesState[edge] = "DB"
                self.badEdges.append(edge)
                self.edgesPerFace[edge[0]] += 1
                self.edgesPerFace[edge[1]] += 1
                if edge != "DB":
                    total += 1
            else:
                self.edgePiecesState[edge] = ""

        self.numBadEdges = total

        return total

    def getDesiredAndOppositeFaces(self, dEdge):

        desiredFace = ""
        oppositeFace = ""
        lEdges = self.edgesPerFace["L"]
        rEdges = self.edgesPerFace["R"]
        if lEdges == 2:
            desiredFace = "L"
        elif rEdges == 2:
            desiredFace = "R"
        elif lEdges == 1:
            if "L" in dEdge:
                desiredFace = "R"
            else:
                desiredFace = "L"
        elif rEdges == 1:
            if "R" in dEdge:
                desiredFace = "L"
            else:
                desiredFace = "R"
        else:
            desiredFace = "R"

        if desiredFace == "L":
            oppositeFace = "R"
        else:
            oppositeFace = "L"

        return desiredFace, oppositeFace

    def solveLineTwoOnTheBottom(self):

        # bottom pieces are across from eachother and in the correct position
        if self.isCubieSolved("DF") and self.isCubieSolved("DB"):
            return True
        # bottom pieces are across from eachother but in swapped positions
        elif self.isDesiredCubie("DB", "DF") and self.isDesiredCubie("DF", "DB"):
            self.rotation("D2")
            return True
        # bottom pieces are across from eachother but not in the correct position
        elif self.edgePiecesState["DR"] != "" and self.edgePiecesState["DL"] != "":
            if self.isDesiredCubie("DR", "DF"):
                self.rotation("D'")
                return True
            if self.isDesiredCubie("DL", "DF"):
                self.rotation("D")
                return True
        # bottom pieces are right next to eachother
        else:
            fbEdge = ""
            lrEdge = ""
            if "F" in self.badEdges[0] or "B" in self.badEdges[0]:
                fbEdge = self.badEdges[0]
                lrEdge = self.badEdges[1]
            else:
                fbEdge = self.badEdges[1]
                lrEdge = self.badEdges[0]

            if "L" in lrEdge:
                self.rotation("L")
                command = self.edgeToFaceCommand["R"]["D"][fbEdge]
                self.rotation(command)
                self.rotation("L'")
                return self.solveLine()
            if "R" in lrEdge:
                self.rotation("R")
                command = self.edgeToFaceCommand["L"]["D"][fbEdge]
                self.rotation(command)
                self.rotation("R'")
                return self.solveLine()

    def solveLineOneOnTheBottom(self):
        # get the edge on the down face
        dEdge = ""
        if "D" in self.badEdges[0]:
            dEdge = self.badEdges[0]
        else:
            dEdge = self.badEdges[1]

        # set the desiredFace and the oppositeFace
        desiredFace, oppositeFace = self.getDesiredAndOppositeFaces(dEdge)

        # move D to the opposite
        if oppositeFace not in dEdge:
            command = self.edgeToFaceCommand[oppositeFace]["D"][dEdge]
            self.rotation(command)
            return self.solveLine()

        # if one on the desired side, move it to the bottom
        if self.edgesPerFace[desiredFace] == 1:
            lrEdge = ""
            if desiredFace in self.badEdges[0]:
                lrEdge = self.badEdges[0]
            else:
                lrEdge = self.badEdges[1]

            command = self.edgeToFaceCommand["D"][desiredFace][lrEdge]
            self.rotation(command)
            return self.solveLine()

        # if zero on the desired side, move it to the desired side and then the bottom
        if self.edgesPerFace[desiredFace] == 0:
            uEdge = ""
            if "U" in self.badEdges[0]:
                uEdge = self.badEdges[0]
            else:
                uEdge = self.badEdges[1]

            command = self.edgeToFaceCommand[desiredFace]["U"][uEdge]
            self.rotation(command)
            return self.solveLine()

    def solveLineNoneOnTheBottom(self):

        desiredFace, oppositeFace = self.getDesiredAndOppositeFaces("")

        if self.edgesPerFace[desiredFace] == 0:
            uEdge = ""
            if "U" in self.badEdges[0]:
                uEdge = self.badEdges[0]
            else:
                uEdge = self.badEdges[1]

            command = self.edgeToFaceCommand[desiredFace]["U"][uEdge]
            self.rotations("U L2 R2")
            return self.solveLine()
        else:
            edge = ""
            if desiredFace in self.badEdges[0]:
                edge = self.badEdges[0]
            else:
                edge = self.badEdges[1]

            command = self.edgeToFaceCommand["D"][desiredFace][edge]
            self.rotation(command)
            return self.solveLine()

    def solveLine(self):
        if self.updateLineEdges() == 0:
            return True

        if self.edgesPerFace["D"] == 2:
            return self.solveLineTwoOnTheBottom()
        elif self.edgesPerFace["D"] == 1:
            return self.solveLineOneOnTheBottom()
        else:
            return self.solveLineNoneOnTheBottom()

    def updateCubiesLists(self, desiredCubies: list = ["DR", "BR", "DRB"]):
        self.leftCubies.clear()
        self.upCubies.clear()
        self.rightCubies.clear()
        for desiredCubie in desiredCubies:
            for cubie in self.cubies:
                if len(desiredCubie) == len(cubie):
                    if self.isDesiredCubie(cubie, desiredCubie):
                        if "L" in cubie:
                            self.leftCubies.append(desiredCubie)
                        if "U" in cubie:
                            self.upCubies.append(desiredCubie)
                        if "R" in cubie:
                            self.rightCubies.append(desiredCubie)

    def isOneByTwoSolved(self):
        return self.areCubiesSolved(["DFR", "FR"])

    def isTwoByTwoSolved(self):
        return self.areCubiesSolved(["DR", "DRB", "BR"])

    # "U R' U' R U R' "
    
    def placeCornerInDFR(self, corner, oneByTwo = False):
        
        if self.getCubieLocation(corner) == "DFR":
            return True
        
        if self.getCubieLocation(corner) == "UFL":
            command = ""
            if oneByTwo:
                condition = self.isDesiredCubie("UF","FR")
            else:
                condition = self.isDesiredCubie("UF", "BR")
                
            if condition:
                command = "U' R U R' "
            else:
                command = "R U' R' "
            self.rotations(command)
            return self.placeCornerInDFR(corner, oneByTwo)
        else:
            cornerLocation = self.getCubieLocation(corner)
            command = self.moveCubie(cornerLocation, "UFL", desiredFace="U", offlimitsFaces=["F", "B", "D", "R"])
            self.rotations(command)
            return self.placeCornerInDFR(corner,oneByTwo)

    def edgeAlreadyPlacedSolve(self):
        DFRLocation = self.getCubieLocation("DFR")
        command = self.moveCubie(DFRLocation, "URF", offlimitsFaces=["F","B","D","R"])
        self.rotations(command)
        orientation = self.isCornerRotated("URF", "F", self.sideToValue["F"])
        if orientation == CORRECT:
            self.rotations("U' R U2 R' U R U R'")
        elif orientation == CLOCKWISE:
            self.rotations("U' R U' R' U2 R U' R'")
        elif orientation == COUNTER_CLOCKWISE:
            self.rotations("R U R' U' R U R' U' R U R' U'")
        else:
            raise ValueError(
                "Orientation: {}, Command: {}".format(orientation, command))

    def cornerAlreadyPlacedSolve(self):
        cubieLocation = self.getCubieLocation("FR")
        command = self.moveCubie(cubieLocation, "UR", offlimitsFaces=["F", "B", "D", "R"])
        self.rotations(command)
        orientation = self.isCornerRotated("DFR", "F", self.sideToValue["F"])
        if orientation == CORRECT:
            self.rotations("R' U' R' U' R' U R U R")
        elif orientation == CLOCKWISE:
            self.rotations("R U' R' U R U' R'")
        elif orientation == COUNTER_CLOCKWISE:
            self.rotations("R U R' U' R U R'")
        else:
            raise ValueError(
                "Orientation: {}, Command: {}".format(orientation, command))

    def solveOneByTwoBlock(self):
        
        if self.isOneByTwoSolved():
            return True
        elif self.isCubieSolved("FR") and self.isDesiredCubie("DFR","DFR"):
            orientation = self.isCornerRotated("DFR", "F", self.sideToValue["F"])
            if orientation == CLOCKWISE:
                self.rotations("R U R' U' R U2 R' U' R U R'")
            elif orientation == COUNTER_CLOCKWISE:
                self.rotations("R U2 R U R' U R U2 R2")
            return self.solveOneByTwoBlock()
        elif self.isCubieSolved("FR"):
            self.edgeAlreadyPlacedSolve()
            return self.solveOneByTwoBlock()
        elif self.isDesiredCubie("DFR", "DFR"):
            self.cornerAlreadyPlacedSolve()
            return self.solveOneByTwoBlock()
        else:
            self.placeCornerInDFR("DFR",oneByTwo=True)
            return self.solveOneByTwoBlock()
        
    def solveTwoByTwoBlock(self):
        if self.isTwoByTwoSolved():
            return True
        #self.updateCubiesLists(desiredCubies=["DR", "BR", "DRB"])
        
        if (self.cubiesMatch("UFL", "UL") and self.isDesiredCubie("UFL", "DRB") and
                "R" in self.getCubieLocation("DR")):
            command = ""
            DRLocation = self.getCubieLocation("DR")
            command += self.moveCubie(DRLocation, "BR", desiredFace="R")
            command += "U2 R "
            self.rotations(command)
            return self.solveTwoByTwoBlock()
        
        if not self.isCubieSolved("DR"):
            DRLocation = self.getCubieLocation("DR")
            command = self.moveCubie(DRLocation, "DR")
            self.rotations(command)
            return self.solveTwoByTwoBlock()
            
        if self.getCubieLocation("DRB") != "DFR":
            DRBLocation = self.getCubieLocation("DRB")
            if DRBLocation == "DRB":
                algorithmNB = "R' U2 R2 U' R'"
                algorithmCCB = "R' U R U2 R U' R'"
                algorithmCB = "R' U' R U R' U R2 U' R'"
                orientation = self.isCornerRotated("DRB","D",self.sideToValue["D"])
                if orientation == CORRECT:
                    if self.isDesiredCubie("UB", "BR"): # OY not GO
                        self.rotation("U'")
                    self.rotations(algorithmNB)
                elif orientation == CLOCKWISE:
                    if self.isDesiredCubie("UR", "BR"): # GW not Gy
                        self.rotations("U R U' R' ")
                    self.rotations(algorithmCB)
                elif orientation == COUNTER_CLOCKWISE:
                    if self.isDesiredCubie("UL", "BR"): # BO not GW
                        self.rotations("R U2 R' ")
                    self.rotations(algorithmCCB)
                else:
                    raise ValueError(
                        "DFR not actually in DRB with orientation {}".format(orientation))
            else:
                self.placeCornerInDFR("DRB")
            return self.solveTwoByTwoBlock()
        
        if self.isDesiredCubie("FR", "BR") and self.isDesiredCubie("DFR", "DRB"):
            orientation = self.isCornerRotated(
                "DFR", "D", self.sideToValue["D"])
            command = ""
            if orientation == CORRECT:
                command = "R U' R' U R U' R' U"
            if orientation == CLOCKWISE:
                command = "R U R' U' R U R' U "
            if orientation == COUNTER_CLOCKWISE:
                command = "R U R' U2 R U R' U2 R U' R' U2 "
            self.rotations(command)
            return self.solveTwoByTwoBlock()
        
        if not self.isDesiredCubie("UF","BR"):
            BRLocation = self.getCubieLocation("BR")
            command = self.moveCubie(BRLocation, "UF", offlimitsFaces=["F","B","D"])
            if "R " in command:
                command += "R' "
            elif "R' " in command:
                command += "R "
            self.rotations(command)
            return self.solveTwoByTwoBlock()
        
        if self.isDesiredCubie("UF", "BR") and self.isDesiredCubie("DFR", "DRB"):
            orientation = self.isCornerRotated(
                "DFR", "D", self.sideToValue["D"])
            command = ""
            if orientation == CORRECT:
                command = "U R U' R' U "
            if orientation == CLOCKWISE:
                command = "R U R' U' R U R' U' R U "
            if orientation == COUNTER_CLOCKWISE:
                command = "R U "
            self.rotations(command)
            return self.solveTwoByTwoBlock()
        
        return self.solveTwoByTwoBlock()
        
    def isSolvedF2L(self):
        rightCubies = ["DR", "DRB", "BR", "DFR", "FR"]
        leftCubies = ["DL", "DBL", "BL", "DLF", "BL"]
        desiredCubies = rightCubies + leftCubies
        return self.areCubiesSolved(desiredCubies)

    def solveF2L(self, secondTime=False):
        if self.isSolvedF2L():
            return True

        if not secondTime:
            if self.solveTwoByTwoBlock() and self.solveOneByTwoBlock():
                self.rotation("y2")
                return self.solveF2L(True)
            else:
                raise ValueError(
                    "Problem solving 2x2 or 1x2 block on first call of solveF2L()")
        else:
            return (self.solveTwoByTwoBlock() and self.solveOneByTwoBlock())

    def listToString(self, lst: list):
        returnString = ""
        for item in lst:
            returnString = str(item) + returnString

        return returnString

    def getTopValueStrings(self):
        topValues = ""
        overallValues = ""
        for index in self.edges["U"]:
            val = self.values[index]
            overallValues += str(val)
            if val == self.sideToValue["U"]:
                topValues += "1"
            else:
                topValues += "0"

        start = self.faceStartIndex["U"]
        for i in range(NUM_SIDE_PIECES):
            index = start + i
            overallValues += str(self.values[index])

            if self.values[index] == self.sideToValue["U"]:
                topValues += "1"
            else:
                topValues += "0"

        return topValues, overallValues

    def rotateTopValues(self, topValues):
        edges = topValues[:12]
        top = topValues[12:]

        newTopValues = ""
        index = 9
        for i in range(12):
            newTopValues += edges[index]
            index = (index + 1) % 12

        index = 6
        for i in range(8):
            newTopValues += top[index]
            index = (index + 1) % 8

        return newTopValues

    def getZBLLCase(self, topValues):
        ZBLLCase = {"00100010000001011111": "ZBLL-T.txt",
                    "00010100000001011111": "ZBLL-U.txt",
                    "10000100000011011101": "ZBLL-L.txt",
                    "10100010100001010101": "ZBLL-H.txt",
                    "10100100010001010101": "ZBLL-Pi.txt",
                    "10010010000001011101": "ZBLL-S.txt",
                    "00100100100001010111": "ZBLL-AS.txt",
                    "00000000000011111111": "PLL.txt"}

        rotations = 0
        change = False
        while (True):
            if topValues in ZBLLCase:
                break
            topValues = self.rotateTopValues(topValues)
            rotations += 1

        if rotations == 1:
            self.rotation("U")
            change = True
        elif rotations == 2:
            self.rotation("U2")
            change = True
        elif rotations == 3:
            self.rotation("U'")
            change = True

        return ZBLLCase[topValues], change

    def caseMatches(self, caseFromFile, caseFromCube):
        translation = {}

        for i in range(len(caseFromCube)):
            ch1 = caseFromCube[i]
            ch2 = caseFromFile[i]

            if ch1 not in translation:
                if ch2 not in translation.values():
                    translation[ch1] = ch2
                else:
                    return False

            if ch2 != translation[ch1]:
                return False

        return True

    def getZbllAlgorithm(self, fileName, overallValues, finished=False):

        isCase = True
        case = ""
        algorithm = ""
        with open(fileName) as file:
            line = file.readline()
            while line:
                if isCase:
                    case = line
                    if self.caseMatches(case, overallValues):
                        algorithm = file.readline().strip()
                        finished = True
                        break
                isCase = not isCase
                line = file.readline()

            # special case with ZBLL-H where you have to rotate U2
            if finished == False:
                self.rotation("U2")
                return self.getZbllAlgorithm(fileName, overallValues, True)

        return algorithm
    
    def getUnsolvedCubies(self):
        cubies = []
        for edge in self.edgePieces:
            if not self.isDesiredCubie(edge,edge):
                cubies.append(edge)
        for corner in self.cornerPieces:
            if not self.isDesiredCubie(corner, corner):
                cubies.append(corner)
                
        return cubies
    
    def getCommonFace(self, cubies:list):
        edge = cubies[0]
        face = ""
        for ch in edge:
            if all(ch in cubie for cubie in cubies):
                face = ch
                break
            
        return face
    
    def needsLastRotation(self):
        
        cubies = self.getUnsolvedCubies()
             
        if len(cubies) != 8:
            return False
           
        face = self.getCommonFace(cubies)
        allOnSameFace = False
        if face != "":
            allOnSameFace = True
            
        topPermutated = True
        indices = self.edges[face]
        for i in range(0,len(indices),3):
            stickers = []
            for j in range(3):
                index = indices[i+j]
                stickers.append(self.values[index])
            if not all(stickers[0] == sticker for sticker in stickers):
                topPermutated = False
                break
            
        return (allOnSameFace and topPermutated)
                
    
    def lastRotation(self):
        
        cubies = self.getUnsolvedCubies()
        commonFace = self.getCommonFace(cubies)
        
        for edge in self.edgePieces:
            if not self.isDesiredCubie(edge, edge):
                cornerLocation = self.getCubieLocation(edge)
                command = self.moveCubie(cornerLocation, edge, offlimitsFaces=[], desiredFace=commonFace)
                self.rotations(command)
                return self.needsLastRotation()
        
        if not self.isSolved():
            raise ValueError(
                "Last rotation did not work with cube in state\n{}".format(str(self)))
                    
    def getPLLCase(self):
        topEdges = ["UF", "UL", "UB", "UR"]
        topCorners = ["UFL", "ULB", "UBR", "URF"]
        outOfPlaceEdges = []
        inPlaceEdge = ""

        for i in range(4):
            if not self.cubiesMatch(topEdges[i], topCorners[i]):
                outOfPlaceEdges.append(topEdges[i])
            else:
                inPlaceEdge = topEdges[i]
                
        edges = []
        checks = []
        for e in outOfPlaceEdges:
            edgeIndex = self.edgePieces[e][1]
            edges.append(edgeIndex)
            checkIndex = self.edgePieces[e][1]+1
            checks.append(checkIndex)
            
        if len(edges) == 3:
            if self.stickersMatch(edges[0],checks[1]):
                return COUNTER_CLOCKWISE, inPlaceEdge
            elif self.stickersMatch(edges[0], checks[2]):
                return CLOCKWISE, inPlaceEdge
            else:
                raise ValueError("Issue with getPLLCase() and 3 edges")
        elif len(edges) == 4:
            if self.stickersMatch(edges[0],checks[2]) and self.stickersMatch(edges[1],checks[3]):
                return CRISS_CROSS, inPlaceEdge
            elif self.stickersMatch(edges[0],checks[1]) and self.stickersMatch(edges[1],checks[0]):
                self.rotations("U ")
                return ZIGZAG, inPlaceEdge
            elif self.stickersMatch(edges[1], checks[2]) and self.stickersMatch(edges[2], checks[1]):
                return ZIGZAG, inPlaceEdge
            else:
                raise ValueError("Issue with getPLLCase() and 4 edges")
            
            
                    
    def PLLSolve(self):
        
        case, goodEdge = self.getPLLCase()
            
        if case == COUNTER_CLOCKWISE:
            command = self.moveCubie(goodEdge, "UF", desiredFace="U")
            command += "R' U R' U' R' U' R' U R U R2"
        elif case == CLOCKWISE:
            command = self.moveCubie(goodEdge, "UF", desiredFace="U")
            command += "R2 U' R' U' R U R U R U' R"
        elif case == ZIGZAG:
            command = "R U R' U R' U' R' U R U' R' U' R2 U R"
        elif case == CRISS_CROSS:
            command = "R L U2 R' L' F' B' U2 B F"
        else:
            raise ValueError("Couled not find PLLCase")
        
        self.rotations(command)

    def solveTop(self):
        
        if self.needsLastRotation():
            return self.lastRotation()

        case = []
        topValues, overallValues = self.getTopValueStrings()
        fileName, isChangeMade = self.getZBLLCase(topValues)

        if isChangeMade:
            topValues, overallValues = self.getTopValueStrings()

        algorithm = self.getZbllAlgorithm(fileName, overallValues)

        if algorithm == "":
            print("ERROR: Case not found with " +
                  str(overallValues) + ", " + str(fileName))
            return False
        else:
            self.rotations(algorithm)
            
            if self.needsLastRotation():
                self.lastRotation()

            return self.isSolved()
        
    def reverseAlgorithm(self, algorithm):
        movements = algorithm.split(" ")
        movements = movements[::-1]
        for i, movement in enumerate(movements):
            if len(movement) == 2:
                if movement[1] == "'":
                    movements[i] = movement[:1]
            else:
                movements[i] = movement + "'"
                
        return " ".join(movements)

    def solution(self):
        self.moves = ""
        self.orientEdges()
        self.solveLine()
        self.solveF2L()
        self.solveTop()
        return self.moves
    
