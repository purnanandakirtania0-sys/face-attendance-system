import cv2
import os
import sys

# ---------------- GET NAME ----------------

if len(sys.argv) < 2:

    print("Name not provided")
    exit()

name = sys.argv[1]

# ---------------- PATHS ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dataset_path = os.path.join(
    BASE_DIR,
    "dataset"
)

cascade_path = os.path.join(
    BASE_DIR,
    "haarcascade_frontalface_default.xml"
)

# ---------------- CREATE DATASET FOLDER ----------------

if not os.path.exists(dataset_path):

    os.makedirs(dataset_path)

# ---------------- AUTO GENERATE ID ----------------

existing_ids = []

for file in os.listdir(dataset_path):

    if file.endswith(".jpg"):

        parts = file.split(".")

        if len(parts) >= 4:

            try:

                existing_ids.append(
                    int(parts[1])
                )

            except:
                pass

# ✅ NEW UNIQUE ID

if len(existing_ids) == 0:

    face_id = 1

else:

    face_id = max(existing_ids) + 1

print("Student ID:", face_id)

# ---------------- FACE DETECTOR ----------------

face_detector = cv2.CascadeClassifier(
    cascade_path
)

# ---------------- CAMERA ----------------

cam = cv2.VideoCapture(0)

cam.set(3, 640)
cam.set(4, 480)

print("Capturing Face...")

count = 0

# ---------------- LOOP ----------------

while True:

    ret, img = cam.read()

    if not ret:
        break

    # ✅ GRAYSCALE FOR DETECTION ONLY
    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x,y,w,h) in faces:

        # ✅ DRAW RECTANGLE
        cv2.rectangle(
            img,
            (x,y),
            (x+w,y+h),
            (0,255,0),
            2
        )

        count += 1

        # ✅ SAVE COLOR FACE IMAGE
        face = img[y:y+h, x:x+w]

        file_name = (
            f"User.{face_id}.{name}.{count}.jpg"
        )

        file_path = os.path.join(
            dataset_path,
            file_name
        )

        cv2.imwrite(
            file_path,
            face
        )

        # ✅ SHOW COUNT
        cv2.putText(
            img,
            f"Image {count}/20",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

    # ✅ SHOW CAMERA
    cv2.imshow(
        "Register Face",
        img
    )

    k = cv2.waitKey(100) & 0xff

    # ESC PRESS
    if k == 27:
        break

    # AUTO STOP AFTER 20 IMAGES
    elif count >= 20:
        break

# ---------------- CLEANUP ----------------

cam.release()

cv2.destroyAllWindows()

print("Dataset Collection Complete")