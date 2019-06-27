#!/usr/bin/env python3

import face_recognition as fr
import numpy as np
import pickle
import os

TRESHOLD = 0.6

class FaceNotFound(RuntimeError):
    pass

data = {
  "encodings": [],
  "timestamps": [],
}

def get_encoding(filename):
    img = fr.load_image_file(filename)
    print(" locating face...")
    boxes = fr.face_locations(img, model="hog")
    print(" done.")
    if len(boxes) < 1:
        raise FaceNotFound()
    print(" computing encodings...")
    enc = fr.face_encodings(img, boxes)
    print(" done.")
    if len(enc) < 1:
        raise FaceNotFound()
    return enc[0]

def query_if_exists_byfile(filename):
    global data
    enc = get_encoding(filename)
    print("searching in %d encodings..." % len(data["encodings"]))
    matches = fr.compare_faces(data["encodings"], 
                                             enc, tolerance=TRESHOLD)
    try:
        return enc, matches.index(True)
    except ValueError:
        return enc, None

def query_and_add_byfile(filename, timestamp):
    global data
    enc = get_encoding(filename)
    print("searching in %d encodings..." % len(data["encodings"]))
    matches = fr.compare_faces(data["encodings"], 
                                             enc, tolerance=TRESHOLD)
    try:
        return enc, matches.index(True)
    except ValueError:
        print("adding with id ", len(data["encodings"]))
        data["encodings"].append(enc)
        data["timestamps"].append(timestamp)
        with open("encodings.pickle", "wb") as f:
            pickle.dump(data, f)
        return enc, len(data["encodings"])-1

def query_if_exists(enc):
    global data
    print("searching in %d encodings..." % len(data["encodings"]))
    matches = fr.compare_faces(data["encodings"], 
                                             enc, tolerance=TRESHOLD)
    try:
        return matches.index(True)
    except ValueError:
        return None

def query_and_add(enc, timestamp):
    global data
    print("searching in %d encodings..." % len(data["encodings"]))
    matches = fr.compare_faces(data["encodings"], 
                                             enc, tolerance=TRESHOLD)
    try:
        return matches.index(True)
    except ValueError:
        print("adding with id ", len(data["encodings"]))
        data["encodings"].append(enc)
        data["timestamps"].append(timestamp)
        with open("encodings.pickle", "wb") as f:
            pickle.dump(data, f)
        return len(data["encodings"])-1

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

def query_by_time_b64(timestamp):
    global data
    ts = data["timestamps"]
    en = data["encodings"]
    split_at = len(ts)
    for i in range(len(ts)-1, -1, -1):
        if timestamp >= ts[i]:
            split_at = i+1
            break
    return list(map(lambda x: str(base64.b64encode(x.tobytes()), "utf-8"), en[split_at:])), ts[split_at:]

def bulk_add(encodings, timestamps):
    global data
    assert len(encodings) == len(timestamps)
    ts = data["timestamps"]
    en = data["encodings"]
    for enc, timestamp in zip(encodings, encodings):
        en.append(enc)
        ts.append(timestamp)
    with open("encodings.pickle", "wb") as f:
        pickle.dump(data, f)

def restore():
    global data
    if os.path.exists("encodings.pickle"):
        with open("encodings.pickle", "rb") as f:
            data = pickle.load(f)

def destroy():
    global data
    data = {
      "encodings": [],
      "timestamps": [],
    }

if __name__ == "__main__":
    restore()
