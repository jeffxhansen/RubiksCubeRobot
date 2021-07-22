# import robot as robot
# import time

from cube import Cube

'''
# Testing defaultClose and defaultOpen - accept cube
time.sleep(1)
robot.defaultClose()
time.sleep(1)
robot.defaultOpen()


# Testing acceptCube method
robot.acceptCube()
time.sleep(1)
robot.defaultOpen()

'''

# robot.defaultOpen()


cube = Cube()

scramble = "B' U' L B2 F2 R' B F2 L F U' R' F L' U B' L2 B' F2 R D' F2 R2 F2 D'"
solve = "B' L' F' L D'"
solve += " L U2 R2 L U L'"
solve += " U R U2 R"
solve += " U' R U2 R' U R U' R'"
solve += " U L' U' L U2 L'"
solve += " U2 L U' L' U2 L"
solve += " B U2 R U R' B' U R U2 R' B U2 B' U'"

print(cube)
cube.rotations(scramble)
print()
values = cube.getValues()
newCube = Cube()
print(cube == newCube)
print("Old cube: \n" + str(cube))
print(cube.getColorsOrder())
newCube.set(values,["y","w","b","o","r","g"])
print("Old cube: \n" + str(cube))
print(cube.getColorsOrder())
print("New cube: \n" + str(newCube))
print(newCube.getColorsOrder())
newCube.rotations(solve)
print(newCube)

