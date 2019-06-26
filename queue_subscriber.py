from io import BytesIO

import paho.mqtt.client as mqtt
import feedback_db_helper
import json
import faces
import time
import configparser

class QueueSubscriber:

    def __init__(self, ip):
        self.client = mqtt.Client() 
        self.client.connect(ip, 1883)
        self.client.loop_start()
        self.client.on_message = on_message
        print("subscribing ")
        self.client.subscribe("masterResults") #subscribe
        
    def stop(self):
        self.client.disconnect() #disconnect
        self.client.loop_stop() #stop loop

def on_message(client, userdata, message):
    m_in = json.loads(str(message.payload.decode("utf-8")))
    print (m_in["encoding"], m_in["isUnwanted"], m_in["chat_id"], m_in["time"])
    face_id = faces.query_and_add(m_in["encoding"])
    db = feedback_db_helper.FeedbackDBHelper()
    db.connect()
    t = db.get_time_by_target_and_chat_id(m_in["chat_id"], face_id)
    if m_in["time"] > t:
        db.add_feedback(m_in["chat_id"], face_id,
        m_in["isUnwanted"], m_in["time"])
    db.close()

    
