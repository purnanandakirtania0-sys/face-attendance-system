import cv2
import os
import csv
from datetime import datetime
import pytz

# ---------------- PATHS ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cascade_path = os.path.join(
    BASE_DIR,
    "haarcascade_frontalface_default.xml"
)

trainer_path = os.path.join(
    BASE_DIR,
    "trainer",
    "trainer.yml"
)

dataset_path = os.path.join(
    BASE_DIR,
    "dataset"
)

attendance_file = os.path.join(
    BASE_DIR,
    "attendance.csv"
)

# ---------------- CHECK TRAINER FILE ----------------

if not os.path.exists(trainer_path):

    print("trainer.yml file not found")
    exit()

# ---------------- FACE DETECTOR ----------------

face_detector = cv2.CascadeClassifier(
    cascade_path
)

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read(trainer_path)

# ---------------- LOAD NAMES ----------------

names = {}

for file in os.listdir(dataset_path):

    if file.endswith(".jpg"):

        parts = file.split(".")

        if len(parts) >= 4:

            face_id = int(parts[1])

            name = parts[2]

            names[face_id] = name

print("Loaded Names:", names)

# ---------------- CREATE CSV FILE ----------------

if not os.path.exists(attendance_file):

    with open(
        attendance_file,
        "w",
        newline=""
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "Name",
            "Date",
            "Time"
        ])

# ---------------- CAMERA ----------------

cam = cv2.VideoCapture(0)

cam.set(3, 640)
cam.set(4, 480)

print("Camera Started...")

# ---------------- LOOP ----------------

while True:

    ret, img = cam.read()

    if not ret:
        break

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(100,100)
    )

    for (x,y,w,h) in faces:

        # ---------------- RECTANGLE ----------------

        cv2.rectangle(
            img,
            (x,y),
            (x+w,y+h),
            (0,255,0),
            3
        )

        # ---------------- FACE PREDICTION ----------------

        id, confidence = recognizer.predict(
            gray[y:y+h, x:x+w]
        )

        # ---------------- REAL FACE DETECTED ----------------

        if confidence < 70:

            name = names.get(id, "Unknown")
            
            india = pytz.timezone('Asia/kolkata')

            now = datetime.now(india)

            date = now.strftime("%Y-%m-%d")

            time = now.strftime("%H:%M:%S")

            # ---------------- SHOW NAME ----------------

            cv2.putText(
                img,
                f"{name}",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,255,255),
                2
            )

            # ---------------- CHECK DUPLICATE ----------------

            already_marked = False

            with open(
                attendance_file,
                "r"
            ) as f:

                reader = csv.reader(f)

                for row in reader:

                    if len(row) >= 2:

                        old_name = row[0].strip().lower()
                        old_date = row[1].strip()

                        if (
                            old_name == name.strip().lower()
                            and old_date == date
                        ):

                            already_marked = True
                            break

            # ---------------- IF ALREADY MARKED ----------------

            if already_marked:

                cv2.putText(
                    img,
                    "Attendance Already Marked",
                    (x, y+h+40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,0,255),
                    2
                )

                cv2.imshow(
                    "Face Attendance System",
                    img
                )

                cv2.waitKey(3000)

                cam.release()

                cv2.destroyAllWindows()

                print("Already Marked")

                exit()

            # ---------------- SAVE ATTENDANCE ----------------

            else:

                with open(
                    attendance_file,
                    "a",
                    newline=""
                ) as f:

                    writer = csv.writer(f)

                    writer.writerow([
                        name,
                        date,
                        time
                    ])

                # ---------------- SHOW SUCCESS ----------------

                cv2.putText(
                    img,
                    "Attendance Marked",
                    (x, y+h+40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,0),
                    2
                )

                cv2.imshow(
                    "Face Attendance System",
                    img
                )

                print("Attendance Saved Successfully")

                #  AUTO CLOSE CAMERA
                cv2.waitKey(3000)

                cam.release()

                cv2.destroyAllWindows()

                print("Camera Closed")

                exit()

        # ---------------- UNKNOWN FACE ----------------

        else:

            cv2.putText(
                img,
                "Unknown Face",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0,0,255),
                2
            )

    # ---------------- SHOW CAMERA ----------------

    cv2.imshow(
        "Face Attendance System",
        img
    )

    # PRESS Q TO EXIT
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---------------- CLEANUP ----------------

cam.release()

cv2.destroyAllWindows()

print("System Closed")