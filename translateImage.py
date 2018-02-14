from  MultiFileTranslator import MultiFileTranslator
from SingleFileTranslator import SingleFileTranslator
import os

def main(argv):
    #translator = MultiFileTranslator()
    fileName = argv[1]

    if(fileName. endswith ('.tiff') or fileName. endswith ('.tif' ) or fileName.endswith ('.pdf' ) or fileName.endswith ('.PDF' ) ):
        translator = MultiFileTranslator()
        translator.translateFile(fileName)
    #PDF, DOCX,JPEG/PNG
    elif (fileName. endswith ('.docx')):
        command ='C:\Techolution\IOTPractise\CustomerProjects\Axa\DocumentTranslator\executeDocumentTranslator.bat '+fileName
        output = os.system(command)
        if (output == 0):
            outputfilename=fileName.replace(".docx",".en.docx")
            print ('output file of document translator %s'%outputfilename)
    else:
        translator = SingleFileTranslator()
        translator.translateFile(fileName)



if __name__ == "__main__":
    from sys import argv
    main(argv)
