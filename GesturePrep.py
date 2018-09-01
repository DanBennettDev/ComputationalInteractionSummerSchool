import numpy
import math
# array processing functions

class GesturePrep(object):
    def __init__(self):
        return none


        
    def getInterpolationDistribution(lenData, lenArray):
        interpCount = max(0, lenArray - lenData)
        # start with all the interpolations
        distribution = numpy.ones(lenData)
        i = 0
        currentSum = lenData
        while currentSum < lenArray:
            i=0
            while i < lenData and currentSum < lenArray:
                distribution[i] += 1
                currentSum += 1
                interpCount -=1
                i+=1            
        theSum = 0
        for v in distribution:
            theSum += v
        return distribution


    def lerp(a, b, t):
        af = (float(a[0]), float(a[1]))
        bf = (float(b[0]), float(b[1]))
        x =  af[0] + t * (bf[0] - af[0]);
        y =  af[1] + t * (bf[1] - af[1]);
        return numpy.array([x,y])


    def addInterpolations(inputData):
        processedArray = numpy.zeros([512, 2])

        interpDistribution = getInterpolationDistribution(len(inputData), 512)    
        iProcessed = 0
        iInput = 0
        div = 0
        
        for interp in interpDistribution:
            while interp > 0:
                if interp > 1:
                    if interp > div:
                        div = float(interp)
                    # interpolate
                    a=0
                    b=0
                    if iInput==0:
                        a=inputData[0]
                        b=inputData[0]
                    elif iInput >= len(inputData)-1:
                        a=inputData[len(inputData)-2]
                        b=inputData[len(inputData)-1]    
                    else :
                        a = inputData[iInput - 1]
                        b = inputData[iInput]
                    processedArray[iProcessed] = lerp(a,b, (div-interp)/div)
                else:
                    # take next value from input
                    processedArray[iProcessed] = inputData[iInput]
                    iInput += 1
                interp -= 1
                iProcessed += 1

        return processedArray



    def vectorise(src):
        # normalise the input image
        maxVal = 0.0
        for element in src:
            if abs(element[0]) > maxVal:
                maxVal = math.fabs(element[0])
            if abs(element[1]) > maxVal:
                maxVal = math.fabs(element[1])

        normalised = numpy.zeros([len(src),2])       
        for i, element in enumerate(src):
            normalised[i] = numpy.array([element[0] / maxVal,element[1] / maxVal])

        # calculate the vectors
        vectorised = numpy.zeros(len(src)*2)   

        for i, element in enumerate(normalised):
            if i < len(src)-1:
                vectorised[i*2] = normalised[i][0] - normalised[i+1][0]
                vectorised[(i*2) + 1] = normalised[i][1] - normalised[i+1][1]  
        return vectorised