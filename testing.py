# import robot as robot
# import time

# from cube import Cube

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

dictionary = {"a":1, "b":2, "c":3, "d":4}

print(2 in dictionary.values())

list = [1,2,3,4,5,6]

def updateList():
    global list
    copy = list.copy()
    pivot = 1
    for i in range(len(list)):
        old = i
        new = pivot
        list[new] = copy[old]
        pivot = (pivot + 1) % len(list)
        
for num in list:
    print(num)
    updateList()
    
type(range(1,4))
        

