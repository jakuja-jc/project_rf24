import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import paho.mqtt.client as mqtt #mqtt library for python
import random
import json

mqttc = mqtt.Client() # Define Connection
#mqttc.connect("iot.eclipse.org", 1883, 60) # Do Connection
mqttc.connect("192.168.43.250" ,1883)


GPIO.setmode(GPIO.BCM)

pipesr = [[0xF0, 0xF0, 0xF0, 0xF0, 0xD2], [0xF0, 0xF0, 0xF0, 0xF0, 0xC3]]
pipesw = [[0xF0, 0xF0, 0xF0, 0xF0, 0xB1], [0xF0, 0xF0, 0xF0, 0xF0, 0xA4]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setPayloadSize(32)
radio.setChannel (0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel (NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipesr[0])
radio.openReadingPipe(2, pipesr[1])
#radio.printDetails()
radio.startListening()

while (1):
        ackPL = [1]
        while not radio.available(0):
                time.sleep(1/100)

        receivedMessage = []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        print("Received : {}".format(receivedMessage))
        string = ""
        for n in receivedMessage:
            if (n >= 32 and n <= 126):
                string += chr(n)
        print(string)
        data = random.randrange(0, 12, 1)
        print(data)
        date = time.strftime("%d/%m/%Y")
        time1 = time.strftime("%H:%M:%S")
        data_json = json.dumps({'date' : date, 'time' : time1, 'peer' : string})
        mqttc.publish("/sensor/peer", payload=data_json, qos=0, retain=True)
