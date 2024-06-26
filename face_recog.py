import cv2
import face_recognition
import glob

# Inisialisasi data wajah yang dikenal
known_face_encodings = []
known_face_names = []

# Mengambil path gambar dari direktori ./faceID/ ga harus jpg tapi semua extensi gambar
image_files = glob.glob('./faceID/*.jpg') + glob.glob('./faceID/*.jpeg') + glob.glob('./faceID/*.png') + glob.glob('./faceID/*.webp')

# Memuat encoding wajah dan nama
for image_path in image_files:
    # Dapatkan nama dari path file tanpa ekstensi
    name = image_path.split('/')[-1].split('.')[0]
    # Muat gambar dan ambil encoding
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)[0]  # Ambil encoding pertama (asumsi hanya satu wajah dalam gambar)
    known_face_encodings.append(encoding)
    known_face_names.append(name)

# Inisialisasi webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Temukan lokasi dan encoding wajah dalam frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Cocokkan encoding wajah dengan data yang dikenal
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Gambar kotak di sekitar wajah
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        # Tampilkan hanya nama tanpa path lengkap dari file gambar
        name = name.replace('faceID\\', '')
        print(name)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
