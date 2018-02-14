import fitz,time
def main(argv):
  doc = fitz.open(argv)
  millis = int(round(time.time() * 1000))

  ocrrecognizedfileName=argv.replace(".","_")+str(millis)+"extracted"
  for i in range(len(doc)):
      for img in doc.getPageImageList(i):
          xref = img[0]
          pix = fitz.Pixmap(doc, xref)
          if pix.n < 5:       # this is GRAY or RGB
              pix.writePNG(ocrrecognizedfileName+"p%s-%s.png" % (i, xref))
          else:               # CMYK: convert to RGB first
              pix1 = fitz.Pixmap(fitz.csRGB, pix)
              pix1.writePNG(ocrrecognizedfileName+"p%s-%s.png" % (i, xref))
              pix1 = None
          pix = None

if __name__ == "__main__":
    from sys import argv
    main(argv[1])
