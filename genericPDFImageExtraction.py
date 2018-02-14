import PyPDF2
import struct
from PIL import Image
"""
Links:
PDF format: http://www.adobe.com/content/dam/Adobe/en/devnet/acrobat/pdfs/pdf_reference_1-7.pdf
CCITT Group 4: https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-T.6-198811-I!!PDF-E&type=items
Extract images from pdf: http://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
Extract images coded with CCITTFaxDecode in .net: http://stackoverflow.com/questions/2641770/extracting-image-from-pdf-with-ccittfaxdecode-filter
TIFF format and tags: http://www.awaresystems.be/imaging/tiff/faq.html
"""


def tiff_header_for_CCITT(width, height, img_size, CCITT_group=4):
    tiff_header_struct = '<' + '2s' + 'h' + 'l' + 'h' + 'hhll' * 8 + 'h'
    return struct.pack(tiff_header_struct,
                       b'II',  # Byte order indication: Little indian
                       42,  # Version number (always 42)
                       8,  # Offset to first IFD
                       8,  # Number of tags in IFD
                       256, 4, 1, width,  # ImageWidth, LONG, 1, width
                       257, 4, 1, height,  # ImageLength, LONG, 1, lenght
                       258, 3, 1, 1,  # BitsPerSample, SHORT, 1, 1
                       259, 3, 1, CCITT_group,  # Compression, SHORT, 1, 4 = CCITT Group 4 fax encoding
                       262, 3, 1, 0,  # Threshholding, SHORT, 1, 0 = WhiteIsZero
                       273, 4, 1, struct.calcsize(tiff_header_struct),  # StripOffsets, LONG, 1, len of header
                       278, 4, 1, height,  # RowsPerStrip, LONG, 1, lenght
                       279, 4, 1, img_size,  # StripByteCounts, LONG, 1, size of image
                       0  # last IFD
                       )
def main(filePath):
    print('FIle to extract %s'%filePath)
    pdf_filename = filePath
    pdf_file = open(pdf_filename, 'rb')
    cond_scan_reader = PyPDF2.PdfFileReader(pdf_file)
    print('After reading file. Num pages %s'%cond_scan_reader.getNumPages())
    for i in range(0, cond_scan_reader.getNumPages()):
        page = cond_scan_reader.getPage(i)
        xObject = page['/Resources']['/XObject'].getObject()
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                """
                The  CCITTFaxDecode filter decodes image data that has been encoded using
                either Group 3 or Group 4 CCITT facsimile (fax) encoding. CCITT encoding is
                designed to achieve efficient compression of monochrome (1 bit per pixel) image
                data at relatively low resolutions, and so is useful only for bitmap image data, not
                for color images, grayscale images, or general data.

                K < 0 --- Pure two-dimensional encoding (Group 4)
                K = 0 --- Pure one-dimensional encoding (Group 3, 1-D)
                K > 0 --- Mixed one- and two-dimensional encoding (Group 3, 2-D)
                """
                print('Filter value is %s'%xObject[obj]['/Filter'])
                width = xObject[obj]['/Width']
                height = xObject[obj]['/Height']
                print('width is %s '%width)
                print('height is %s '%height)
                size = (width, height)
                mode = "P"
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"

                if xObject[obj]['/Filter'] == '/CCITTFaxDecode':
                    if xObject[obj]['/DecodeParms']['/K'] == -1:
                        CCITT_group = 4
                    else:
                        CCITT_group = 3
                    data = xObject[obj]._data  # sorry, getData() does not work for CCITTFaxDecode
                    img_size = len(data)
                    tiff_header = tiff_header_for_CCITT(width, height, img_size, CCITT_group)
                    img_name = obj[1:] + '.tiff'
                    with open(img_name, 'wb') as img_file:
                        img_file.write(tiff_header + data)

                if xObject[obj]['/Filter'] == '/DCTDecode':
                    data = xObject[obj]._data
                    img = open(obj[1:] + ".jpg", "wb")
                    img.write(data)
                    img.close()

                if xObject[obj]['/Filter'] == '/FlateDecode':
                    try:
                        data = xObject[obj]._data
                        #print('Data is %s'%data)
                        img = Image.frombytes(mode, size, data)
                        img.save(obj[1:] + ".png")
                    #
                    # import io
                    # from PIL import Image
                    # im = Image.open(io.BytesIO(tiff_header + data))
                    except Exception as e:
                        print('Error:')
                        print(e)
    pdf_file.close()

if __name__ == "__main__":
    from sys import argv
    main(argv[1])
#################
