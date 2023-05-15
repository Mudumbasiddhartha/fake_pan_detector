from flask import Flask, render_template,redirect, url_for, request, session, flash
import os

from skimage.metrics import structural_similarity
import imutils

import cv2

from PIL import Image

app = Flask(__name__)
path = os.getcwd()
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['INITIAL_FILE_UPLOADS'] = os.path.join(path, 'static\\uploads')
app.config['EXISTNG_FILE'] = os.path.join(path, 'static\\original')
app.config['GENERATED_FILE'] = os.path.join(path, 'static\\generated')


@app.route("/", methods=["GET", "POST"])
def hello_world():

    return render_template("index.html")


@app.route("/redirect", methods=["GET", "POST"])
def redirect_to_test():
    return redirect(url_for("test"))


@app.route("/test",methods=["GET", "POST"])
def test():

    if request.method == "GET":
        return render_template("test.html")

    if request.method == "POST":
                return redirect(url_for("redirect2"))





@app.route("/redirect2", methods=["GET", "POST"])
def redirect2():
    if request.method == "GET":
        return redirect(url_for("test"))

    if request.method == "POST":
                file_upload = request.files['file_upload']
                filename = file_upload.filename
                if filename == '':
                    # flash('No selected file')
                    return render_template('test.html',error="No file selected")
                
                # Resize and save the uploaded image
                uploaded_image = Image.open(file_upload).resize((250,160))
                uploaded_image=uploaded_image.convert('RGB')

                uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))

                # Resize and save the original image to ensure both uploaded and original matches in size
                original_image = Image.open(os.path.join(app.config['EXISTNG_FILE'], 'pan-card.png')).resize((250,160))
                original_image=original_image.convert('RGB')

                original_image.save(os.path.join(app.config['EXISTNG_FILE'], 'image.jpg'))

                # Read uploaded and original image as array
                original_image = cv2.imread(os.path.join(app.config['EXISTNG_FILE'], 'image.jpg'))
                uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))

                # convert image into grayscale
                original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
                uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)

                # Calculate structural similarity
                (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
                diff = (diff * 255).astype("uint8")

                # Calculate threshold and contours
                thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                
                # Draw contours on image
                for c in cnts:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(uploaded_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Save all output images (if required)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_thresh.jpg'), thresh)
                res = score*100
                if res>80:
                    # tbp = "The pan card uploaded is original (Score = "+str(round(res,2))+")"
                    # h2 with green color
                    tbp = "The pan card uploaded is original (Score = "+str(round(res,2))+")"
                    return render_template('results.html',pred="<h3 style='background-color:#5cf785;'>"+tbp+"</h3>")
                else:
                    # tbp="The pan card uploaded is fake (Score = "+str(round(res,2))+")"
                    # h2 with red color
                    tbp = "The pan card uploaded is fake (Score = "+str(round(res,2))+")"
                    return render_template('results.html',pred="<h3 style='background-color:red;'>"+tbp+"</h3>")

                return render_template('results.html',pred=tbp)

@app.route("/results",methods=["GET", "POST"])
def results():
    if request.method == "GET":

        return render_template("results.html")
    if request.method == "POST":
        return redirect(url_for("redirect2"))

if __name__ == "__main__":
    app.run(debug=False, host ='0.0.0.0')
