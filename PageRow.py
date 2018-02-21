from  AzureLineResult import AzureLineResult
from functools import reduce
from OCRResponseWord import OCRResponseWord
class PageRow:
    def __init__(self):
        self.azureLineResults = []
        self.minY = 0
        self.maxY = 0
        self.lineEnd= 0
        self.lineStart = 0
        self.maxX = 0
        self.height=0

    #azureLineResults = []
    #minY = 0
    #maxY = 0
    def addToLine(self,azureLineResult,translatedText,recognitionsource):
            #print('Before creating addToLine in PageRow')
            wordslist = []
            #lineval = None
            if (recognitionsource == 'HW'):
                wordslist = azureLineResult["words"]
                lineval = AzureLineResult(azureLineResult["boundingBox"], azureLineResult["text"], translatedText,
                                          recognitionsource, wordslist)
            else:
                wordslist.append(azureLineResult.text)
                lineval = AzureLineResult(azureLineResult.boundingBox, azureLineResult.text, translatedText,
                                          recognitionsource, wordslist)

            #print('Before adding lineval')
            self.azureLineResults.append(lineval)
            #print('After adding lineval')
            maxf = lambda a,b: a if (a > b) else b
            maxval = 0
            if (recognitionsource == 'HW'):
                maxval = reduce(maxf, [azureLineResult["boundingBox"][1],azureLineResult["boundingBox"][3],azureLineResult["boundingBox"][5],azureLineResult["boundingBox"][7]])
            else:
                maxval = reduce(maxf, [azureLineResult.boundingBox[1], azureLineResult.boundingBox[3],azureLineResult.boundingBox[5], azureLineResult.boundingBox[7]])

            #print('maxval %s'%maxval)
            minf = lambda a,b: a if (a < b) else b

            minval =0
            if (recognitionsource == 'HW'):
                minval = reduce(minf, [azureLineResult["boundingBox"][1],azureLineResult["boundingBox"][3],azureLineResult["boundingBox"][5],azureLineResult["boundingBox"][7]])
            else :
                minval = reduce(minf, [azureLineResult.boundingBox[1], azureLineResult.boundingBox[3],azureLineResult.boundingBox[5], azureLineResult.boundingBox[7]])
           # print('minval %s' % minval)
            maxxtemp = 0
            if (recognitionsource == 'HW'):
                maxxtemp = reduce(maxf, [azureLineResult["boundingBox"][0], azureLineResult["boundingBox"][2],
                                         azureLineResult["boundingBox"][4], azureLineResult["boundingBox"][6],
                                         self.maxX])
            else:
                maxxtemp = reduce(maxf, [azureLineResult.boundingBox[0],azureLineResult.boundingBox[2],azureLineResult.boundingBox[4],azureLineResult.boundingBox[6],self.maxX])

            self.maxX = maxxtemp
            #print('self.maxX %s' %self.maxX)
            if(self.lineEnd== 0):
                if(recognitionsource == 'HW'):

                    self.lineEnd=azureLineResult["boundingBox"][2]
                    if (azureLineResult["boundingBox"][4] > self.lineEnd ):
                        self.lineEnd= azureLineResult["boundingBox"][4]
                else:
                    self.lineEnd = azureLineResult.boundingBox[2]
                    if (azureLineResult.boundingBox[4] > self.lineEnd):
                        self.lineEnd = azureLineResult.boundingBox[4]
            else:
                if (recognitionsource == 'HW'):
                    if (azureLineResult["boundingBox"][2] > self.lineEnd ):
                        self.lineEnd= azureLineResult["boundingBox"][2]
                    if (azureLineResult["boundingBox"][4] > self.lineEnd ):
                        self.lineEnd= azureLineResult["boundingBox"][4]
                else:
                    if (azureLineResult.boundingBox[2] > self.lineEnd ):
                        self.lineEnd= azureLineResult.boundingBox[2]
                    if (azureLineResult.boundingBox[4] > self.lineEnd ):
                        self.lineEnd= azureLineResult.boundingBox[4]
            #print('self.lineEnd %s' %self.lineEnd)
            if(self.lineStart== 0):
                if (recognitionsource == 'HW'):

                    self.lineStart=azureLineResult["boundingBox"][0]
                    if (azureLineResult["boundingBox"][6] < self.lineStart ):
                        self.lineStart= azureLineResult["boundingBox"][6]
                else:

                    self.lineStart = azureLineResult.boundingBox[0]
                    if (azureLineResult.boundingBox[6] < self.lineStart):
                        self.lineStart = azureLineResult.boundingBox[6]

            else:
                if (recognitionsource == 'HW'):
                    if (azureLineResult["boundingBox"][0] < self.lineStart ):
                        self.lineStart= azureLineResult["boundingBox"][0]
                    if (azureLineResult["boundingBox"][6] < self.lineStart ):
                        self.lineStart= azureLineResult["boundingBox"][6]
                else:
                    if (azureLineResult.boundingBox[0] < self.lineStart ):
                        self.lineStart= azureLineResult.boundingBox[0]
                    if (azureLineResult.boundingBox[6] < self.lineStart ):
                        self.lineStart= azureLineResult.boundingBox[6]
            #print('self.lineStart %s' % self.lineStart)

            if(self.minY == 0):
                #self.minY = azureLineResult["boundingBox"][1]
                self.minY = minval

            if (minval < self.minY):
                self.minY = minval

            if (maxval > self.maxY):
                self.maxY = maxval
            self.height = self.maxY - self.minY
           # print('self.height %s' % self.height)
            '''
            if(azureLineResult["boundingBox"][1] < self.minY):
                self.minY = azureLineResult["boundingBox"][1]
            if(azureLineResult["boundingBox"][3] < self.minY):
                self.minY = azureLineResult["boundingBox"][3]
            if(azureLineResult["boundingBox"][5] > self.maxY):
                self.maxY = azureLineResult["boundingBox"][5]
            if(azureLineResult["boundingBox"][7] > self.maxY):
                self.maxY = azureLineResult["boundingBox"][7]
            '''
