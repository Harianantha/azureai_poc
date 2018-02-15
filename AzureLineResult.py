class AzureLineResult:

    #boundingBoxValues = []
    #textVal = ''

    def __init__(self,boundingBoxValue,textValue,translatedText):
        self.boundingBoxValues =boundingBoxValue
        self.textVal=textValue
        self.translatedValue=translatedText
