from translateImage import translateImage

def main(argv):
    translateImageObj = translateImage()
    outputfile = translateImageObj.gettranslateImage(argv[1])
    print('Translation output is in file %s' %outputfile)

if __name__ == "__main__":
    from sys import argv
    main(argv)
            #translateImage(argv)