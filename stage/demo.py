#!/usr/bin/env python
from optparse import OptionParser
import paho.mqtt.client as mqtt
import json
import logging
from time import sleep 
config = {
    "stage_name":"myStage",
    "mqtt_host":"mosquitto",
    "mqtt_port":1883,
    "log_level":"INFO"
    }
stage = {
    "x":0.0,
    "y":0.0
}
stage_info = {	"status":{
                            "isConnected":"false",
			    			"isRunning":"false",
			    		},
			    "position":{
                            "x_world":"",
                            "y_world":"",
                        }
            }
options = {}
def _parser():
    global config
    parser = OptionParser("""usage: %prog [options]

SYNOPSIS AND USAGE
  %prog [options]

DESCRIPTION
    MQTT publisher and subscriber for vs-remote app. This program
    publishes stage or marker position regulary and receives commands
    from vs-remote app.
    Note that this program reads `~/.vs2007rc' for configuration.
    Set `stage-name' line on the configuration file as below.

    stage-name: myStage

    If you see timeout error, set `timeout'
    line on the configration file as below and raise the
    value.  Default setting is 5000 mseconds.

    timeout: 5000  
""")
    parser.add_option("-v","--verbose",action="store_true",dest="verbose",default=False,help="make lots of noise")
    parser.add_option("--stage-name",action="store",type="string",dest="stage_name",default=config['stage_name'],help="set the name of stage to identify the MQTT message (default: '%default') which the program will publish and subscribe to.")
    parser.add_option("--mqtt-host",action="store",type="string",dest="mqtt_host",default=config['mqtt_host'],help="set the address of the MQTT broker (default: %default) which the program will connect to.")
    parser.add_option("--mqtt-port",action="store",type="int",dest="mqtt_port",default=config['mqtt_port'],help="set the port of the MQTT broker (default: %default) which the program will connect to.")
    parser.add_option("-l","--log_level",dest="log_level",default="INFO",help="set log level")
    return parser

def _parse_options():
    parser = _parser()
    (options, args) = parser.parse_args()
    options.topic_info = 'stage/info/' + options.stage_name
    options.topic_ctrl = 'stage/ctrl/' + options.stage_name

    return options, args
# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
    logging.info("Connected with result code " + str(rc))
    logging.info("subscribe topic |%s| to receive stage control command..." % options.topic_ctrl)
    client.subscribe(options.topic_ctrl)  # subするトピックを設定 

# ブローカーが切断したときの処理
def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
        print("Unexpected disconnection.")

# publishが完了したときの処理
def on_publish(client, userdata, mid):
    logging.info("published: {0}".format(mid))

# メッセージが届いたときの処理
def on_message(client, userdata, msg):
    # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
    logging.info("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))
    data = json.loads(msg.payload)
    stage["x"] = data["d_x"]
    stage["y"] = data["d_y"]

def publisher(client):
    while True:
        stage_info['position']['x_world'] = stage["x"]
        stage_info['position']['y_world'] = stage["y"]
        json_message = json.dumps( stage_info )
        client.publish(options.topic_info,json_message)
        logging.info("publish message {} on topic {}".format(json_message, options.topic_info))
        sleep(1)


def main():
    global options
    (options, args) = _parse_options()
    logging.basicConfig(level=options.log_level, format='%(asctime)s %(levelname)s:%(message)s')
    logging.info(options)

    client = mqtt.Client()
    client.on_connect = on_connect         # 接続時のコールバック関数を登録
    client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
    client.on_publish = on_publish         # メッセージ送信時のコールバック
    client.on_message = on_message
    client.connect(options.mqtt_host, options.mqtt_port, 60)
    client.loop_start()    # subはloop_forever()だが，pubはloop_start()で起動だけさせる
    publisher(client)
if __name__ == '__main__':
    main()
