import cv2 as cv
import numpy as np

class ImageProcessor:
    
    orange = np.array([0, 134, 254])
    red = np.array([0, 0, 254])
    green = np.array([0, 243, 0])
    yellow = np.array([0, 254, 254])
    blue = np.array([242, 0, 0])
    
    def __init__(self, path):
        self.img = cv.imread(path, 1)
        self.width, self.height, self.colors = self.img.shape
        self.square = self.width // 5
        self.halfSquare = self.square // 2
        self.quarterSquare = self.halfSquare // 2
    
    def colorValFromPixel(self, pixel):
        if np.array_equal(self.orange, pixel):
            return 0
        elif np.array_equal(self.red, pixel):
            return 1
        elif np.array_equal(self.green, pixel):
            return 2
        elif np.array_equal(self.yellow, pixel):
            return 3
        elif np.array_equal(self.blue, pixel):
            return 5


    def lString(self):
        x = self.halfSquare + self.quarterSquare
        y = self.square*3 + self.halfSquare

        string = ""

        for i in range(3):
            string += str(self.colorValFromPixel(self.img[y][x]))
            y -= self.square

        return string


    def bString(self):
        x = self.square + self.halfSquare
        y = self.halfSquare + self.quarterSquare

        string = ""

        for i in range(3):
            string += str(self.colorValFromPixel(self.img[y][x]))
            x += self.square

        return string


    def rString(self):
        x = self.square*4 + self.quarterSquare
        y = self.square + self.halfSquare

        string = ""

        for i in range(3):
            string += str(self.colorValFromPixel(self.img[y][x]))
            y += self.square

        return string


    def fString(self):
        x = self.square*3 + self.halfSquare
        y = self.square*4 + self.quarterSquare

        string = ""

        for i in range(3):
            string += str(self.colorValFromPixel(self.img[y][x]))
            x -= self.square

        return string


    def uString(self):
        string = ""

        x = self.square + self.halfSquare
        y = self.square + self.halfSquare

        shifts = [(self.square, 0), (self.square, 0), (0, self.square), (0, self.square),
                (self.square*-1, 0), (self.square*-1, 0), (0, self.square*-1), (0, self.square*-1)]

        for i in range(8):
            string += str(self.colorValFromPixel(self.img[y][x]))
            changes = shifts[i]
            x += changes[0]
            y += changes[1]

        return string


    def valuesString(self):
        returnString = ""
        returnString += self.lString()
        returnString += self.bString()
        returnString += self.rString()
        returnString += self.fString()
        returnString += self.uString()
        return returnString

