import face_recognition
import cv2
from multiprocessing import Process, Manager, cpu_count, set_start_method
import time
import numpy
import threading
import platform

# Face_Recognition multiprocessing rewritten from
# facerec_from_webcam_multiprocessing.py
# in the Face_Recognition library

v_capture = cv2.VideoCapture(0)

def next_id(c_id, w_num):
    return 1 if c_id == w_num else c_id + 1


def prev_id(c_id, w_num):
    return w_num if c_id == 1 else c_id - 1


def capture(read_frame_list, Global, w_num):
    #print the dimensions
    #print("w: %d, h %d, FPS: %d" % (v_capture.get(3), v_capture.get(4), v_capture.get(5)))

    while not Global.exited:
        if Global.buff_num != next_id(Global.read_num, w_num):
            ret, frame = v_capture.read()
            read_frame_list[Global.buff_num] = frame
            Global.buff_num = next_id(Global.buff_num, w_num)
        else:
            time.sleep(0.01)


def process(w_id, read_frame_list, write_frame_list, Global, w_num):
    known_face_enc = Global.known_face_encodings
    known_face_names = Global.known_face_names

    while not Global.exited:
        while Global.read_num != w_id or Global.read_num != prev_id(Global.buff_num, w_num):
            if Global.exited:
                break
            #wait
            time.sleep(0.01)
        #delay to avoid lag
        time.sleep(Global.frame_delay)

        #get frame from webcame
        frame_proc = read_frame_list[w_id]

        #get next processor to read frame
        Global.read_num = next_id(Global.read_num, w_num)

        rgb_frame = frame_proc[:, :, ::-1]

        #find faces and encodings in each frame
        #these two itty-bitty lines are why I must suffer
        #through making it multi processor
        face_loc = face_recognition.face_locations(rgb_frame)
        face_enc = face_recognition.face_encodings(rgb_frame, face_loc)

        #colors = detect_body.detect_body(frame_proc)

        #iterate through the faces
        for(top, right, bot, left), face_enc in zip(face_loc, face_enc):
            matches = face_recognition.compare_faces(known_face_enc, face_enc)
            name = "Failed to Recognize"

            #if we find a match, we use the first one
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            #minecraft
            cv2.rectangle(frame_proc, (left, top - 10), (right, top-30), (0,0,0), -1)
            cv2.putText(frame_proc, name, (left, top - 15), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 1)
            #cv2.putText(frame_proc, colors[1], (left + 6, top - 25), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 1)
            #cv2.putText(frame_proc, colors[2], (left + 6, top - 35), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 1)

        #wait before writing
        while Global.write_num != w_id:
            time.sleep(0.01)
        write_frame_list[w_id] = frame_proc
        Global.write_num = next_id(Global.write_num, w_num)


def realtime_facial_recognize():
    #Apparently this fixes something on macOS? I'm not sure why
    #but the Face Recognition source code knows more than I do.
    if platform.system() == 'Darwin':
        set_start_method('forkserver')

    #print("Declaring Globals")
    #Globals
    Global = Manager().Namespace()
    Global.buff_num = 1
    Global.read_num = 1
    Global.write_num = 1
    Global.frame_delay = 0
    Global.exited = False
    read_frame_list = Manager().dict()
    write_frame_list = Manager().dict()

    #if more than 2, use one to cap frames
    if cpu_count() > 2:
        w_num = cpu_count()-1
    else:
        w_num = 2

    #list of subprocesses
    p = []

    #print("Appending Thread Capture")
    p.append(threading.Thread(target=capture, args = (read_frame_list, Global, w_num)))
    p[0].start()
    #print("Appended")

    tdogg_image = face_recognition.load_image_file("tdogg.jpg")
    tdogg_enc = face_recognition.face_encodings(tdogg_image)[0]
    aryan_image = face_recognition.load_image_file("aryan.jpg")
    aryan_enc = face_recognition.face_encodings(aryan_image)[0]
    ryan_image = face_recognition.load_image_file("ryan.jpg")
    ryan_enc = face_recognition.face_encodings(ryan_image)[0]

    Global.known_face_encodings = [
        tdogg_enc,
        aryan_enc,
        ryan_enc
    ]

    Global.known_face_names = [
        "T-Dogg",
        "Aryan Chaudhary",
        "Ryan Meliti"
    ]

    print("Registering Worker Threads")
    #register worker threads
    for w_id in range(1, w_num + 1):
        p.append(Process(target=process, args =(w_id, read_frame_list, write_frame_list, Global, w_num)))
        p[w_id].start()
    print("Worker Threads Registered")

    #show video
    last_num = 1
    fps_list = []
    temp = time.time() #start time
    print("starting show")
    while not Global.exited:
        while Global.write_num != last_num:
            last_num = int(Global.write_num)
            print("Calc FPS")
            #calc fps
            delay = time.time() - temp
            temp = time.time()
            fps_list.append(delay)
            if len(fps_list) > 5 * w_num:
                fps_list.pop(0)
            fps = len(fps_list) / numpy.sum(fps_list)
            print("fps: %.2f" % fps)

            #Frame delay based on values in facerec_from_webcam_multiprocessing.py
            if fps < 6:
                Global.frame_delay = (1 / fps) * 0.75
            elif fps < 20:
                Global.frame_delay = (1 / fps) * 0.5
            elif fps < 30:
                Global.frame_delay = (1 / fps) * 0.25
            else:
                Global.frame_delay = 0

            #print("Loading Video")
            #finally, display the result
            cv2.imshow('Video', write_frame_list[prev_id(Global.write_num, w_num)])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            Global.exited = True
            break
    time.sleep(0.01)
    v_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    realtime_facial_recognize()