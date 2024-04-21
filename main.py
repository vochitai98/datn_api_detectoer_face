import os

from flask import Flask, jsonify, request

from logger import get_logger
from deepface_recognition import DeepFaceRecognition

app = Flask("Face Recognition with DeepFace")
logger = get_logger()


UPLOAD_FOLDER = 'data/database'
TMP_IMG_PATH = "tmp.jpg"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TMP_IMG_PATH'] = TMP_IMG_PATH
deepface_reg = DeepFaceRecognition(detector_backend="retinaface", face_model="ArcFace", database=UPLOAD_FOLDER, logger=logger)

@app.route("/recognize", methods=["POST"])
def recognize():
    try:
        file = request.files["file"]
        file.save(app.config['TMP_IMG_PATH'])
        logger.info("Get data successfully")
        output = deepface_reg.recognize(app.config['TMP_IMG_PATH'])
        logger.info(output)

    except Exception as e:
        logger.info(e)
        output = "error"

    return jsonify(text=output)

@app.route("/register", methods=["POST"])
def register():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        username = request.form.get('username')
        if file and username:
            filename = username + '.jpg'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return jsonify({'message': 'File uploaded successfully', 'file_path': file_path})

    except Exception as e:
        logger.info(e)
        return jsonify({'error': e})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)


