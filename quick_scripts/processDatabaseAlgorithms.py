from imageProcessor import ImageProcessor

import os
from cube import Cube

path = "PLLPictures/"
files = os.listdir(path)
result = []
for file in files:
    imageProcessor = ImageProcessor(path+file)
    
    valueString = imageProcessor.valuesString()
    result.append(valueString)
    startIndex = file.find(" ")+1
    endIndex = file.find(".")
    algorithm = file[startIndex:endIndex]
    result.append(algorithm)
    
    cube = Cube()
    uNormalValueString = cube.rotateTopValues(valueString)
    uNormalAlgorithm = "U' " + algorithm
    result.append(uNormalValueString)
    result.append(uNormalAlgorithm)
    
    u2ValueString = cube.rotateTopValues(uNormalValueString)
    u2Algorithm = "U2 " + algorithm
    result.append(u2ValueString)
    result.append(u2Algorithm)
    
    uPrimeValueString = cube.rotateTopValues(u2ValueString)
    uPrimeAlgorithm = "U " + algorithm
    result.append(uPrimeValueString)
    result.append(uPrimeAlgorithm)
    

with open("PLL.txt", "a+") as file:
    for line in result:
        file.write(line + "\n")
        


    
