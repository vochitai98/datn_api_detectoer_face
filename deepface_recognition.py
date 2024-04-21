from deepface import DeepFace

class DeepFaceRecognition:
    def __init__(self, detector_backend, face_model, database, logger, distance_threshold=0.3):
        self.detector_backend = detector_backend
        self.face_model = face_model
        self.database = database
        self.logger = logger
        self.distance_threshold = distance_threshold

    
    def recognize(self, img_path): # attendance
        self.logger.info(f"image path: {img_path}")
        dfs = DeepFace.find(img_path = img_path,
            db_path = self.database, 
            model_name = self.face_model,
            detector_backend = self.detector_backend,
            enforce_detection = False
        )
        person_name_list = []
        self.logger.info(dfs)
        for df in dfs:
            if df.empty:
                print('DataFrame is empty!')
                continue
            username = df['identity'][0].split('.')[0].split('\\')[-1]
            distance = float(df['distance'][0])
            if distance < self.distance_threshold:
                self.logger.info(username)
                person_name_list.append(username)
        return person_name_list


if __name__ == "__main__":
    from logger import get_logger
    logger = get_logger()
    deepface_reg = DeepFaceRecognition(detector_backend="fastmtcnn", face_model="ArcFace", database="database", logger=logger)