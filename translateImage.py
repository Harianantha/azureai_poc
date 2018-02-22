from  MultiFileTranslator import MultiFileTranslator
from SingleFileTranslator import SingleFileTranslator
import os

class translateImage:
    def gettranslateImage(self,argv):
        #translator = MultiFileTranslator()
        fileName = argv

        if(fileName. endswith ('.tiff') or fileName. endswith ('.tif' ) or fileName.endswith ('.pdf' ) or fileName.endswith ('.PDF' ) ):
            translator = MultiFileTranslator()
            outputfile=translator.translateFile(fileName)
            print('Access translated file at %s'%outputfile)
            return outputfile
        #PDF, DOCX,JPEG/PNG
        elif (fileName. endswith ('.docx')):
            command ='C:\Axa\executeDocumentTranslator.bat '+fileName
            output = os.system(command)
            if (output == 0):
                outputfilename=fileName.replace(".docx",".en.docx")
                print ('output file of document translator %s'%outputfilename)
                return outputfilename
        else:
            translator = SingleFileTranslator()
            outputfile=translator.translateFile(fileName)
            print('Access translated file at %s'%outputfile)
            return outputfile



    '''
    if __name__ == "__main__":
        from sys import argv
            gettranslateImage(argv)
            #translateImage(argv)
    '''