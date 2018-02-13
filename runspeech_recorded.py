import requests,http.client, urllib.request, urllib.parse, urllib.error, base64, json,time,xml.etree.ElementTree as ET,wave

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

speech_headers = {
    # Request headers.
    #'Content-Type': 'application/json',
    'Content-Type': 'audio/wav; codec=audio/pcm; samplerate=16000',
    'Ocp-Apim-Subscription-Key': '1a9c61810190481b9baba5c0f5e45a79',
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



def main(argv):
    # The URL of a JPEG image containing text.
    print ("file is:%s" %argv[1])
    #body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png'}"
    body = "{'url':'https://1.bp.blogspot.com/-U_3DWTsQiT4/WUo-5gpun-I/AAAAAAAA4qc/gCH286FcQOAZTM0nyDfBz-D2FJNQba3mgCLcBGAs/s1600/PicsArt_06-21-05.25.44%2B%25281%2529.jpg'}"

    try:
        # Replace the three dots below with the full file path to a JPEG image of a celebrity on your computer or network.
        print("Before opening the file")
        audiofile = open(argv[1],'rb').read() # Read image file in binary mode
        # Execute the REST API call and get the response.

        #response = requests.post(url = uri_base,headers = headers,params = params,data = image)
        print("After opening the file")

        speech_URI='https://speech.platform.bing.com/speech/recognition/dictation/cognitiveservices/v1?language=en-US&format=simple'

        speechresponse = requests.request('POST', speech_URI, json=None, data=audiofile, headers=speech_headers, params=None)
        print("After getting the response %s" %speechresponse)
        parsed = json.loads(speechresponse.text)
        print (json.dumps(parsed, sort_keys=True, indent=2))
        lines=parsed["NBest"][0]
        itnText=lines["ITN"]
        print("Max text %s" %itnText)
        translatedtText=translatetext(itnText)
        print('-----------English translation is %s' %translatedtText)


    except Exception as e:
        print('Error:')
        print(e)

def translatetext (textVal):

    headers = {'Ocp-Apim-Subscription-Key': translation_subscription_key}
    conn = http.client.HTTPSConnection(translation_host)
    params = '?to=FR&category=generalnn&text=' + urllib.parse.quote (textVal)

    conn.request ("GET", translation_path + params, None, headers)
    response = conn.getresponse ()
    responseVal = ET.fromstring(response.read ().decode("UTF-8"))
    return responseVal.text

if __name__ == "__main__":
    from sys import argv
    main(argv)
####################################
