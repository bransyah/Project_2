import mqtt_google
import mqtt_rpi
import time

def on_message_bridge(client, userdata, message):
    """Callback when the device receives a message on a subscription."""

    # Get Payload
    payload = ujson.dumps(payload).encode('utf-8')

    print("on_message: publishing to google")    
    print("  Payload: " + payload)
    print()

    # Publish to google
    client_google = mqtt_google.get_client()
    mqtt_google.publish_events(client_google, payload1)
    mqtt_google.release_client(client_google)

    
# Open Connection to the Raspberry Pi MQTT Broker
client = mqtt_rpi.get_client(on_message_bridge)
# Subscribe to the temperature reading topic at the broker
mqtt_rpi.subscribe(client, "/devices/temperature")


# Wait, since above methods are non blocking
while True:
    try:
        time.sleep(15)
    except KeyboardInterrupt:
        print("Quiting...")
        break

# We are done, close connection to the Raspberry Pi MQTT Broker
mqtt_rpi.release_client(client)

