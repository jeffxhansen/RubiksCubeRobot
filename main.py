
from cube import Cube
from robot import Robot

import random
import time

# still in progress

def robotToStringTest():
    robot = Robot()
    robot.defaultOpen()
    
robotToStringTest()


def badEdgesTest():
    '''
    twoBadEdges = Cube()
    twoBadEdges.rotations("F U2 D2 B2 U' F U' R' L' D R' F U' R' F")
    print(twoBadEdges.numBadEdges)
    print("edgePiecesState")
    print(twoBadEdges.edgePiecesState)
    print("edgesPerFace")
    print(twoBadEdges.edgesPerFace)
    print("SOL: " + str(twoBadEdges.solution()))
    print(twoBadEdges.numBadEdges)
    print("edgePiecesState")
    print(twoBadEdges.edgePiecesState)
    print("edgesPerFace")
    print(twoBadEdges.edgesPerFace)
    '''
    fourBadEdges = Cube()
    fourBadEdges.rotations("F U2 D2 B2 U' F U' R'   L' D R' U' D R' L'")
    print(fourBadEdges.numBadEdges)
    print("edgePiecesState")
    print(fourBadEdges.edgePiecesState)
    print("edgesPerFace")
    print(fourBadEdges.edgesPerFace)

    eightBadEdges = Cube()
    eightBadEdges.rotations(" F' B' U L2 D B R2 L2 U'")
    print(eightBadEdges.numBadEdges)
    print("edgePiecesState")
    print(eightBadEdges.edgePiecesState)
    print("edgesPerFace")
    print(eightBadEdges.edgesPerFace)

    sixBadEdges = Cube()
    sixBadEdges.rotations("R F2 B' D' L U2 L2 D2 B")
    print(sixBadEdges.numBadEdges)
    print("edgePiecesState")
    print(sixBadEdges.edgePiecesState)
    print("edgesPerFace")
    print(sixBadEdges.edgesPerFace)

    eightBadEdges2 = Cube()
    eightBadEdges2.rotations("R' D F2 R B' U F' D' F2")
    print(eightBadEdges2.numBadEdges)
    print("edgePiecesState")
    print(eightBadEdges2.edgePiecesState)
    print("edgesPerFace")
    print(eightBadEdges2.edgesPerFace)

# passed
def middleRotationsTest():
    cube = Cube()
    print(cube)
    cube.rotation("E")
    print(cube)
    cube.rotation("E'")
    print(cube)
    cube.rotation("M")
    print(cube)
    cube.rotation("M'")
    print(cube)
    cube.rotation("S")
    print(cube)
    cube.rotation("S'")
    print(cube)
    
# passed
def rotateCubeTest():
    cube = Cube()
    print(cube)
    cube.rotation("x")
    print(cube)
    cube.rotation("x'")
    print(cube)
    cube.rotation("y")
    print(cube)
    cube.rotation("y'")
    print(cube)
    cube.rotation("z")
    print(cube)
    cube.rotation("z'")
    print(cube)
    
# passed
def setFaceToFrontTest():
    cube = Cube()
    print(cube)
    cube.setToFront("L")
    print(cube)
    cube.setToFront("R")
    print(cube)
    cube.setToFront("U")
    print(cube)
    cube.setToFront("D")
    print(cube)
    
def orientEdgesTest():
    cube = Cube()
    # impossible: "F U2 D2 B2 U' F U' R' L' D R' U' R U' L' D L2"
    cube.rotations("F R2 B F2 L2 F R' D L2 F L2 R L' L2 R' D")
    cube.updateBadEdges()
    print(cube.numBadEdges)
    print("edgePiecesState")
    print(cube.edgePiecesState)
    print("edgesPerFace")
    print(cube.edgesPerFace)
    print("badEdges")
    print(cube.badEdges)
    print("SOL: " + str(cube.solution()))
    print(cube.numBadEdges)
    print("edgePiecesState")
    print(cube.edgePiecesState)
    print("edgesPerFace")
    print(cube.edgesPerFace)
    print("badEdges")
    print(cube.badEdges)
    
def testingSixEdges():
    sides = ["L","R","U","D"]
    movements = []
    for side in sides:
        movements.append(" " + side)
        movements.append(" " + side + "2")
        movements.append(" " + side + "'")
    #print(movements)
    
    '''
    F U R' R' L2 U' R
    SOL: R D L2 F2 D' F
    
    F R D R' L' D' L'
    SOL: L2 R D' R' F
    '''
        
    for i in range(100):
        scramble = "F R2 B F2 L2 F R' D L2 F L2 R"
        for i in range(6):
            scramble += movements[random.randint(0,len(movements)-1)]
        cube = Cube()
        print(".",end="")
        cube.rotations(scramble)
        cube.updateBadEdges()
        badEdges = cube.badEdges.copy()
        before = cube.numBadEdges
        solution = cube.solution()
        after = cube.numBadEdges
        if (after != 0):
            print()
            print("Failed with: " + scramble)
        '''
        if (len(solution.split()) > 6):
            print(scramble)
            print(badEdges)
            print("SOL: " + solution)
            print()
        '''
    print()
    print("Done")
    

def testingOrientEdges():
    sides = ["L", "R", "U", "D", "F", "B"]
    movements = []
    for side in sides:
        movements.append(" " + side)
        movements.append(" " + side + "2")
        movements.append(" " + side + "'")
    #print(movements)

    '''
    F U R' R' L2 U' R
    SOL: R D L2 F2 D' F
    
    F R D R' L' D' L'
    SOL: L2 R D' R' F
    '''

    for i in range(10000):
        scramble = ""
        for i in range(14):
            scramble += movements[random.randint(0, len(movements)-1)]
        cube = Cube()
        print(".", end="")
        cube.rotations(scramble)
        cube.updateBadEdges()
        badEdges = cube.badEdges.copy()
        before = cube.numBadEdges
        solution = cube.solution()
        after = cube.numBadEdges
        #print(str(before) + " " + str(after) + " " + solution)
        if (after != 0):
            print()
            print("Failed with: " + scramble)
        '''
        if (len(solution.split()) > 6):
            print(scramble)
            print(badEdges)
            print("SOL: " + solution)
            print()
        '''
    print()
    print("Done")
    
def isCorrectTest():
    cube = Cube()
    print(cube.isCubieSolved("UF"))
    cube.rotation("U")
    print(cube.isDesiredCubie("UL","UF"))
    cube.rotation("U'")
    print(cube.isCubieSolved("UF"))
    print()
    print(cube.isCubieSolved("UFL"))
    cube.rotation("U")
    print(cube.isDesiredCubie("ULB", "UFL"))
    cube.rotation("U'")
    print(cube.isCubieSolved("UFL"))
    
def solveLineTest():
    sides = ["L", "R", "U", "D"]
    movements = []
    for side in sides:
        movements.append(" " + side)
        movements.append(" " + side + "2")
        movements.append(" " + side + "'")
    
    for i in range(10000):
        cube = Cube()
        scramble = ""
        for i in range(12):
            scramble += movements[random.randint(0, len(movements)-1)]
        cube.rotations(scramble)
        before = cube.updateLineEdges()
        badEdges = cube.badEdges.copy()
        badEdges = str(badEdges)
        solution = cube.solution()
        after = cube.updateLineEdges()
        print(".",end="")
        if after != 0:
            print("Failed!")
            print("Scramble: " + scramble)
            print("Edges: " + badEdges)
            print("Solution: " + solution)
            print()
            break
        '''
        else:
            print("Succeeded!")
            print("Scramble: " + scramble)
            print("Edges: " + badEdges)
            print("Solution: " + solution)
            print()
        '''
    print("Done")
    
def orientEdgesSubtest(scramble, cube: Cube):
    cube.moves = ""
    cube.updateBadEdges()
    orientEdges = cube.badEdges.copy()
    cube.orientEdges()
    cube.updateBadEdges()
    orientEdgesAfter = cube.numBadEdges
    solution = cube.moves

    if orientEdgesAfter != 0:
        print("Failed")
        print("Scramble: " + scramble)
        print("Orient Before:" + str(orientEdges))
        print("Solution: " + solution)
        
def solveLineEdgesSubtest(scramble, cube: Cube):
    cube.updateLineEdges()
    lineEdges = cube.badEdges.copy()
    cube.solveLine()
    cube.updateLineEdges()
    lineEdgesAfter = cube.numBadEdges
    solution = cube.moves

    if lineEdgesAfter != 0:
        print("Failed")
        print("Scramble: " + scramble)
        print("LineEdges Before:" + str(lineEdges))
        print("Solution: " + solution)
        
        
def topTest():
    cube = Cube()
    algorithm = "R U R' U R U2 R' U2"
    cube.rotations(algorithm)
    top, overall = cube.getTopValueStrings()
    print(top)
    print(overall)
    x, y = cube.getZBLLCase(top)
    print(x)
    if y:
        top, overall = cube.getTopValueStrings()
    print(top)
    print(overall)
    print(cube)
    cube.solveTop()
    print(cube)
    
def reversedAlgorithm(algorithm : str):
    
    algorithm = algorithm.strip()
    movements = algorithm.split()
    movements.reverse()
    
    result = ""
    for movement in movements:
        
        if len(movement) == 1:
            result += movement
            result += "'"
        else:
            if movement[1] == "'":
                result += movement[0]
            else:
                result += movement
        result += " "
    result = result.strip()
        
    return result
    
def partialTopTest():
    
    # 1 31 47
    with open("ZBLL-H.txt") as file:
        for i in range(38):
            case = file.readline().strip()
            algorithm = file.readline().strip()
        
        scramble = reversedAlgorithm(algorithm)
        
        cube = Cube()
        cube.rotations(scramble)
        print(case)
        print(algorithm)
        print(cube)
        cube.solveTop()
        print(cube)
            
    
def completeTopTest():
    files = ["ZBLL-T.txt", "ZBLL-U.txt", "ZBLL-L.txt", "ZBLL-H.txt",
             "ZBLL-Pi.txt", "ZBLL-S.txt", "ZBLL-AS.txt"]
    for fileName in files:
        print(fileName)
        with open(fileName) as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            
        isCase = True
        lineCounter = 0
        case = ""
        algorithm = ""
        scramble = ""
        for line in lines:
            lineCounter += 1
            #print(fileName[5] + str(lineCounter), end="")
            if isCase:
                case = line
            else:
                
                algorithm = line
                scramble = reversedAlgorithm(algorithm)
                
                cube = Cube()
                solvedTop, solvedValues = cube.getTopValueStrings()
                cube.rotations(scramble)
                topValuesBefore, overallValuesBefore = cube.getTopValueStrings()
                textFile = cube.getZBLLCase(topValuesBefore)
                topValuesBefore, overallValuesBefore = cube.getTopValueStrings()
                if (textFile != fileName and not cube.caseMatches(case,overallValuesBefore)):
                    print()
                    print("Failed setting up case scramble: " + str(scramble))
                    print("File: " + str(fileName))
                    print("Algorithm: " + str(algorithm))
                    print("Case: " + str(case))
                    print("LineNumber: " + str(lineCounter))
                    print("Case #" + str(lineCounter//2))
                    print()
                else:
                    cube.solveTop()
                    topValuesAfter, overallValuesAfter = cube.getTopValueStrings()
                    if (cube.caseMatches(solvedValues, overallValuesAfter)):
                        print(".",end="")
                    else:
                        print()
                        print("Failed solving scramble: " + str(scramble))
                        print("File: " + str(fileName))
                        print("Algorithm: " + str(algorithm))
                        print("Case: " + str(case))
                        print("LineNumber: " + str(lineCounter))
                        print("Case #" + str(lineCounter//2))
                        print(cube)
                        print()
            isCase = not isCase
            
        print(lineCounter)
     

    
def cubeRotationsTest():
    cube = Cube()
    rotate = "R' D' R D "
    command = ""
    for i in range(4):
        command += str(rotate*(i*2))
        command += "U "
    cube.rotations(command)
    print(cube.isCornerRotated("UFL","U"))
    print(cube.isCornerRotated("URF","U"))
    print(cube.isCornerRotated("UBR","U"))
    print(cube.isCornerRotated("ULB", "U"))
    
def lastRotationTest():
    cube = Cube()
    cube.rotation("U'")
    print(cube.isDesiredCubie("UF","UR"))
    
def isSolvedTest():
    
    moveCenters = "R L' F' B U' D R L'"
    
    cube = Cube()
    print("True: " + str(cube.isSolved()))
    cube.rotation("U")
    print("False: " + str(cube.isSolved()))
    cube.rotation("U'")
    print("True: " + str(cube.isSolved()))
    cube.rotations("x")
    print("True: " + str(cube.isSolved()))
    cube.rotations("x'")
    print("True: " + str(cube.isSolved()))
    cube.rotations(moveCenters)
    print("False: " + str(cube.isSolved()))
    reverseMoveCenters = reversedAlgorithm(moveCenters)
    cube.rotations(reverseMoveCenters)
    print("True: " + str(cube.isSolved()))
    
def zbllHTest():
    cube = Cube()
    # 31355132310203235303
    cube.rotations("B D' B2 U2 B U' B2 R2 F' U F R2 U' B2 U2 D U2")
    print(cube)
    top, overall = cube.getTopValueStrings()
    print(top)
    print(overall)
    print(cube.caseMatches("30325032311213535303",overall))
    newBase = "31355132310203235303"
    newBase = cube.rotateTopValues(newBase)
    newBase = cube.rotateTopValues(newBase)
    print(cube.caseMatches(newBase, overall))
 
'''   
def zbllTest():
    with open("casemap.js") as file:
        counter = 0
        scrambles = []
        while line := file.readline().strip():
            if ("=" not in line and "{" not in line and "[" not in line and 
                "}" not in line and "]" not in line and ":" not in line):
                cube = Cube()
                scramble = line.replace("\"","").replace(",","")
                scrambles.append(scramble)
                cube.rotations(scramble)
                # cube.moves = ""
                cube.solveTop()
                
                if not cube.isSolved():
                    print("Failed: " + str(scramble))
                    print(cube)
                    print(cube.moves)
                
                else:
                
                print(".",end="")
                counter += 1
        print(counter)
        
    tempScramble = scrambles[random.randint(0,len(scrambles))]
    cube1 = Cube()
    print(cube1)
    cube1.rotations(tempScramble)
    print(cube1)
    cube1.solveTop()
    print(cube1)
'''     
                    
def lastRotationTest():
    cube = Cube()
    
    faces = "LRBUDF"
    movements = []
    
    for ch in faces:
        movements.append(ch)
        movements.append((ch + "'"))
        movements.append((ch+"2"))
        
    for i in range(10000):
        scramble = movements[random.randint(0, len(movements)-1)]
        cube.rotations(scramble)
        before = str(cube)
        cube.lastRotation()
        after = str(cube)
        
        if not cube.isSolved():
            print(before)
            print(scramble)
            print(after)
        else:
            print(".", end="")
            
    print("Done")
    
# passed
def isCornerRotatedTest():
    cube = Cube()
    algorithm = "R' D' R D "
    first = (algorithm*2) + "U "
    second = (algorithm*4) + "U' "
    final = first + second
    cube.rotations(final)
    print(cube)
    upValue = cube.sideToValue["U"]
    print(cube.isCornerRotated("URF", "U", upValue))
    print(cube.isCornerRotated("UBR", "U", upValue))
    #print(cube.isCornerRotated("URF", "Z", upValue))
    
def colorOfSideOfCubieTest():
    cube = Cube()
    print(cube.colorOfSideOfCubie("U","UF"))
    print(cube.colorOfSideOfCubie("R","UR"))
    print(cube.colorOfSideOfCubie("Z","UF"))
    
def updateCubiesListTest():
    cube = Cube()
    cube.updateCubiesLists(["DR","DRB","BR"])
    print(cube.leftCubies)
    print(cube.upCubies)
    print(cube.rightCubies)
    
def solveF2LTest():
    cube = Cube()
    print(cube.isSolvedF2L())
    cube.rotation("U")
    print(cube.isSolvedF2L())
    cube.rotation("R")
    print(cube.isSolvedF2L())
    
def correctCubieNameTest():
    cube = Cube()
    cube.moveCorner("UFL","DFR")
    
def moveCornerTest():
    cube = Cube()
    print(cube.moveCubie("UFL","DFR"))
    print()
    print(cube.moveCubie("UF", "DB", offlimitsFaces=["F", "B"]))
    
def generateCornerToCornerDictionary():
    cube = Cube()
    string = ""
    for side in cube.sides:
        string += "\"" + side + "\": {"
        for corner in cube.cornerPieces:
            if side in corner:
                string += "\t\"" + corner + "\": {"
                for c in cube.cornerPieces:
                    if side in c:
                        string += "\"" + c + "\": \"\", "
                string = string[:-2]
                string += "},\n"
        string = string[:-2]
        string += "},\n"
        
    print(string)
                
def getLocationTest():
    cube = Cube()
    cube.rotation("U")
    print(cube.getCubieLocation("UF"))
    
def oneByTwoTest():
    for i in range(300):
        scramble = ""
        rRotation = True
        normal = True
        options = ["U ", "U' ", "U2 ", "U2 "]
        optionsL = ["L ", "L' ", "L2 "]
        for i in range(11):
            if rRotation:
                scramble += "R"
                if not normal:
                    scramble += "'"
                scramble += " "
                normal = not normal
            else:
                scramble += options[random.randint(0, len(options)-1)]
                scramble += optionsL[random.randint(0, len(optionsL)-1)]
            rRotation = not rRotation
        
        cube = Cube()
        #scramble = "R U2 R' U R U' R' U' R U' R'"
        cube.rotations(scramble)
        cube.moves = ""
        print(scramble)
        # print(cube)
        cube.solveOneByTwoBlock()
        print(cube.moves)
        if not cube.isOneByTwoSolved():
            raise ValueError("Scramble: {}\nSolution: {}".format(scramble, cube.moves))
        else:
            print()
            
def fullTwoByTwoTest():
    sides = ["L", "R", "U", "D", "F", "B"]
    movements = []
    for side in sides:
        movements.append(side + " ")
        movements.append(side + "2 ")
        movements.append(side + "' ")

    for i in range(400):
        cube = Cube()
        scramble = ""
        scrambles = 0
        previousScramble = ""
        currentScramble = ""
        while scrambles < 20:
            currentScramble = movements[random.randint(0, len(movements)-1)]
            if currentScramble[0] not in previousScramble:
                scramble += currentScramble
                scrambles += 1
                previousScramble = currentScramble

        #scramble = "R D U R' D2 R2 B2 R2 U L U L D' R' L2 U2 F R2 B' R "
        cube.rotations(scramble)
        #print(scramble)
        #print(cube)
        if cube.orientEdges():
            if cube.solveLine():
                #print(cube)
                cube.solveF2L()
        if not cube.isSolvedF2L():
            raise ValueError("F2L not solved with scramble {}".format(scramble))
        else:
            print(".",end="")
            
    print("Done")

def twoByTwoTest():
    for i in range(600):
        scramble = ""
        rRotation = True
        normal = True
        options = ["U ", "U' ", "U2 ", "L ", "L' ", "L2 ", "R ", "R' ", "R2 "]
        scrambles = 0
        previousScramble = ""
        currentScramble = ""
        while scrambles < 20:
            currentScramble = options[random.randint(0, len(options)-1)]
            if currentScramble[0] not in previousScramble:
                scramble += currentScramble
                scrambles += 1
                previousScramble = currentScramble

        cube = Cube()
        scramble = "U R' L' U2 R' U R L' R' L2 R"
        cube.rotations(scramble)
        cube.moves = ""
        #print(scramble)
        cube.solveTwoByTwoBlock()
        #print(cube.moves)
        if not cube.isTwoByTwoSolved():
            raise ValueError(
                "Scramble: {}\nSolution: {}".format(scramble, cube.moves))
        else:
            print(".", end="")
    
    print("Done")
            
def cubiesMatchTest():
    cube = Cube()
    print(cube.cubiesMatch("UFL","UF"))
    print(cube.cubiesMatch("UF", "UFL"))
    #print(cube.cubiesMatch("UF","UR"))
    #print(cube.cubiesMatch("UFL","UBR"))
    cube.rotation("F")
    print(cube.cubiesMatch("UFL", "UL"))
    print(cube.cubiesMatch("UF", "UFL"))
    print(cube.cubiesMatch("DRB", "DR"))
    
def lastEdgePermutationTest():
    cube = Cube()
    scramble = "R2 U' R' U' R U R U R U' R "
    scramble += "U'"
    cube.rotations(scramble)
    cube.PLLSolve()
    print(cube)
    
    cube = Cube()
    scramble = "R' U R' U' R' U' R' U R U R2 "
    scramble += "U"
    cube.rotations(scramble)
    cube.PLLSolve()
    print(cube)
    
    cube = Cube()
    scramble = "R L U2 R' L' F' B' U2 B F "
    scramble += "U"
    cube.rotations(scramble)
    cube.PLLSolve()
    print(cube)
    
    cube = Cube()
    scramble = "U R U R' U R' U' R' U R U' R' U' R2 U R "
    cube.rotations(scramble)
    cube.PLLSolve()
    print(cube)
    
    cube = Cube()
    scramble = "R U R' U R' U' R' U R U' R' U' R2 U R "
    cube.rotations(scramble)
    cube.PLLSolve()
    print(cube)

def lastRotationTest():
    for i in range(10):
        cube = Cube()
        scramble = getScramble(1)
        cube.rotations(scramble)
        print(scramble + ": ", end="")
        print(cube.needsLastRotation(), end=" -> ")
        cube.lastRotation()
        print(cube.needsLastRotation())
        

def solveTest():
    scrambles = 1000
    periodsPerLine = 0
    start = time.time()
    for i in range(scrambles):
        cube = Cube()
        scramble = getScramble(20)
                
        # scramble = "D' L B' F2 L R U' R2 F R2 B L' R2 B' D F R B' L' D' "
        # scramble = "B' D R D U R F' U D' B2 F B R L R2 D R2 B U2 L2 "
        # scramble = "L' U D' U2 F' B2 L F' R B R F' R' U R D2 U2 B2 F' U"
        cube.rotations(scramble)
        before = str(cube)
        #print(scramble)
        solution = cube.solution()
        after = str(cube)
        if not cube.isSolved():
            print("\nFailed with scramble: {} and solution: {}\n".format(
                scramble, solution))
            print(before + "\n" + after)
            return (scramble + solution)
        else:
            #print("Scramble: {}\nSolution: {}\n{}".format(scramble, solution, str(cube)))
            print(".", end="")
            periodsPerLine += 1
            if periodsPerLine > 50:
                print()
                periodsPerLine = 0

        #print(cube)
    print()
    end = time.time()
    print("Solved: " + str(scrambles) + " Rubik's Cubes succesfully in " + str(end-start) + " seconds.")


def debugSolveTest():
    movements = solveTest()
    if movements == "Done":
        print("It worked")
    else:
        cube = Cube()
        movementsSoFar = ""
        movementsList = movements.split()
        counter = 0
        while counter < len(movementsList):
            print(movements)
            print(movementsSoFar)
            iterations = input("How far forward do you want to go? ({} - max): ".format(len(movementsList)-counter))
            iterations = int(iterations)
            for i in range(iterations):
                currMove = movementsList[counter]
                cube.rotations(currMove)
                movementsSoFar += currMove + " "
                counter += 1
            
            print(cube)
                
            
            
            
            
    
def getScramble(scrambleSize, sides=["L", "R", "U", "D", "F", "B"]):
    movements = []
    for side in sides:
        movements.append(side + " ")
        movements.append(side + "2 ")
        movements.append(side + "' ")
        
    scramble = ""
    scrambles = 0
    previousScramble = ""
    currentScramble = ""
    while scrambles < scrambleSize:
        currentScramble = movements[random.randint(0, len(movements)-1)]
        if currentScramble[0] not in previousScramble:
            scramble += currentScramble
            scrambles += 1
            previousScramble = currentScramble
            
    return scramble
       
    
# TEST START
# badEdgesTest()
# orientEdgesTest()
# testingSixEdges()
#testingOrientEdges()
# isCorrectTest()
# solveLineTest()

# cubeRotationsTest()

# topTest()
# completeTopTest()
#partialTopTest()
#solveTest()

# zbllTest()
# zbllHTest()
# isSolvedTest()
# lastRotationTest()
#isCornerRotatedTest()
# #updateCubiesListTest()
# colorOfSideOfCubieTest()
# correctCubieNameTest()
# moveCornerTest()
# generateCornerToCornerDictionary()
# getLocationTest()
# oneByTwoTest()
# cubiesMatchTest()
# twoByTwoTest()

# fullTwoByTwoTest()
# solveTest()
# lastEdgePermutationTest()
# lastRotationTest()
# debugSolveTest()

#solveF2LTest()

# TEST FINISH

# integration tests
#testingOrientEdges()
# solveLineTest()
#zbllTest()
#isSolvedTest()

'''
31355132310203235303
L' B R2 B' L' U F D2 F U' B2 U R2 B2 D F2 U U2
31355132310203235303
B' U2 B U' L2 F U F' L2 D L2 D' B2 U B2 U' L2 U U2
'''
