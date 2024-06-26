# Gender and Age Detetction and Face Recognition Python

## Installation
1. Download face detector https://github.com/spmallick/learnopencv/blob/master/AgeGender/opencv_face_detector.pbtxt
2. Download face detector pb https://github.com/spmallick/learnopencv/blob/master/AgeGender/opencv_face_detector_uint8.pb
3. Download caffemodel age https://github.com/eveningglow/age-and-gender-classification/blob/master/model/age_net.caffemodel
4. Download prototxt age https://github.com/eveningglow/age-and-gender-classification/blob/master/model/deploy_age2.prototxt
5. Download caffemodel gender https://github.com/eveningglow/age-and-gender-classification/blob/master/model/gender_net.caffemodel
6. Download prototxt gender https://github.com/eveningglow/age-and-gender-classification/blob/master/model/deploy_gender2.prototxt
7. Install venv ```sh python3 -m venv venv```
8. Windows ```sh venv\bin\activate```, Linux/MacOS ```sh source venv/bin/activate```
9. Install requirements ```sh pip3 install -r requirements.txt```
10. Run ```sh python main.py``` or ```sh python3 face_recog.py```

## Structure
```sh 
 .
 ├── faceID
 │   ├── person1.jpg
 │   ├── person2.jpg
 │   └── person3.jpg
 ├── models
 │   ├── age
 │   │   ├── age_net.caffemodel
 │   │   └── age.prototxt
 │   ├── gender
 │   │   ├── gender_net.caffemodel
 │   │   └── gender.prototxt
 │   ├── opencv_face_detector.pbtxt
 │   └── opencv_face_detector_uint8.pb
 ├── main.py
 └── face_recog.py
 └── rollcall.py
 └── visitors.db
 └── README.md
 └── requirements.txt
```