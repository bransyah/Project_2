import datetime
import time

import paho.mqtt.client as mqtt

# Local MQTT Broker
LOCAL_MQTT_BRIDGE_HOSTNAME = "raspberrypi"
LOCAL_MQTT_BRIDGE_PORT = 1883

# Timeout to wait for connection
WAIT_CONNECTION_TIMEOUT = 5

# ID of the Gateway
GATEWAY_ID = "fog_rpi"


# Connection status
connected = False


def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return f"{rc}: {mqtt.error_string(rc)}"


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    #print('on_connect: ', mqtt.connack_string(rc))
    print(f"on_connect: {error_str(rc)} ({mqtt.connack_string(rc)})")
    print()

    global connected
    connected = True


def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print(f"on_disconnect: {error_str(rc)}")
    print()

    global connected
    connected = False


def on_publish(client, userdata, mid):
    """Paho callback when a message is sent to the broker."""
    print('on_publish')
    print("  userdata:" + str(userdata))
    print("  mid:" + str(mid))
    print()


def on_subscribe(client, userdata, mid, granted_qos):
    print("on_subscribe")
    print("  userdata:" + str(userdata))
    print("  mid:" + str(mid))
    print()


def on_unsubscribe(client, userdata, mid):
    print("on_unsubscribe")
    print("  userdata:" + str(userdata))
    print("  mid:" + str(mid))
    print()


def on_message(client, userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = str(message.payload.decode('utf-8'))
    topic = message.topic
    qos = str(message.qos)
    print("on_message")    
    print("  Topic: " + topic)
    print("  Payload: " + payload)
    print("  QoS: " + qos)
    print()


def wait_for_connection(timeout):
    """Wait for the device to become connected."""
    global connected 

    total_time = 0
    while not connected and total_time < timeout:
        time.sleep(1)
        total_time += 1

    if not connected:
        raise RuntimeError('Could not connect to MQTT bridge.')


def get_client(on_message_callback=on_message):
    # create client Object
    client = mqtt.Client(client_id=GATEWAY_ID)

    # Register message callbacks. https://eclipse.org/paho/clients/python/docs/
    # describes additional callbacks that Paho supports. In this example, the
    # callbacks just print to standard out.
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.on_unsubscribe = on_unsubscribe
    client.on_message = on_message_callback

    # Connect to the local MQTT broker
    client.connect(LOCAL_MQTT_BRIDGE_HOSTNAME, LOCAL_MQTT_BRIDGE_PORT)
    client.loop_start()
    wait_for_connection(WAIT_CONNECTION_TIMEOUT)

    return client


def wait_for_disconnection(timeout):
    """Wait for the device to become connected."""
    global connected 

    total_time = 0
    while connected and total_time < timeout:
        time.sleep(1)
        total_time += 1

    if connected:
        raise RuntimeError('Could not disconnect to MQTT bridge.')


def release_client(client):
    """"Disconnect device from broker."""
    client.disconnect()
    client.loop_stop()
    wait_for_disconnection(WAIT_CONNECTION_TIMEOUT)


def subscribe(client, mqtt_topic):
    """Subscribe to a topic."""

    print()
    print("Subscribe")
    print("================================================")
    print()

    # Subscribe to the config topic.
    print("Subscribing")
    print(mqtt_topic)
    print()
    client.subscribe(mqtt_topic, qos=1)
