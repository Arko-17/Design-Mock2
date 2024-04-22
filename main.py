import paho.mqtt.client as mqtt
import time
from flask import Flask, render_template

app = Flask(__name__)

# Initialize detection variable
detection = 1  # Assuming the initial value is "0"

# Define on_connect callback
def on_connect(client, userdata, flags, rc):
    client.subscribe("topicName/pir")

# Define on_message callback
def on_message(client, userdata, msg):
    global detection
    detection = msg.payload.decode("utf8")

@app.route('/', methods=['GET'])
def check_detection():
    client = mqtt.Client()  
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.emqx.io", 1883)
    client.loop_start()  
    
    for i in range(10):  # Run for 10 iterations
        time.sleep(5)
        print("Detection Data", detection)
    
    client.loop_stop()  # Stop MQTT client loop after loop completion
    
    return render_template('index.html', status=int(detection))  # Moved outside the loop

if __name__ == '__main__':
    app.run(port=5001)
