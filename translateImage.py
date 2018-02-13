from  MultiFileTranslator import MultiFileTranslator
from SingleFileTranslator import SingleFileTranslator

def main(argv):
    #translator = MultiFileTranslator()
    fileName = argv[1]

    if(fileName. endswith ('.tiff') or fileName. endswith ('.tif' ) or fileName.endswith ('.pdf' ) or fileName.endswith ('.PDF' ) ):
        translator = MultiFileTranslator()
        translator.translateFile(fileName)
    #PDF, DOCX,JPEG/PNG
    else:
        translator = SingleFileTranslator()
        translator.translateFile(fileName)



if __name__ == "__main__":
    from sys import argv
    main(argv)
