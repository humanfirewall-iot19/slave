import os
import requests
import faces
import queue_subscriber
import feedback_db_helper

SRV_PORT = 41278

if os.uname()[4][:3] == "arm":
    import raspberry as dev
else:
    import laptop as dev

if os.path.exists(os.path.expanduser("~/master_ip")):
    MASTER_IP = open(os.path.expanduser("~/master_ip")).read().strip()
else:
    MASTER_IP = "0.0.0.0" # debug

def image_handler(image_path):
    r = None
    req = {}
    try:
        print ("face query")
        r = faces.query_if_exists_byfile(image_path)
    except faces.FaceNotFound:
        req["has_face"] = False
    else:
        req["has_face"] = True
    if r is not None:
        enc, face_id = r
        db = feedback_db_helper.FeedbackDBHelper()
        db.connect()
        req["feedback"] = db.get_feedback_by_target(face_id)
        db.close()
        req["encoding"] = enc
    req["board_id"] = dev.get_id()
    with open(image_path, 'rb') as f:
        print ("sending to master")
        files = {"file": f}
        r = requests.post("http://%s:%d/ring" % (MASTER_IP, SRV_PORT),
                          files=files, data=req)

qs = queue_subscriber.QueueSubscriber()

dev.register_handler(image_handler)
dev.device_setup_and_idle()

