import random

import time
from paho.mqtt import client as mqtt_client
from time import sleep
from threading import Thread


broker = '192.168.70.91'
port = 1883
topic = "test/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'



def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

def publish(client):
     msg_count = 0
     while True:
         time.sleep(1)
         msg = f"messages: {msg_count}"
         result = client.publish(topic, msg)
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print(f"Send `{msg}` to topic `{topic}`")
         else:
             print(f"Failed to send message to topic {topic}")
         msg_count += 1

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

def run2():
    client = connect_mqtt()
    publish(client)

if __name__ == '__main__':
    thread1 = Thread(target=run)
    thread2 = Thread(target=run2)
    thread1.start()
    thread2.start()
    print("Test")
    print("Test2")