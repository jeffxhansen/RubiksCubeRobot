import cv2 as cv
import numpy as np
from numpy.linalg import norm
from math import sqrt
import pigpio
from time import sleep

class Lights:
    
    def __init__(self):
        self.pi = pigpio.pi()
        
    def getBrightness(self):
        return self.pi.get_PWM_dutycycle(4)
        
    def setBrightness(self, val):
        
        curr = self.pi.get_PWM_dutycycle(4)
        
        step = 1 if curr < val else -1
        
        for i in range(curr, val+step, step):
            self.pi.set_PWM_dutycycle(4, i)
            sleep(0.002)

class CameraSensor:
    
    SIDE_ORDER = ["L", "R", "B", "U", "D", "F"]

    def __init__(self):
        capture = cv.VideoCapture(0)
        ret, frame = capture.read()
        self.camHeight, self.camWidth, self.camColors = frame.shape
        capture.release()

        self.cubeDim = 294
        self.startPoint = None
        self.endPoint = None
        self.initPoints()

        self.cubies = []
        self.initCubies()
        
        self.coreColors = []
        self.initCoreColors()
        self.colorKey = {"r":0, "o":1, "y":2, "g":3, "b":4, "w":5}
        
        self.lights = Lights()

    def initPoints(self):
        xShift = -24
        yShift = 10
        startX = (self.camWidth // 2) - (self.cubeDim // 2) + xShift
        startY = (self.camHeight // 2) - (self.cubeDim // 2) + yShift
        endX = startX + self.cubeDim
        endY = startY + self.cubeDim
        self.startPoint = (startX, startY)
        self.endPoint = (endX, endY)

    def initCubies(self):
        cubieDim = self.cubeDim // 3

        sxShift = 8
        syShift = 8
        exShift = -12
        eyShift = -12

        for i in range(3):
            for j in range(3):
                sX = self.startPoint[0] + j*cubieDim + sxShift
                sY = self.startPoint[1] + i*cubieDim + syShift
                eX = self.startPoint[0] + (j+1)*cubieDim + exShift
                eY = self.startPoint[1] + (i+1)*cubieDim + eyShift
                sPoint = (sX, sY)
                ePoint = (eX, eY)
                self.cubies.append([sPoint, ePoint])
            sxShift += 4
            syShift += 2
            exShift += 4
            eyShift += 2
            
    def initCoreColors(self, colors=None):

        '''
        RED = np.array([40,40,120])/255
        ORANGE = np.array([100,140,200])/255
        YELLOW = np.array([100,200,220])/255
        GREEN = np.array([100,170,80])/255
        BLUE = np.array([175,120,50])/255
        WHITE = np.array([200, 200, 200])/255
        self.coreColors = [RED/norm(RED), ORANGE/norm(ORANGE), 
                           YELLOW/norm(YELLOW), GREEN/norm(GREEN), 
                           BLUE/norm(BLUE), WHITE/norm(WHITE)]
        '''
        
        RED = np.array([120,120,240])
        ORANGE = np.array([90,170,250])
        YELLOW = np.array([95,215,180])
        GREEN = np.array([125,225,85])
        BLUE = np.array([210,115,50])
        WHITE = np.array([205, 205, 190])
        self.coreColors = [RED, ORANGE, YELLOW, GREEN, BLUE, WHITE]
        
        self.reds = np.array(RED)
        self.oranges = np.array(ORANGE)
        self.yellows = np.array(YELLOW)
        self.greens = np.array(GREEN)
        self.blues = np.array(BLUE)
        self.whites = np.array(WHITE)
        
        '''
        RED = np.array([5.97083801, 157.63980131,  89.28440955])
        ORANGE = np.array([11.45890082, 162.49110719, 106.24274956])
        YELLOW = np.array([39.14821343, 119.77695882,  85.41884313])
        GREEN = np.array([84.52491588, 101.74315014, 124.51610319])
        BLUE = np.array([120.1559045, 146.61528601,  37.20781926])
        WHITE = np.array([27.47828874,   4.92228809, 128.4619452])
        self.coreColors = [RED, ORANGE, YELLOW, GREEN, BLUE, WHITE]
        '''
        
    def updateColorOrientation(self, coreColors:dict, order:list):
        # test this method
        colors = ["r", "o", "y", "g", "b", "w"]
        
        self.colorArrays = list()
        for c in colors:
            index = order.index(c)
            key = self.SIDE_ORDER[index]
            pixelVal = coreColors[key]/norm(coreColors[key])
            self.colorArrays.append(pixelVal)
        
        for i, o in enumerate(order):
            self.colorKey[o] = i
            
    def updateOranges(self):
        avgOrange = np.average(self.oranges, axis=0)
        normalizedOrange = avgOrange/255
        normalizedOrange /= norm(normalizedOrange)
        self.coreColors[1] = normalizedOrange

    def streamWebcamVideo(self):
        videoCaptureObject = cv.VideoCapture(1)
        while(True):
            ret, frame = videoCaptureObject.read()
            cv.imshow('Capturing Video', frame)
            if(cv.waitKey(1) & 0xFF == ord('q')):
                videoCaptureObject.release()
                cv.destroyAllWindows()

    def printWebcamProps(self, capture=None):
        if capture == None:
            capture = cv.VideoCapture(1)
        print("CV_CAP_PROP_FRAME_WIDTH : '{}'".format(
            capture.get(cv.CAP_PROP_FRAME_WIDTH)))
        print("CV_CAP_PROP_FRAME_HEIGHT : '{}'".format(
            capture.get(cv.CAP_PROP_FRAME_HEIGHT)))
        print("CAP_PROP_BRIGHTNESS : '{}'".format(
            capture.get(cv.CAP_PROP_BRIGHTNESS)))
        print("CAP_PROP_CONTRAST : '{}'".format(
            capture.get(cv.CAP_PROP_CONTRAST)))
        print("CAP_PROP_SATURATION : '{}'".format(
            capture.get(cv.CAP_PROP_SATURATION)))
        print("CAP_PROP_EXPOSURE : '{}'".format(
            capture.get(cv.CAP_PROP_EXPOSURE)))
        print("CAP_PROP_HUE : '{}'".format(capture.get(cv.CAP_PROP_HUE)))
        print("CAP_PROP_SHARPNESS : '{}'".format(
            capture.get(cv.CAP_PROP_SHARPNESS)))
        print("CAP_PROP_AUTO_EXPOSURE : '{}'".format(
            capture.get(cv.CAP_PROP_AUTO_EXPOSURE)))
        print("CAP_PROP_TEMPERATURE : '{}'".format(
            capture.get(cv.CAP_PROP_TEMPERATURE)))
        print("CAP_PROP_ZOOM : '{}'".format(capture.get(cv.CAP_PROP_ZOOM)))
        print("CAP_PROP_FOCUS : '{}'".format(capture.get(cv.CAP_PROP_FOCUS)))
        print("CAP_PROP_AUTOFOCUS : '{}'".format(
            capture.get(cv.CAP_PROP_AUTOFOCUS)))
        print("CAP_PROP_ZOOM : '{}'".format(capture.get(cv.CAP_PROP_ZOOM)))
        
    def enhancePicture(self, img):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV) # convert image to HSV color space
        hsv = np.array(hsv, dtype = np.float64)
        hsv[:,:,0] = hsv[:,:,0]*1.25 # scale pixel values up for channel 0
        hsv[:,:,0][hsv[:,:,0]>255]  = 255
        hsv[:,:,1] = hsv[:,:,1]*1 # scale pixel values up for channel 1
        hsv[:,:,1][hsv[:,:,1]>255]  = 255
        hsv[:,:,2] = hsv[:,:,2]*1 # scale pixel values up for channel 2
        hsv[:,:,2][hsv[:,:,2]>255]  = 255
        hsv = np.array(hsv, dtype = np.uint8)
        # converting back to BGR used by OpenCV
        img = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        return img
    
    def convertToHSV(self, img):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV) # convert image to HSV color space
        hsv = np.array(hsv, dtype = np.float64)
        return hsv
    
    def referencePicture(self):
        capture = cv.VideoCapture(0)
        ret, img = capture.read()
        
        area = [(5, 150), (95, 210)]
        leftArea = img[area[0][1]:area[1][1]+1, area[0][0]:area[1][0]+1]
        redAverage = np.average(np.average(leftArea, axis=1), axis=0)
        area = [(505,150), (595,210)]
        rightArea = img[area[0][1]:area[1][1]+1, area[0][0]:area[1][0]+1]
        orangeAverage = np.average(np.average(rightArea, axis=1), axis=0)
        
        '''
        redAverage /= 255
        redAverage /= norm(redAverage)
        orangeAverage /= 255
        orangeAverage /= norm(orangeAverage)
        '''
        
        self.coreColors[0] = redAverage
        self.coreColors[1] = orangeAverage
        capture.release()

    def takePicture(self, name, brightness=0):
        
        if brightness != 0:
            self.lights.setBrightness(brightness)
        
        capture = cv.VideoCapture(0)
        ret, frame = capture.read()
        #frame = self.enhancePicture(frame)
        cv.imwrite(name, frame)
        self.largeBox(name)
        capture.release()

    def largeBox(self, name):
        color = (255, 50, 50)
        edit = cv.imread(name, 1)
        edit = cv.rectangle(edit, self.startPoint, self.endPoint, color, 2)
        cv.imwrite(name[:-4] + "Edit" + name[-4:], edit)

    def smallBoxes(self, name, edit):
        orig = cv.imread(name, 1)

        color = (50, 255, 50)
        for c in self.cubies:
            orig = cv.rectangle(orig, c[0], c[1], color, 1)
        cv.imwrite(edit, orig)

    def drawBoxes(self):
        original = "./webcam/ToEdit.jpg"
        self.takePicture(original)
        self.largeBox(original)
        self.smallBoxes(original, "./webcam/smallBoxes.jpg")
        print(self.cubies)
        
    def sum_similarity(self, a, b):
        #a = a/norm(a)
        #b = b/norm(b)
        result = abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])
        result = -result
        return result

    def cosine_similarity(self, a, b):
        return np.dot(a, b)/(norm(a)*norm(b))
    
    def euclidean_similarity(self, a, b):
        return sqrt(sum(pow(x-y,2) for x, y in zip(a, b)))
    
    def dot_product_similarity(self, a, b):
        return np.dot(a, b)

    def averages(self, file: str):
        img = cv.imread(file, 1)
        #img = self.convertToHSV(img)
        averages = []
        for area in self.cubies:
            subImg = img[area[0][1]:area[1][1]+1, area[0][0]:area[1][0]+1]
            avgPixel = np.average(np.average(subImg, axis=1), axis=0)
            averages.append(avgPixel)

        return averages
    
    def averages2(self, file: str):
        img = cv.imread(file, 1)
        #img = self.convertToHSV(img)
        averages = []
        for area in self.cubies:
            subImg = img[area[0][1]:area[1][1]+1, area[0][0]:area[1][0]+1]
            avgPixel = np.average(np.average(subImg, axis=1), axis=0)
            averages.append(avgPixel)

        return averages
    
    def updateColors(self, color, pixel):
        if color == "w":
            print("White Updated:")
            print(self.whites)
            self.whites = np.append([self.whites], [pixel], axis=0)
            self.whites = np.average(self.whites, axis=0)
            print(self.whites, end="\n\n")
            #self.coreColors[5] = self.whites
        elif color == "r":
            print("Red Updated:")
            print(self.reds)
            self.reds = np.append([self.reds], [pixel], axis=0)
            self.reds = np.average(self.reds, axis=0)
            print(self.reds, end="\n\n")
            #self.coreColors[0] = self.reds
        elif color == "o":
            print("Orange Updated:")
            print(self.oranges)
            self.oranges = np.append([self.oranges], [pixel], axis=0)
            self.oranges = np.average(self.oranges, axis=0)
            print(self.oranges, end="\n\n")
            #self.coreColors[1] = self.oranges
        elif color == "y":
            print("Yellow Updated:")
            print(self.yellows)
            self.yellows = np.append([self.yellows], [pixel], axis=0)
            self.yellows = np.average(self.yellows, axis=0)
            print(self.yellows, end="\n\n")
            #self.coreColors[2] = self.yellows
        elif color == "g":
            print("Green Updated:")
            print(self.greens)
            self.greens = np.append([self.greens], [pixel], axis=0)
            self.greens = np.average(self.greens, axis=0)
            print(self.greens, end="\n\n")
            #self.coreColors[3] = self.greens
        elif color == "b":
            print("Blue Updated:")
            print(self.blues)
            self.blues = np.append([self.blues], [pixel], axis=0)
            self.blues = np.average(self.blues, axis=0)
            print(self.blues, end="\n\n")
            #self.coreColors[4] = self.blues
            
    def printColorAverages(self):
        print("R: {}".format(self.reds))
        print("O: {}".format(self.oranges))
        print("Y: {}".format(self.yellows))
        print("G: {}".format(self.greens))
        print("B: {}".format(self.blues))
        print("W: {}".format(self.whites))
        
    
    def getColor(self, pixel):
        colors = ["r", "o", "y", "g", "b", "w"]
        #pixel /= 255
        max = -float('inf')
        index = 0
        similarities = []
        for i, c in enumerate(self.coreColors):
            #similarity = self.euclidean_similarity(pixel, c)
            #similarity = self.cosine_similarity(pixel/norm(pixel), c/norm(c))
            similarity = self.sum_similarity(pixel, c)
            #similarity = self.cosine_similarity(pixel, c)
            #similarity = self.dot_product_similarity(pixel, c)
            #print("sim: {}-{} is {}".format(pixel, c, similarity))
            similarities.append(tuple([pixel, c, similarity, colors[i]]))
            if similarity > max:
                index = i
                max = similarity
        '''      
        if index == 1:
            self.oranges.append(pixel)
            self.updateOranges()
        '''
        for t in similarities:
            print(t)
        print()
        returnColor = colors[index]
        self.updateColors(returnColor, pixel)
        '''
        if returnColor == "r" or returnColor == "o":
            pixelG = pixel[1]
            redG = self.coreColors[0][1]
            orangeG = self.coreColors[1][1]
            
            redRate = abs(pixelG-redG)
            orangeRate = abs(pixelG-orangeG)
            if redRate > orangeRate:
                returnColor = "o"
            else:
                returnColor = "r"
        '''
        #print(returnColor, end="\n\n")
        return returnColor
    
    def reorderVals(self, vals):
        final = [0 for i in range(48)]
        order = [4,5,6,3,-1,7,2,1,0,
                 14,15,8,13,-1,9,12,11,10,
                 20,21,22,19,-1,23,18,17,16,
                 28,29,30,27,-1,31,26,25,24,
                 32,33,34,39,-1,35,38,37,36,
                 40,41,42,47,-1,43,46,45,44]
        
        lefts = 0
        rights = 0
        backs = 0
        ups = 0
        downs = 0
        fronts = 0
        for i, val in enumerate(vals):
            if order[i] != -1:
                final[order[i]] = val
                if val == 0:
                    lefts += 1
                elif val == 1:
                    rights += 1
                elif val == 2:
                    backs += 1
                elif val == 3:
                    ups += 1
                elif val == 4:
                    downs += 1
                elif val == 5:
                    fronts += 1

        print("lefts: {} \nrights: {} \nbacks: {} \nups: {} \ndowns: {} \nfronts: {}"\
            .format(lefts, rights, backs, ups, downs, fronts))
        
        self.printColorAverages()
        input("Stop here")
        
        if lefts != rights and rights != backs and \
            backs != ups and ups != downs and \
            downs != fronts and fronts != lefts:
            input("Error!!")
        
        return final
    
    def getValues(self, files):
        faceVals = []
        corePixels = {}
        coreColors = []
        
        sides_seen = set()
        count = 1
        for file in files:
            side = file[9]
            
            if side not in sides_seen:
                print(side)
                averages = self.averages(file)
                faceVals += averages
                corePixels[file[9]] = averages[4]
                print("center color: {}".format(averages[4]))
                color = self.getColor(averages[4])
                coreColors.append(color)
                sides_seen.add(side)
        
        print(corePixels)
        print(coreColors)
        input("stop here")
        self.updateColorOrientation(corePixels, coreColors)
        for i, val in enumerate(faceVals):
            key = self.getColor(val)
            val = self.colorKey[key]
            faceVals[i] = val # JEFF: switch to KEY for debugging
                
        
        print(corePixels)
        print(faceVals)
        
        returnVals = self.reorderVals(faceVals)
        
        return coreColors, returnVals
            
