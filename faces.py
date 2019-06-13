#!/usr/bin/env python3

import face_recognition as fr
import numpy as np
import pickle
import os

TRESHOLD = 0.4

class FaceNotFound(RuntimeError):
    pass

data = {
  "encodings": [],
  "timestamps": [],
}

def get_econding(filename):
    img = fr.load_image_file(filename)
    boxes = face_recognition.face_locations(img, model="hog")
    if len(boxes) < 1:
        raise FaceNotFound()
    enc = fr.face_encodings(img, boxes)
    if len(enc) < 1:
        raise FaceNotFound()
    return enc[0]

def query_if_exists_byfile(filename):
    global data
    enc = get_encoding(filename)
    matches = face_recognition.compare_faces(data["encodings"], 
                                             enc, tolerance=TRESHOLD)
    try:
        return matches.index(True)
    except ValueError:
        return None

def query_and_add_byfile(filename, timestamp):
    global data
    enc = get_encoding(filename)
    matches = face_recognition.compare_faces(data["encodings"], 
                                             enc, tolerance=TRESHOLD)
    try:
        return matches.index(True)
    except ValueError:
        data["encodings"].append(enc)
        data["timestamps"].append(timestamp)
        with open("encodings.pickle", "wb") as f:
            pickle.dump(data, f)

def query_if_exists(enc):
    global data
    matches = face_recognition.compare_faces(data["encodings"], 
                                             enc, tolerance=TRESHOLD)
    try:
        return matches.index(True)
    except ValueError:
        return None

def query_and_add(enc, timestamp):
    global data
    matches = face_recognition.compare_faces(data["encodings"], 
                                             enc, tolerance=TRESHOLD)
    try:
        return matches.index(True)
    except ValueError:
        data["encodings"].append(enc)
        data["timestamps"].append(timestamp)
        with open("encodings.pickle", "wb") as f:
            pickle.dump(data, f)

def query_by_time(timestamp):
    global data
    ts = data["timestamps"]
    en = data["encodings"]
    split_at = len(ts)
    for i in range(len(ts)-1, -1, -1):
        if timestamp >= ts[i]:
            split_at = i+1
            break
    return en[split_at:], ts[split_at:]

def bulk_add(encodings, timestamps):
    assert len(encodings) == len(timestamps)
    ts = data["timestamps"]
    en = data["encodings"]
    for enc, timestamp in zip(encodings, encodings):
        en.append(enc)
        ts.append(timestamp)
    with open("encodings.pickle", "wb") as f:
        pickle.dump(data, f)


def restore():
    if os.path.exists("encodings.pickle"):
        with open("encodings.pickle", "wb") as f:
            data = pickle.load(f)


if __name__ == "__main__":
    restore()
