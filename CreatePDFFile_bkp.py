import fpdf
from  PageVal import PageVal
from  PageRow import PageRow
from  AzureLineResult import AzureLineResult
from functools import reduce
class CreatePDFFile:


    def createTranslatedPDF(self, pagevals,fileName):
        maxf = lambda a,b: a if (a > b) else b
        minf = lambda a,b: a if (a < b) else b
        pdf = fpdf.FPDF(unit = 'pt',format='Legal')
        pdf.set_font("Arial", size=12)
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
            for row in pageval.pageRows:
                content = ''
                lastXend = 0

                heightToLeave = row.minY - lastY
                print("height to leave %s"  %heightToLeave)
                if(heightToLeave < 15):
                    print("Setting default height" )
                    heightToLeave =15
                pdf.ln(h = heightToLeave)
                for lineResult in row.azureLineResults:
                    #gap = boundingBoxValues["boundingBox"][0] - lastXend
                    #pdf.cell(gap)
            #        content = content +" " +lineResult.translatedValue

                    maxval = reduce(maxf, [lineResult.boundingBoxValues[0],lineResult.boundingBoxValues[2],lineResult.boundingBoxValues[4],lineResult.boundingBoxValues[6]])

                    minval = reduce(minf, [lineResult.boundingBoxValues[0],lineResult.boundingBoxValues[2],lineResult.boundingBoxValues[4],lineResult.boundingBoxValues[6]])
                    width = minval - lastXend
                    #width = maxval -minval
                    if(width < 1):
                        width = 2
                    pdf.cell(10)
                    pdf.cell(0,  0,  lineResult.translatedValue, 0,  0)
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
            #    pdf.cell(0,  0,  content, 0,  1)
                #pdf.ln(5)
                #pdf.write(row.lineStart,content)



        pdf.output(fileName)
