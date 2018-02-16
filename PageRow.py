from  AzureLineResult import AzureLineResult
from functools import reduce

class PageRow:
    def __init__(self):
        self.azureLineResults = []
        self.minY = 0
        self.maxY = 0
        self.lineEnd= 0
        self.lineStart = 0

    #azureLineResults = []
    #minY = 0
    #maxY = 0
    def addToLine(self,azureLineResult,translatedText):
            #print('Before creating lineval')
            lineval = AzureLineResult(azureLineResult["boundingBox"],azureLineResult["text"],translatedText)
            #print('After creating lineval')
            self.azureLineResults.append(lineval)

            maxf = lambda a,b: a if (a > b) else b
            maxval = reduce(maxf, [azureLineResult["boundingBox"][1],azureLineResult["boundingBox"][3],azureLineResult["boundingBox"][5],azureLineResult["boundingBox"][7]])
            minf = lambda a,b: a if (a < b) else b
            minval = reduce(minf, [azureLineResult["boundingBox"][1],azureLineResult["boundingBox"][3],azureLineResult["boundingBox"][5],azureLineResult["boundingBox"][7]])

            if(self.lineEnd== 0):

                self.lineEnd=azureLineResult["boundingBox"][2]
                if (azureLineResult["boundingBox"][4] > self.lineEnd ):
                    self.lineEnd= azureLineResult["boundingBox"][4]
            else:
                if (azureLineResult["boundingBox"][2] > self.lineEnd ):
                    self.lineEnd= azureLineResult["boundingBox"][2]
                if (azureLineResult["boundingBox"][4] > self.lineEnd ):
                    self.lineEnd= azureLineResult["boundingBox"][4]

            if(self.lineStart== 0):

                self.lineStart=azureLineResult["boundingBox"][0]
                if (azureLineResult["boundingBox"][6] < self.lineStart ):
                    self.lineStart= azureLineResult["boundingBox"][6]
            else:
                if (azureLineResult["boundingBox"][0] < self.lineStart ):
                    self.lineStart= azureLineResult["boundingBox"][0]
                if (azureLineResult["boundingBox"][6] < self.lineStart ):
                    self.lineStart= azureLineResult["boundingBox"][6]


            if(self.minY == 0):
                #self.minY = azureLineResult["boundingBox"][1]
                self.minY = minval

            if (minval < self.minY):
                self.minY = minval

            if (maxval > self.maxY):
                self.maxY = maxval
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
