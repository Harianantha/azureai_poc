
import os
from SingleFileTranslator import SingleFileTranslator
# from MultiFileTranslator import MultiFileTranslator

from translateImage import translateImage
from flask import Flask, request, render_template, send_from_directory, send_file

__author__ = 'kranthi'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():

    print("came here" )
    '''
    # this is to verify that folder to upload to exists.
    if os.path.isdir(os.path.join(APP_ROOT, 'files/{}'.format(folder_name))):
        print("folder exist")
    '''
    target = os.path.join(APP_ROOT, 'files/{}'.format(''))
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png") or (ext == ".tiff") or (ext == ".tif") or (ext == ".pdf") or (ext == ".docx")  :
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
       # print("Save it to:", destination)
        upload.save(destination)
     #   filename = upload.filename
        '''
        if (upload.filename.endswith('.tiff') or upload.filename.endswith('.png') or upload.filename.endswith('.pdf') or upload.filename.endswith(
                '.PDF')):

            translator = SingleFileTranslator()
            outputfile = translator.translateFile(destination)
        '''
        translateImageObj=translateImage()
        outputfile = translateImageObj.gettranslateImage(destination)
    #return outputfile
    return send_file(outputfile, as_attachment=True,mimetype='application/pdf')



@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./images')
    print(image_names)
    return render_template("gallery.html", image_names=image_names)


if __name__ == "__main__":
    app.run(port=80, debug=True ,host ='0.0.0.0')
