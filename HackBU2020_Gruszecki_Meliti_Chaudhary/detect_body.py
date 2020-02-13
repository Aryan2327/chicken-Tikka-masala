import cv2
from PIL import Image
import numpy
import webcolors

def detect_body(img):
    #i don't even want to comment this but it basically
    #uses someone elses cooler code to find bod sections
    body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
    upper_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
    lower_cascade = cv2.CascadeClassifier('haarcascade_lowerbody.xml')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bodies = body_cascade.detectMultiScale(gray, 1.05, 4)
    upper = upper_cascade.detectMultiScale(gray, 1.05, 4)
    lower = lower_cascade.detectMultiScale(gray, 1.05, 4)
    dcolors = [None,None,None]


    for (x, y, w, h) in bodies:
        #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        dcolors[0] = color_find(img[y:y + h, x:x + w])

    for (x,y,w,h) in upper:
        #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        dcolors[1] = color_find(img[y:y + h, x:x + w])

    for (x,y,w,h) in lower:
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        dcolors[2] = color_find(img[y:y + h, x:x + w])

    return dcolors

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def color_find(img):
    pixels = numpy.float32(img.reshape(-1, 3))
    num_colors = 5
    thresh = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, num_colors, None, thresh, 10, cv2.KMEANS_RANDOM_CENTERS)
    _, counts = numpy.unique(labels, return_counts=True)

    color = closest_colour(palette[numpy.argmax(counts)])
    return color