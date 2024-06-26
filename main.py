import os
import shutil
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
        classId = request.form["classId"]
        file.save(app.config['TMP_IMG_PATH'])
        logger.info("Get data successfully")
        output = deepface_reg.recognize(app.config['TMP_IMG_PATH'],classId)
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
        classId = request.form.get('classId')
        if file and username:
            filename = username + '.jpg'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'] + "/" + classId, filename)
            file.save(file_path)
            return jsonify({'message': 'File uploaded successfully', 'file_path': file_path})

    except Exception as e:
        logger.info(e)
        return jsonify({'error': e})

@app.route("/addClass", methods=["POST"])
def registerClass():
    try:
        classId = request.form.get('classId')
        class_folder = os.path.join(app.config['UPLOAD_FOLDER'], classId)
        if not os.path.exists(class_folder):
            os.makedirs(class_folder)
            return jsonify({'message': f'Class {classId} registered successfully', 'class_folder': class_folder})
        else:
            return jsonify({'message': f'Class {classId} already exists', 'class_folder': class_folder})

    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)})

@app.route("/deleteClass", methods=["POST"])
def deleteClass():
    try:
        classId = request.form.get('classId')
        class_folder = os.path.join(UPLOAD_FOLDER, classId)

        if os.path.exists(class_folder):
            shutil.rmtree(class_folder)
            message = f"Class {classId} and its associated folder have been deleted successfully"
        else:
            message = f"Class {classId} does not exist"

        return jsonify({'message': message})

    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route("/updateStudentClass", methods=["POST"])
def update_student_class():
    try:
        old_class_id = request.form.get('old_class_id')
        username = request.form.get('username')  
        new_class_id = request.form.get('new_class_id')
        
        # Get paths for old and new class folders
        old_class_folder = os.path.join(UPLOAD_FOLDER, old_class_id)
        new_class_folder = os.path.join(UPLOAD_FOLDER, new_class_id)
        # Check if the old class folder exists
        if os.path.exists(old_class_folder):
            # Move student's image folder to the new class folder
            if not os.path.exists(new_class_folder):
                os.makedirs(new_class_folder)  # Create new class folder if it doesn't exist
            # Move images from old class folder to new class folder
            for filename in os.listdir(old_class_folder):
                if filename == f"{username}.jpg":  # Assuming image files are named username.jpg
                    old_image_path = os.path.join(old_class_folder, filename)
                    new_image_path = os.path.join(new_class_folder, filename)
                    shutil.move(old_image_path, new_image_path)

            message = f"Student {username}'s class has been updated to {new_class_id}"
        else:
            message = f"Student {username}'s folder does not exist"

        return jsonify({'message': message})

    except Exception as e:
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)


