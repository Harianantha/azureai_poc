from  MultiFileTranslator import MultiFileTranslator
from SingleFileTranslator import SingleFileTranslator

def main(argv):
    #translator = MultiFileTranslator()
    fileName = argv[1]

    if(fileName. endswith ('.tiff') or fileName. endswith ('.tif' ) ):
        translator = MultiFileTranslator()
        translator.translateFile(fileName)
    else:
        translator = SingleFileTranslator()
        translator.translateFile(fileName)



if __name__ == "__main__":
    from sys import argv
    main(argv)
