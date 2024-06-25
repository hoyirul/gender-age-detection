import cv2
import sqlite3

# Inisialisasi koneksi SQLite
conn = sqlite3.connect('visitors.db')
cursor = conn.cursor()

# Buat tabel jika belum ada
cursor.execute('''
    CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gender TEXT,
        age_group TEXT
    )
''')
conn.commit()

# Muat model dan konfigurasi
faceProto = "./models/opencv_face_detector.pbtxt"
faceModel = "./models/opencv_face_detector_uint8.pb"
genderProto = "./models/gender/gender.prototxt"
genderModel = "./models/gender/gender_net.caffemodel"
ageProto = "./models/age/age.prototxt"
ageModel = "./models/age/age_net.caffemodel"

# Muat model OpenCV
faceNet = cv2.dnn.readNet(faceModel, faceProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)
ageNet = cv2.dnn.readNet(ageModel, ageProto)

# Parameter
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
genderList = ['Male', 'Female']
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']

# Fungsi untuk mendeteksi wajah
def getFaceBox(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, bboxes

# Buka koneksi ke kamera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Tidak dapat membuka kamera.")
    exit()

while True:
    # Baca frame dari kamera
    ret, frame = cap.read()
    if not ret:
        break

    # Dapatkan deteksi wajah
    frameFace, bboxes = getFaceBox(faceNet, frame)

    if not bboxes:
        print("Tidak ada wajah yang terdeteksi")
        continue

    for bbox in bboxes:
        # Ekstrak wajah dari frame
        face = frame[max(0, bbox[1]):min(bbox[3], frame.shape[0]-1), max(0, bbox[0]):min(bbox[2], frame.shape[1]-1)]

        # Dapatkan prediksi gender
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]

        # Dapatkan prediksi usia
        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]

        label = "{}, {}".format(gender, age)
        cv2.putText(frameFace, label, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)

        # Simpan ke database SQLite
        # cursor.execute('INSERT INTO visitors (gender, age_group) VALUES (?, ?)', (gender, age))
        # conn.commit()
    # Tampilkan hasil
    cv2.imshow("Gender and Age Detection", frameFace)

    # Tunggu selama 1ms dan periksa apakah tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup jendela dan lepaskan kamera
cap.release()
cv2.destroyAllWindows()
