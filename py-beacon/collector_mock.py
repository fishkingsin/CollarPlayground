#
# by Taka Wang
#

import ConfigParser
import paho.mqtt.client as mqtt
# from proximity import *
import time
import random
DEBUG = True

def onConnect(client, userdata, rc):
    """MQTT onConnect handler"""
    print("Connected to broker: " + str(rc))

def initMQTT(url = "localhost", port = 1883, keepalive = 60):
    """Init MQTT connection"""
    client = mqtt.Client()
    client.on_connect = onConnect
    try:
        client.connect(url, port, keepalive)
        client.loop_start()
        return client
    except Exception, e:
        print(e)
        return None
utilNext = 0
foo = ("da:9d:40:1e:7e:f7,e0:f0:81:46:9c:fc,cd:20:25:48:19:69,e0:9c:1c:5b:b6:04,ff:06:e6:2d:39:0f,f8:92:1c:fa:69:fe,e0:de:fc:4b:49:e5,d1:1a:3a:aa:ed:f7,fb:85:25:92:91:cb,e8:9a:04:f2:02:12,fb:22:35:ac:a7:31,e9:30:cd:fd:90:bc,cf:0d:0a:f0:7e:1a,dd:6f:57:29:62:0a,ec:ad:21:9a:13:6b,db:ea:c1:64:7b:34,ec:1d:8c:4a:3e:86,cc:96:bd:6f:65:5d,ff:19:75:20:86:24,00:00:00:00:00:00").split(",")
rssi = [-60.0,-66.0,-70.0,-75.0,-80.0,-85.0]
def millis():
    return int(round(time.time() * 1000))

def startScan(mqttclnt, filters=[], topic="/ble/rssi/"):
    """Scan BLE beacon and publish to MQTT broker"""
    if mqttclnt:
        # scanner = Scanner()
        global utilNext
        while True:
            if(millis()>utilNext):
                for x in xrange(1,5):
                    fields = [random.choice(foo), random.choice(rssi)]
                    found = False
                    for filter in filters:
                        if fields[0].startswith(filter):
                            mqttclnt.publish(topic, '{"id":"%s","val":"%s"}' % (fields[0], fields[1]))
                            found = True
                            print(fields[0], fields[1])
                            break;
                    if found == False:
                        print fields[0] + ' not found in filter '
                    pass

                
                utilNext =  millis() + 3000 

            # for beacon in scanner.scan():
            #     fields = beacon.split(",")
            #     for filter in filters:
            #         if fields[1].startswith(filter):
            #             mqttclnt.publish(topic, '{"id":"%s","val":"%s"}' % (fields[0], fields[5]))
            #             if DEBUG: print(fields[0], fields[5])

def init():
    """Read config file"""
    ret = {}
    config = ConfigParser.ConfigParser()
    config.read("config")
    global DEBUG
    DEBUG = True if int(config.get('Collector', 'debug')) == 1 else False
    ret["url"]       = config.get('MQTT', 'url')
    ret["port"]      = int(config.get('MQTT', 'port'))
    ret["keepalive"] = int(config.get('MQTT', 'keepalive'))
    ret["filter"]    = config.get('Scanner', 'filter').split(",")
    print ret["filter"]
    ret["topic_id"]  = config.get('Scanner', 'topic_id')
    return ret

if __name__ == '__main__':
    conf = init()
    clnt = initMQTT(conf["url"], conf["port"], conf["keepalive"])
    startScan(clnt, conf["filter"], conf["topic_id"])
