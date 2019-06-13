from io import BytesIO

import paho.mqtt.client as mqtt
import json
import time
class QueueSubscriber:

    def __init__(self):
        broker="iot.eclipse.org"
        self.client= mqtt.Client() 
        print("connecting to broker ",broker)
        self.client.connect(broker)#connect
        self.client.loop_start()
        self.client.on_message=on_message
        print("subscribing ")
        self.client.subscribe("masterResults")#subscribe
        

  
    def stop(self):
        self.client.disconnect() #disconnect
        self.client.loop_stop() #stop loop


def on_message(client, userdata, message):
    m_in=json.loads(str(message.payload.decode("utf-8")))
    print(m_in["encoding"],m_in["isUnwanted"], m_in["chat_id"], m_in["time"])

queue = QueueSubscriber()