from io import BytesIO

import paho.mqtt.client as mqtt
import feedback_db_helper
import numpy as np
import json
import faces
import time
import base64

class QueueSubscriber:

    def __init__(self, ip):
        self.client = mqtt.Client() 
        self.client.connect(ip, 1883)
        self.client.loop_start()
        self.client.on_message = on_message
        print("subscribing on ", ip)
        self.client.subscribe("masterResults") #subscribe
        
    def stop(self):
        self.client.disconnect() #disconnect
        self.client.loop_stop() #stop loop

def on_message(client, userdata, message):
    try:
        m_in = json.loads(str(message.payload.decode("utf-8")))
        print ("ON MESSAGE:", m_in["encoding"], m_in["isUnwanted"], m_in["chat_id"], m_in["time"])
        ndarr = np.ndarray(shape=(128,), dtype="float64", buffer=base64.b64decode(m_in["encoding"]))
        #print(ndarr)
        face_id = faces.query_and_add(ndarr, m_in["time"])
        print("FACE ID:", face_id)
        db = feedback_db_helper.FeedbackDBHelper()
        db.connect()
        t = db.get_time_by_target_and_chat_id(m_in["chat_id"], face_id)
        print("get_time_by_target_and_chat_id: ", t, " < ", m_in["time"], " ? ", m_in["time"] > t)
        if m_in["time"] > t:
            db.add_feedback(m_in["chat_id"], face_id,
            m_in["isUnwanted"], m_in["time"])
        db.close()
    except Exception as ee:
        import traceback
        traceback.print_exc()
    
