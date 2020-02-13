import face_recognition
import cv2

#load the default hot men
#tdogg_image = face_recognition.load_image_file("tdogg.jpg")
#tdogg_enc = face_recognition.face_encodings(tdogg_image)[0]
aryan_image = face_recognition.load_image_file("aryan.jpg")
aryan_enc = face_recognition.face_encodings(aryan_image)[0]
ryan_image = face_recognition.load_image_file("ryan.jpg")
ryan_enc = face_recognition.face_encodings(ryan_image)[0]

known_face_enc = [
    #tdogg_enc,
    aryan_enc,
    ryan_enc
]
known_face = [
    #"T-Dogg",
    "Aryan Chaudhary",
    "Ryan Meliti"
]

def get_name(cap):
    if not cap.isOpened():
        cap.open()

    #get frame, close it
    ret, frame = cap.read()

    #register faces
    rgb_frame = frame[:, :, ::-1]
    face_loc = face_recognition.face_locations(rgb_frame)
    face_enc = face_recognition.face_encodings(rgb_frame, face_loc)

    #find matches
    matches = None
    for (top, right, bottom, left), enc in zip(face_loc, face_enc):
        matches = face_recognition.compare_faces(known_face_enc, enc)

    #load matches
    name = "Unknown"
    if matches != None and True in matches:
        name = known_face[matches.index(True)]

    #first match
    print(name)
    return name

def add_name(cap, name):
    ret, frame = cap.read()
    rgb_frame = frame[:, :, ::-1]
    face_loc = face_recognition.face_locations(rgb_frame)
    face_enc = face_recognition.face_encodings(rgb_frame, face_loc)[0]
    known_face_enc.append(face_enc)
    known_face.append(name)