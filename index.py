from iofog.microservices.client import Client
from iofog.microservices.exception import IoFogException
from iofog.microservices.iomessage import IoMessage
from iofog.microservices.listener import *

from csv import reader
from datetime import datetime
import json

import logging
log = logging.getLogger(__name__)

IoClient = Client()


# def update_config():
#     attempt_limit = 5
#     while attempt_limit > 0:
#         try:
#             config = IoClient.get_config()
#             break
#         except IoFogException as e:
#             attempt_limit -= 1
#             log.error('Error updating config: ', e)
#     if attempt_limit == 0:
#         print("Config update failed")
#         return
#     current_config = config
#     return current_config



def send_sensor_data():
    log.info("Starting sending data")
    #TODO: Get data from csv and send
    msg = IoMessage()
    msg.infotype = 'application/json'
    msg.infoformat = 'text/utf-8'

    with open('data.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
        # row variable is a list that represents a row in csv
        # time = (row[0] * 1000)
            contentdata = {
                'time': str(datetime.now()),
                'speed': float(row[1]) * 2.23694,
                'acceleration': row[4],
                'rpm': row[5],
            }
            contentdata = json.dumps(contentdata)
            msg.contentdata = bytearray(contentdata)
            IoClient.post_message_via_socket(msg)


class ControlListener(IoFogControlWsListener):
    def on_control_signal(self):
        # update_config()
        return

class MessageListener(IoFogMessageWsListener):
    # Receipt of received message
    def on_receipt(self, message_id, timestamp):
        print ('Receipt: {} {}'.format(message_id, timestamp))

#update_config()
IoClient.establish_message_ws_connection(MessageListener())
IoClient.establish_control_ws_connection(ControlListener())

while True:
    send_sensor_data()