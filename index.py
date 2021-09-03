from iofog.microservices.client import Client
from iofog.microservices.exception import IoFogException
from iofog.microservices.iomessage import IoMessage
from iofog.microservices.listener import *

from csv import reader
from datetime import datetime
import json
import time
import base64

# from iofog.microservices.log import Logger
# log = Logger('logger1')
import logging
log = logging.getLogger(__name__)

IoClient = Client(host='iofog', port='54321')


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
    print("STARTING")

    data = {
        "time": 1540855847710,
        "speed": 41.71445712,
        "acceleration": "0.52431",
        "rpm": "2078.3"
    }
    print("Before json dump")
    contentdata = json.dumps(data)
    print("After json dump")
    try:
        msg = IoMessage()
        msg.infotype = 'application/json'
        msg.infoformat = 'text/utf-8'
        contentdata = base64.b64decode(contentdata)
        msg.contentdata = str.encode(contentdata)
    except IoFogException as e:
        print("Error: ", e)
    except Exception as er:
        print("Error general: ", er)
 
    #msg = IoMessage.from_json(json_msg)
    print("Sending")
    try:
        IoClient.post_message_via_socket(msg)
    except IoFogException as e:
        print("Error: ", e)
    # with open('data.csv', 'r') as read_obj:
    #     csv_reader = reader(read_obj)
    #     data = list(csv_reader)
    #     # Iterate over each row in the csv using reader object
    # for row in data:
    # # row variable is a list that represents a row in csv
    # # time = (row[0] * 1000)
    #     data = {
    #         'time': str(datetime.now()),
    #         'speed': float(row[1]) * 2.23694,
    #         'acceleration': row[4],
    #         'rpm': row[5],
    #     }

    #     contentdata = json.dumps(data)
    #     json_msg = {
    #         'INFO_TYPE': 'application/json',
    #         'INFO_FORMAT': 'text/utf-8',
    #         'CONTENT_DATA': contentdata
    #     }
    #     #print(json_msg)
    #     msg = IoMessage.from_json(json_msg)
    #     #print(msg)
    #     print("Sending")
    #     IoClient.post_message_via_socket(msg)


class ControlListener(IoFogControlWsListener):
    def on_control_signal(self):
        # update_config()
        print("Control listener")

class MessageListener(IoFogMessageWsListener):
    # Receipt of received message
    def on_receipt(self, message_id, timestamp):
        print ('Receipt: {} {}'.format(message_id, timestamp))

# update_config()
IoClient.establish_message_ws_connection(MessageListener())
IoClient.establish_control_ws_connection(ControlListener())

while True:
    send_sensor_data()
    time.sleep(1)
    print("resend")
