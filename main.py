import os
import requests
import faces
import queue_subscriber
import feedback_db_helper
import json

SRV_PORT = 41278

if os.uname()[4][:3] == "arm":
    import raspberry as dev
else:
    import laptop as dev

faces.restore()

if os.path.exists(os.path.expanduser("~/master_ip")):
    MASTER_IP = open(os.path.expanduser("~/master_ip")).read().strip()
else:
    MASTER_IP = "0.0.0.0" # debug

def image_handler(image_path):
    r = None
    req = {
      "encoding": None,
      "feedback": None
    }
    try:
        print ("face query")
        r = faces.query_if_exists_byfile(image_path)
    except faces.FaceNotFound:
        req["has_face"] = False
    else:
        req["has_face"] = True
    if r is not None:
        enc, face_id = r
        req["encoding"] = enc.tolist()
        if face_id is not None:
            db = feedback_db_helper.FeedbackDBHelper()
            db.connect()
            req["feedback"] = db.get_feedback_by_target(face_id)
            db.close()
    req["board_id"] = dev.get_id()
    with open(image_path, 'rb') as f:
        req = json.dumps(req)
        print ("sending to master ", req)
        files = {"file": f}
        r = requests.post("http://%s:%d/ring" % (MASTER_IP, SRV_PORT),
                          files=files, data={"json": req})
        print(r)

qs = queue_subscriber.QueueSubscriber()

dev.register_handler(image_handler)
dev.device_setup_and_idle()

