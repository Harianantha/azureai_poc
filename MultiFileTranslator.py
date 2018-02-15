import requests,http.client, urllib.request, urllib.parse, urllib.error, base64, json,time,xml.etree.ElementTree as ET,os,fitz
from PIL import Image
from  PageVal import PageVal
from CreatePDFFile import CreatePDFFile

class MultiFileTranslator:
    ###############################################
    #### Update or verify the following values. ###
    ###############################################

    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = 'b4ded92110f0496494aaa9e016e6a48e'
    translation_subscription_key='7d5a83b4afff4ab9aae93122a4f28d83'

    translation_host = 'api.microsofttranslator.com'
    translation_path = '/V2/Http.svc/Translate'


    # Replace or verify the region.
    #
    # You must use the same region in your REST API call as you used to obtain your subscription keys.
    # For example, if you obtained your subscription keys from the westus region, replace
    # "westcentralus" in the URI below with "westus".
    #
    # NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
    # a free trial subscription key, you should not need to change this region.
    #uri_base = 'westcentralus.api.cognitive.microsoft.com/vision/v1.0/ocr'
    uri_base = 'westcentralus.api.cognitive.microsoft.com'
    handwritten_uri = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/RecognizeText'

    headers = {
        # Request headers.
        #'Content-Type': 'application/json',
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    requestHeaders = {
        # Request headers.
        # Another valid content type is "application/octet-stream".
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }


    params = urllib.parse.urlencode({
        # Request parameters. The language setting "unk" means automatically detect the language.
        'language': 'unk',
        'detectOrientation ': 'true',
    })



    def translateFile(self,fileNameInput):
        # The URL of a JPEG image containing text.
        print ("file is:%s" %fileNameInput)
        #body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png'}"
        body = "{'url':'https://1.bp.blogspot.com/-U_3DWTsQiT4/WUo-5gpun-I/AAAAAAAA4qc/gCH286FcQOAZTM0nyDfBz-D2FJNQba3mgCLcBGAs/s1600/PicsArt_06-21-05.25.44%2B%25281%2529.jpg'}"

        try:
            # Replace the three dots below with the full file path to a JPEG image of a celebrity on your computer or network.



            # Execute the REST API call and get the response.

            splitfilelist = []
            if(fileNameInput.endswith('.tif')):
                splitfilelist = self.parse_tif(fileNameInput)

            if (fileNameInput.endswith('.pdf')):
                splitfilelist = self.splitPdfToPNG(fileNameInput)

            millis = int(round(time.time() * 1000))
            ocrrecognizedfileName=fileNameInput.replace(".","_")+str(millis)+"_ocrtext.doc"

            translatedfileName=fileNameInput.replace(".","_")+str(millis)+"_engtranslation.pdf"

            ocrrecognizedfile=open(ocrrecognizedfileName,'a')
            translatedfile=open(translatedfileName,'a')

            pagevallist = []
            print("After splitting the file")
            for filename in splitfilelist:
                pageVal = PageVal()
                print("Before opening the file %s" %filename)
                image = open(filename,'rb').read() # Read image file in binary mode
                print("After opening the file")
                response = requests.post(url = MultiFileTranslator.handwritten_uri,headers = MultiFileTranslator.headers,params = MultiFileTranslator.params,data = image)


                if response.status_code != 202:
                    # if the first REST API call was not successful, display JSON data and exit.
                    parsed = json.loads(response.text)
                    print ("Error:")
                    print (json.dumps(parsed, sort_keys=True, indent=2))
                    exit()
                operationLocation = response.headers['Operation-Location']

                #conn.close()
                print('\nHandwritten text submitted. Waiting 10 seconds to retrieve the recognized text.\n')
                time.sleep(10)
                print('Operation location:%s' %operationLocation )

                # Execute the second REST API call and get the response.

                response = requests.request('GET', operationLocation, json=None, data=None, headers=MultiFileTranslator.requestHeaders, params=None)

                # 'data' contains the JSON data. The following formats the JSON data for display.
                parsed = json.loads(response.text)
                print ("Response:")
                print (json.dumps(parsed, sort_keys=True, indent=2))
                lines=parsed["recognitionResult"]["lines"]
                print("Number of lines %s" %len(lines))
                for words in lines:
                    print(words["text"])
                    if not words["text"] is None:
                        ocrrecognizedfile.write(words["text"])
                        ocrrecognizedfile.write('\n')
                        translatedtText=self.translatetext(words["text"])
                        if not translatedtText is None:
                            #translatedfile.write(translatedtText)
                            #translatedfile.write('\n')
                            pageVal.createOrAddToPageRow(words,translatedtText)
                            print('-----------English translation is %s' %translatedtText)
                pagevallist.append(pageVal)
            createPdf= CreatePDFFile()
            createPdf.createTranslatedPDF(pagevallist,translatedfileName)
            return translatedfileName


        except Exception as e:
            translatedfile.write('Due to Exception, translation could not be completed successfully. Please contact the technical team for more details.')
            ocrrecognizedfile.write('Due to Exception, recognition could not be completed successfully. Please contact the technical team for more details.')
            print('Error:')
            print(e)


    def translatetext (self,textVal):

        headers = {'Ocp-Apim-Subscription-Key': MultiFileTranslator.translation_subscription_key}
        conn = http.client.HTTPSConnection(MultiFileTranslator.translation_host)
        params = '?to=en&category=generalnn&text=' + urllib.parse.quote (textVal)

        conn.request ("GET", MultiFileTranslator.translation_path + params, None, headers)
        response = conn.getresponse ()
        responseVal = ET.fromstring(response.read ().decode("UTF-8"))
        return responseVal.text

    def parse_tif(self,filePath):
        img = Image.open(filePath)
        numFramesPerTif = 5
        n = 0
        file, ext = os.path.splitext(filePath)
        filelist = []
        while True:
            try:
                img.seek(n)
                img.save(file+'Block_%s.png'%(n,))
                filelist.append(file+'Block_%s.png'%n)
                n = n +1
            except EOFError:
                print ("Got EOF error when I tried to load %s"  %n)
                break;
        return filelist;

    def splitPdfToPNG(self,argv):
        doc = fitz.open(argv)


        file, ext = os.path.splitext(argv)
        filelist = []
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:       # this is GRAY or RGB
                    pix.writePNG(file+"p%s-%s.png" % (i, xref))
                    filelist.append(file+"p%s-%s.png" % (i, xref))
                else:               # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG(file+"p%s-%s.png" % (i, xref))
                    filelist.append(file+"p%s-%s.png" % (i, xref))
                    pix1 = None
                pix = None
        return filelist;

        #for i in range (numFramesPerTif)
        #    try:
        #        img.seek(i)
        #        img.save('Block_%s.tif'%(i,))
        #    except EOFError:

#
#    if __name__ == "__main__":
#        from sys import argv
#        main(argv)

####################################
