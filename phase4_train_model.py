import cv2
import os
import numpy as np
from PIL import Image

# ---------------- PATHS ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dataset_path = os.path.join(
    BASE_DIR,
    "dataset"
)

trainer_dir = os.path.join(
    BASE_DIR,
    "trainer"
)

trainer_path = os.path.join(
    trainer_dir,
    "trainer.yml"
)

# ---------------- CREATE TRAINER FOLDER ----------------

if not os.path.exists(trainer_dir):

    os.makedirs(trainer_dir)

# ---------------- FACE RECOGNIZER ----------------

recognizer = cv2.face.LBPHFaceRecognizer_create()

detector = cv2.CascadeClassifier(
    os.path.join(
        BASE_DIR,
        "haarcascade_frontalface_default.xml"
    )
)

print("Training Faces...")

# ---------------- GET IMAGES ----------------

def getImagesAndLabels(path):

    imagePaths = []

    #  GET ALL JPG FILES
    for root, dirs, files in os.walk(path):

        for file in files:

            if file.endswith(".jpg"):

                imagePaths.append(
                    os.path.join(root, file)
                )

    faceSamples = []

    ids = []

    for imagePath in imagePaths:

        try:

            #  CONVERT IMAGE TO GRAY
            PIL_img = Image.open(
                imagePath
            ).convert('L')

            img_numpy = np.array(
                PIL_img,
                'uint8'
            )

            # ---------------- FILE NAME FORMAT ----------------
            # User.<id>.<name>.<count>.jpg

            file_name = os.path.split(
                imagePath
            )[-1]

            parts = file_name.split(".")

            if len(parts) < 4:
                continue

            face_id = int(parts[1])

            faces = detector.detectMultiScale(
                img_numpy
            )

            for (x,y,w,h) in faces:

                faceSamples.append(
                    img_numpy[y:y+h, x:x+w]
                )

                ids.append(face_id)

        except Exception as e:

            print("Error:", imagePath)

            print(e)

    return faceSamples, ids

# ---------------- TRAIN MODEL ----------------

faces, ids = getImagesAndLabels(
    dataset_path
)

if len(faces) == 0:

    print("No face data found")

    exit()

recognizer.train(
    faces,
    np.array(ids)
)

# ---------------- SAVE TRAINER ----------------

recognizer.write(
    trainer_path
)

print("Model Trained Successfully")

print(f"Total Faces Trained: {len(set(ids))}")