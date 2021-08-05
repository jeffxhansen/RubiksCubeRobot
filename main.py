
from cube import Cube

import random

# still in progress
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
    
    
# TEST START
# badEdgesTest()
# orientEdgesTest()
# testingSixEdges()
# testingOrientEdges()



# TEST FINISH
