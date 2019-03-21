from flask import Flask, request, render_template
from flask_cors import CORS
import json
import time
import datetime
import os
import RPi.GPIO as GPIO

app = Flask(__name__)
CORS(app)

statusJSONFile = "./IO/status.json"

@app.route("/write", methods=['POST'])
def write_data():
    data = request.get_json()
    with open(statusJSONFile, 'w') as f:
        f.write(json.dumps(data))
    analyse(data)
    return "OK"

@app.route("/read")
def read_data():
    data = ''
    with open(statusJSONFile, 'r') as f:
        data = f.read()
    return data

@app.route("/")
def index():
    return render_template('index.html')

#Phils Stuff

#setup GPIO using Board numbering + Pin setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(11, GPIO.RISING, bouncetime=300)
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(12, GPIO.RISING, bouncetime=300)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

#turning the server on/off with buttons on Raspberry
    if(GPIO.input(11)):
        print("turn on/off now")
        GPIO.output(16, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(16, GPIO.LOW)

    if(GPIO.input(12)):
        print("emergency turn off")
        GPIO.output(15, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(15, GPIO.LOW)

#turning on/off the Server with help of internet
def analyse(data):
    foo = 1
#   if(data.status = aus):
#       print("NotAus")
    if(data.status):
        print("anschalten")
        GPIO.output(16, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(16, GPIO.LOW)
    else:
        print("ausschalten")
        GPIO.output(16, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(16, GPIO.LOW)

#is needed to reset the status of any GPIO pins when you exit the programm
GPIO.cleanup()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)   
