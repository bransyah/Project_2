import base64
from datetime import datetime
from google.cloud import datastore
import jwt
import ssl
import time

import paho.mqtt.client as mqtt

PROJECT_ID = "hsc2020-04"

def suhu_kelembaban(temp, humi):
     client = datastore.Client(project=PROJECT_ID)


     newKey = client.key("baca")


     newEntity = datastore.Entity(newKey)


     newEntity.update({
     "created": datetime.now(),
     "0": temp,
     "1": humi,
     })

     client.put(newEntity)

