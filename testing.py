
'''
import cv2 as cv
import numpy as np
print(cv.__version__)

img = cv.imread('Capture.png',1)
print(type(img[0, 0]))

height, width, colors = img.shape

print(height)
print(width)
print(colors)

square = height // 5

startPoint = (square*2+2, square*2+2)
endPoint = (square*3-2, square*3-2)
color = (255,50,50)
thickness = 2
gradientChange = 255 // 9
gradient = 0
centerSpace = square // 2

img2 = cv.imread("Capture.png", 1)

for i in range(1,4):
    for j in range(1,4):
        startx = (square*j) + centerSpace
        endx = (square*j + 2) + centerSpace
        starty = (square*i) + centerSpace
        endy = (square*i + 2) + centerSpace
        startPoint = (startx, starty)
        endPoint = (endx, endy)
        
        color = (gradient, gradient, gradient)
        
        print(startPoint)
        
        img2 = cv.rectangle(img2, startPoint, endPoint, color, thickness)
        
        gradient += gradientChange

cv.imwrite("Edit.png", img2)


current = img[0, 0]
print(current)
print(current[0])
print(current[1])
print(current[2])
white = np.array([255, 255, 255])
print(type(white))
print(img[0][0])
#print(white == img[0][0])
truth = (white == current)
print("Truth: " + str(truth))
print("NPEqualCommand: " + str(np.array_equal(white, img[0][0])))


def inside(val, array):
    for p in array:
        if np.array_equal(p, val):
            return True
            
    return False

a = np.array([[1,1,1],[2,2,2],[3,3,3]])
b = np.array([2,2,2])
c = np.array([4,4,4])

print(inside(b,a))
print(inside(c, a))


current = np.copy(img[0][0])
pixels = np.zeros([1,3], dtype=int)
counter = 0
for row in img:
    for pixel in row:
        blackOrWhite = np.all(pixel == pixel[0])
        if not blackOrWhite:
            if not np.array_equal(pixel, current):
                current = np.copy(pixel)
                if (not inside(pixel, pixels)):
                    #print(pixel)
                    pixels = np.append(pixels, [pixel], axis=0)
                    counter += 1
                    
                    if counter < 1:
                        break

for p in pixels:
    print(p)
            

# Testing defaultClose and defaultOpen - accept cube
time.sleep(1)
robot.defaultClose()
time.sleep(1)
robot.defaultOpen()


# Testing acceptCube method
robot.acceptCube()
time.sleep(1)
robot.defaultOpen()


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
    
lst = [1,2,3,4]
lst2 = [1,2,3,4]

print(lst == lst2)

print(0xfffff)
print(bin(0xfffff))

start = 0x00000
one = 0x00001

print(bin(start))
print(bin(one))
print(bin(start | one))
print(bin((start | one) << 1))

values = [0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,1,1,1,1]

start = 0x00000
for i in range(len(values)):
    val = values[i]
    if val == 1:
        start = start | 0x00001
    if i < len(values)-1:
        start = start << 1
    
print(bin(start))

hexVersion = hex(int("00100010000001011111", 2))

print(hexVersion)
stringVersion = str(hexVersion)
print(stringVersion)

print("0x2205f" == stringVersion)

print(len("00100010000001011111"))


def listToString(lst: list):
    returnString = ""
    for item in lst:
        returnString += str(item)

    return returnString

print(listToString(values))
        


word1 = "1111"
word2 = "2223"

translation = {}

result = True

for i in range(len(word1)):
    ch1 = word1[i]
    ch2 = word2[i]
    
    if ch1 not in translation:
        if ch2 not in translation.values():
            translation[ch1] = ch2
        else:
            result = False
            break
        
    if ch2 != translation[ch1]:
        result = False
        break
    
print(result)

file = open("test.txt", "w+")
file.write("a\nb\nc\n")
file.close()
file = open("test.txt", "r")
a = file.readline().strip()
b = file.readline().strip()
print(a)
print(b)
file.close()
file = open("test.txt", "r")
c = file.readline().strip()
print(c)

people = {}
people["Jeff"] = 22
people["Emilee"] = 23
people["A"] = 1
people["B"] = 2
people["C"] = 3
people2 = people.copy()
people2["Jeff"] = 666
print(people)
print(type(people))
print(people.keys())
print(type(people.keys()))
pKeys = people.keys()
        
'''

def strangeFunction(n):
    print(n)
    if n > 2:
        strangeFunction(n-1)
        strangeFunction(n-2)
        
strangeFunction(4)

stack = []

def makeWord(word):
    pass


def modular_exp(x, y, N):
    if y == 0:
        return 1
    z = modular_exp(x, y//2, N)
    print("x:{}   y:{}   yo:{}".format(x, y, y % 2 == 1), end="   ")
    if y % 2 == 0:
        print("z:{}   rv: z^2 = {}^2 = {} mod {} = {}".format(z, z, z**2, N, z**2 % N))
        return z**2 % N
    else:
        print("z:{}   rv: x*z^2 = {}*{}^2 = {} mod {}   =   {}".format(z, x, z, x * z**2, N, x * z**2 % N))
        return x * z**2 % N
    
modular_exp(2,21,18)

a = "hello"
b = a
a += "!"
print(a)
print(b)

stack.append("J")
stack.append("e")
stack.append("f")
stack.pop()
stack.append("f")

print("".join(stack))

print(len(".................................................................................................................................................................................................."))

names = ["Jeff", "TrevDawg", "Jacob", "Brian"]

for name, i in enumerate(names):
    print(str(name) + " " + str(i))