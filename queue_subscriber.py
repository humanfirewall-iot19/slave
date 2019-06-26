from io import BytesIO

import paho.mqtt.client as mqtt
import feedback_db_helper
import json
import faces
import time

class QueueSubscriber:

    def __init__(self, master_ip):
        parser = configparser.ConfigParser()
        parser.read('config.ini')
        self.client = mqtt.Client() 
        url = master_ip
        port = 1883
        self.client.username_pw_set(username, password)
        self.client.connect(url, port)
        self.client.loop_start()
        self.client.on_message = on_message
        print("subscribing ")
        self.client.subscribe("masterResults") #subscribe
        
    def stop(self):
        self.client.disconnect() #disconnect
        self.client.loop_stop() #stop loop

def on_message(client, userdata, message):
    m_in = json.loads(str(message.payload.decode("utf-8")))
    print ("ON MESSAGE:", m_in["encoding"], m_in["isUnwanted"], m_in["chat_id"], m_in["time"])
    face_id = faces.query_and_add(m_in["encoding"], m_in["time"])
    print("FACE ID:", face_id)
    db = feedback_db_helper.FeedbackDBHelper()
    db.connect()
    t = db.get_time_by_target_and_chat_id(m_in["chat_id"], face_id)
    print("get_time_by_target_and_chat_id: ", t, " < ", m_in["time"], "  ??? ", m_in["time"] > t)
    if m_in["time"] > t:
        db.add_feedback(m_in["chat_id"], face_id,
        m_in["isUnwanted"], m_in["time"])
    db.close()

    
