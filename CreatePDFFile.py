import fpdf
from  PageVal import PageVal
from  PageRow import PageRow
from  AzureLineResult import AzureLineResult
from functools import reduce
from OCRResponseWord import OCRResponseWord

class CreatePDFFile:


    def createTranslatedPDF(self, pagevals,fileName):
        maxf = lambda a,b: a if (a > b) else b
        minf = lambda a,b: a if (a < b) else b
        pdf = fpdf.FPDF(unit = 'pt',format='Legal')
        pdf.add_font('DejaVuSansCondensed', '', 'DejaVuSansCondensed_0.ttf', uni=True)
      #  pdf.set_font("DejaVu", size=8)
       # pdf.add_font("Cambria", uni = True)
        pdf.set_font("DejaVuSansCondensed", size=8)

        for pageval in pagevals:
            maxxvals = []
            maxYVals = []
            for rowtemp in pageval.pageRows:
                maxxvals.append (rowtemp.maxX)
                maxYVals.append (rowtemp.maxY)
            maxWidth = reduce(maxf, maxxvals)
            maxheight = reduce(maxf, maxYVals)
            heighttoset = maxheight+100
            widthtoset = maxWidth +100
            dim = (widthtoset,heighttoset)
            #pdf.add_page(dim)
            pdf.add_page()
            lineEnd =0
            space = 0
            #pageRowEntries = pageval.pageRows
            lastY = 0
            rownum =1
            rowvals = pageval.pageRows
            rowvals.sort(key=lambda rowval: rowval.minY)
            #for row in pageval.pageRows:
            for row in rowvals:
                content = ''
                lastXend = 0
                print('In row %s' %rownum)
                if (lastY == 0):
                    heightToLeave = 15
                else:
                    heightToLeave = row.minY - lastY
                #print("height to leave %s"  %heightToLeave)
                if(heightToLeave < 15):
                #    print("Setting default height" )
                    heightToLeave =15
                if(heightToLeave > 100):
                #    print("Restrciting maximum height" )
                    heightToLeave =100
                print('heightToLeave %s'%heightToLeave)
                pdf.ln(h = heightToLeave)

                lineresults = row.azureLineResults
                '''
                print('lineresults count IS%s' % lineresults.count)
                uniquevalset=set(lineresults)
              #  print('SET IS%s'%uniquevalset)

                uniquevals = list(uniquevalset)
               # print('LIST IS%s' %uniquevals)
                print('LIST count IS%s' % uniquevals.count)
                uniquevals.sort(key=lambda uniqueval:uniqueval.minxval)
                '''
                lstHWlist= list(filter(lambda result: result.recognitionsource == 'HW' , lineresults))
                listOCRlist = list(filter(lambda result: result.recognitionsource == 'OCR' , lineresults))

                deltaocrlist = []

                for ocrResult in listOCRlist:
                    addToList = True
                    for hwlist in lstHWlist:
                        startxdiff = ocrResult.boundingBoxValues[0] - hwlist.boundingBoxValues[0]
                        startydiff = ocrResult.boundingBoxValues[1] - hwlist.boundingBoxValues[1]
                        endxdiff = ocrResult.boundingBoxValues[6] - hwlist.boundingBoxValues[6]
                        endydiff = ocrResult.boundingBoxValues[7] - hwlist.boundingBoxValues[7]
                        #print('STARTXDIFF %s' % startxdiff)
                        #print('startydiff %s' % startydiff)
                        #print('endxdiff %s' % endxdiff)
                        #print('endydiff %s' % endydiff)
                        if ((abs(startxdiff) < 11 and abs(startydiff) < 11 and abs(endxdiff) < 11 and abs(endydiff) < 11) or (ocrResult.textVal in hwlist.textVal)):
                            addToList = False
                            break
                    if addToList:
                        deltaocrlist.append(ocrResult)

                lstHWlist.extend(deltaocrlist)

                lstHWlist.sort(key=lambda listentry: listentry.minxval)
                #for lineResult in row.azureLineResults:
                for lineResult in lstHWlist:
                    #gap = boundingBoxValues["boundingBox"][0] - lastXend
                    #pdf.cell(gap)
                    if (lineResult is None):
                        print ('Line Result is None')
                    if not lineResult.translatedValue is None:

                        content = content +" " +lineResult.translatedValue

                    valuestocompare = []



                    maxval = reduce(maxf, [lineResult.boundingBoxValues[0],lineResult.boundingBoxValues[2],lineResult.boundingBoxValues[4],lineResult.boundingBoxValues[6]])

                    minval = reduce(minf, [lineResult.boundingBoxValues[0],lineResult.boundingBoxValues[2],lineResult.boundingBoxValues[4],lineResult.boundingBoxValues[6]])
                    #width = minval - lastXend
                    width = maxval -minval
                    diff = minval - lastXend
                    if(width < 1):
                        width = 2
                    if(diff < 1):
                        diff = 2
                    #pdf.cell(diff)
                    #pdf.cell(width,  0,  lineResult.translatedValue, 0,  0)

                    lastXend = maxval



                if (row.maxY > lastY + 14):

                    lastY = row.maxY
                else:
                    lastY = lastY + 15
            #    print ('Content is %s' %content)
                #print ('minY is %s' %row.minY)
                #print ('lastY is %s' %lastY)

            #    print ('Space is %s' %space)

                if (space < 1):
                    space = 1
                #    print ('Space set to 1')
                space =  row.lineStart - lineEnd;
                lineEnd =  row.lineEnd;
                #pdf.ln(1)
            #    pdf.cell(space)
                #pdf.multi_cell(0, 0,content, 0,'L')
                pdf.cell(0,  0,  content, 0,  1)
            #    pdf.write( content)
        #        pdf.ln(h = '15')

                #pdf.ln(5)
                #pdf.write(row.lineStart,content)

                rownum= rownum+1

        pdf.output(fileName)
