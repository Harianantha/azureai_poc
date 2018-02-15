from  AzureLineResult import AzureLineResult

class PageRow:
    def __init__(self):
        self.azureLineResults = []
        self.minY = 0
        self.maxY = 0

    #azureLineResults = []
    #minY = 0
    #maxY = 0
    def addToLine(self,azureLineResult,translatedText):
            #print('Before creating lineval')
            lineval = AzureLineResult(azureLineResult["boundingBox"],azureLineResult["text"],translatedText)
            #print('After creating lineval')
            self.azureLineResults.append(lineval)
            if(azureLineResult["boundingBox"][1] < self.minY):
                self.minY = azureLineResult["boundingBox"][1]
            if(azureLineResult["boundingBox"][3] < self.minY):
                self.minY = azureLineResult["boundingBox"][3]
            if(azureLineResult["boundingBox"][5] > self.maxY):
                self.maxY = azureLineResult["boundingBox"][5]
            if(azureLineResult["boundingBox"][7] > self.maxY):
                self.maxY = azureLineResult["boundingBox"][7]
