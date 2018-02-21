from  PageRow import PageRow
from  AzureLineResult import AzureLineResult
from functools import reduce
from OCRResponseWord import OCRResponseWord

class PageVal:
    def __init__(self):
        self.pageRows = []

    #
#    def _init_(self,pagerows):
#      self.pageRows = pagerows

    def addpageRow(self,pagerow):
        #print('In addpageRow')
        updatedList = self.pageRows.append(pagerow)
        #self.pageRows = updatedList

    def createOrAddToPageRow(self,azureLineResult,translatedtText,sourceval):
        '''
        if(sourceval == 'HW'):
            print('In createOrAddToPageRow.Line text is%s'%azureLineResult["text"])
        else:
            print('In createOrAddToPageRow.Line bounding box is%s' % azureLineResult.boundingBox)
            print('In createOrAddToPageRow.Txt is%s' % azureLineResult.text)
        '''
        if (len(self.pageRows) == 0):
            nppagerow = PageRow()
            nppagerow.addToLine(azureLineResult,translatedtText,sourceval)
            self.addpageRow(nppagerow)
        else:
            '''
            tempMaxy=azureLineResult["boundingBox"][5]
            if(azureLineResult["boundingBox"][7] >  tempMaxy):
                tempMaxy = azureLineResult["boundingBox"][7]
            '''
            minf = lambda a,b: a if (a < b) else b

            minval = 0
            if(sourceval == 'HW'):
                minval = reduce(minf, [azureLineResult["boundingBox"][1],azureLineResult["boundingBox"][3],azureLineResult["boundingBox"][5],azureLineResult["boundingBox"][7]])
            else :
                minval = reduce(minf, [azureLineResult.boundingBox[1], azureLineResult.boundingBox[3],azureLineResult.boundingBox[5], azureLineResult.boundingBox[7]])
            maxf = lambda a,b: a if (a < b) else b

            maxval = 0
            if (sourceval == 'HW'):
                maxval = reduce(maxf, [azureLineResult["boundingBox"][5], azureLineResult["boundingBox"][7]])
            else:
                maxval = reduce(maxf, [azureLineResult.boundingBox[5], azureLineResult.boundingBox[7]])

            existingrow = 1
            selectedPageRow = None
            for pagerow in self.pageRows:
                #if(pagerow.maxY >= tempMaxy):
                ##If even the minimum is less than any rows maximum, then consider them to be in same row
                #if(pagerow.maxY >= minval):
                if(pagerow.maxY >= maxval ):

                    #selectedPageRow = pagerow
                    pagerow.addToLine(azureLineResult,translatedtText,sourceval)
                    #print("AFTER ADDING CONTENTS ARE")
                    existingrow = 0
                    #for result in  pagerow.azureLineResults:
                    #    print(result.textVal)

                    break
            #print ('existingrow %s' %existingrow)
            if (existingrow == 1):
                newpagerow=PageRow()
                newpagerow.addToLine(azureLineResult,translatedtText,sourceval)
                self.addpageRow(newpagerow)
#            else:
#                selectedPageRow.addToLine(azureLineResult)
#                resultsinrow=selectedPageRow.azureLineResults
#                print("AFTER ADDING CONTENTS ARE")
#                for result in  resultsinrow:
#                    print(result["text"])

    def printValues(self):
        i =1
        for row in self.pageRows:
            print("LINE NUMBER %s"%i)
            resultsinrow=row.azureLineResults
            for result in  resultsinrow:
                print("BoundingBox%s"%result.boundingBoxValues)
                print("text%s"%result.textVal)
                print("translatedtext%s"%result.translatedValue)
            i = i+1
