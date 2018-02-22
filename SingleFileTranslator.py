import requests,http.client, urllib.request, urllib.parse, urllib.error, base64, json,time,xml.etree.ElementTree as ET,time
from  PageVal import PageVal
from CreatePDFFile import CreatePDFFile
from HandleOCR import HandleOCR

class SingleFileTranslator:
    ###############################################
    #### Update or verify the following values. ###
    ###############################################

    # Replace the subscription_key string value with your valid subscription key.
    # subscription_key = 'b4ded92110f0496494aaa9e016e6a48e'
    subscription_key = '1afca1f57e954b318058e0311e2c1e18'
    # translation_subscription_key='7d5a83b4afff4ab9aae93122a4f28d83'
    translation_subscription_key = '5074b07cfe9f408392534c166eb1222b'

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
    #handwritten_uri = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/RecognizeText'
    handwritten_uri = 'https://eastus.api.cognitive.microsoft.com/vision/v1.0/RecognizeText'

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



    def translateFile(self,argv):
        # The URL of a JPEG image containing text.
        print ("file is:%s" %argv)
        #body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png'}"
        body = "{'url':'https://1.bp.blogspot.com/-U_3DWTsQiT4/WUo-5gpun-I/AAAAAAAA4qc/gCH286FcQOAZTM0nyDfBz-D2FJNQba3mgCLcBGAs/s1600/PicsArt_06-21-05.25.44%2B%25281%2529.jpg'}"

        try:
            # Replace the three dots below with the full file path to a JPEG image of a celebrity on your computer or network.
            print("Before opening the file")
            image = open(argv,'rb').read() # Read image file in binary mode
            millis = int(round(time.time() * 1000))

            ocrrecognizedfileName=argv.replace(".","_")+str(millis)+"_HW_translationtext.txt"
            ocr_output_filename=ocrrecognizedfileName.replace(".txt","_handwritten_response.txt")
            translatedfileName=argv.replace(".","_")+str(millis)+"_engtranslation.pdf"


            ocrrecognizedfile=open(ocrrecognizedfileName,'a')
            translatedfile=open(translatedfileName,'a')
            ocr_output_file=open(ocr_output_filename,'a')

            # Execute the REST API call and get the response.
            print("After opening the file")
            response = requests.post(url = SingleFileTranslator.handwritten_uri,headers = SingleFileTranslator.headers,params = SingleFileTranslator.params,data = image)

            #conn = http.client.HTTPSConnection(uri_base)
            #conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
            #conn.request("POST", "/vision/v1.0/RecognizeText?%s" % params, image, headers)
            #response = conn.getresponse()
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
            #conn2 = http.client.HTTPSConnection(operationLocation,port=None)
            #conn2.request("GET", "", "", "",requestHeaders)
            #response = conn2.getresponse()
            response = requests.request('GET', operationLocation, json=None, data=None, headers=SingleFileTranslator.requestHeaders, params=None)

            # 'data' contains the JSON data. The following formats the JSON data for display.
            parsed = json.loads(response.text)
            print ("Response:")
            jsonoutput = json.dumps(parsed, sort_keys=True, indent=2)
            #print (json.dumps(parsed, sort_keys=True, indent=2))

            ocr_output_file.write(jsonoutput)
            lines=parsed["recognitionResult"]["lines"]
            print("Number of lines %s" %len(lines))
            pageVal = PageVal()
            for words in lines:

            #    print(words["text"])
                if not words["text"] is None:
                    ocrrecognizedfile.write(words["text"])
                    ocrrecognizedfile.write('\n')
                    translatedtText=self.translatetext(words["text"])
                    if not translatedtText is None:
                        ocrrecognizedfile.write('--Eng:--'+translatedtText)
                        ocrrecognizedfile.write('\n')
                        pageVal.createOrAddToPageRow(words,translatedtText,'HW')

            print ('Number of ROWS in pageVal %s--PAGE VAL IS'%len(pageVal.pageRows) )
            pageVal.printValues()
            pagevallist = []

            handleocr = HandleOCR()
            handleocr.translateImage(argv,pageVal)

            pagevallist.append(pageVal)

            print ('Number of ROWS in pageVal %s--PAGE VAL IS  '% len(pageVal.pageRows))
            pageVal.printValues()
            print ('Before creating PDF')
            createPdf= CreatePDFFile()
            createPdf.createTranslatedPDF(pagevallist,translatedfileName)

            return translatedfileName


        except Exception as e:
            print('Error:')
            print(e)

    def translatetext (self,textVal):

        headers = {'Ocp-Apim-Subscription-Key': SingleFileTranslator.translation_subscription_key}
        conn = http.client.HTTPSConnection(self.translation_host)
        params = '?to=en&category=generalnn&text=' + urllib.parse.quote (textVal)

        conn.request ("GET", SingleFileTranslator.translation_path + params, None, headers)
        response = conn.getresponse ()
        responseVal = ET.fromstring(response.read ().decode("UTF-8"))
        return responseVal.text
