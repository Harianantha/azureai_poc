from functools import reduce
class AzureLineResult:

    #boundingBoxValues = []
    #textVal = ''

    minf = lambda a, b: a if (a < b) else b
    def __init__(self,boundingBoxValue,textValue,translatedText,sourceval,wordslist):
        self.boundingBoxValues =boundingBoxValue
        self.textVal=textValue
        self.translatedValue=translatedText
        self.recognitionsource = sourceval
        self.wordslist = wordslist
        self.minxval=reduce(AzureLineResult.minf, [self.boundingBoxValues[0], self.boundingBoxValues[2],self.boundingBoxValues[4], self.boundingBoxValues[6]])

    def __eq__(self, other):
        print('In SELF Method')
        if(self.recognitionsource == 'HW'):
            print ('Returning FALSE as source is HW ')
            return False

        if(self.recognitionsource == 'OCR' and other.recognitionsource == 'HW'):

            startxdiff =  self.boundingBoxValues[0] - other.boundingBoxValues[0]
            startydiff = self.boundingBoxValues[1] - other.boundingBoxValues[1]
            endxdiff= self.boundingBoxValues[6] - other.boundingBoxValues[6]
            endydiff = self.boundingBoxValues[7] - other.boundingBoxValues[7]

            print('STARTXDIFF %s'%startxdiff)
            print('startydiff %s'%startydiff)
            print('endxdiff %s'%endxdiff)
            print('endydiff %s'%endydiff)
            if(abs(startxdiff) <11 and abs(startydiff) <11 and abs(endxdiff) <11 and abs(endydiff) <11):
                print ('Returning true %s  %s'%self.textVal %other.textVal)
                return True
            else:
                print ('Returning FALSE as LIMIT exceeds ')
                return False

        else:
            print ('Returning BASED ON VAL')
            return other.textVal == self.textVal



    def __hash__(self):
        print('In HASH Method')
        return hash(('textVal', self.textVal))
