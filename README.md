# MQTT project -- demo-stage-view 

Demo for real-time control of xy-stage devices with a web interface. 
A MQTT broker is required to bidirectional communication between stage and web interface.
In MQTT, the word topic refers to a string that the broker uses to filter messages for each connected client. 
A stage named **myStage** publishes current position (and status) on the topic **stage/info/myStage** 
with a JSON encoded message payload like the following.

`{"status": {"isConnected": "false", "isRunning": "false"}, "position": {"x_world": 0.0, "y_world": 0.0}}`

A web interface for **myStage** receives the position on the topic and updates interface in real-time.
The web interface publishes stage control commands on the topic **stage/ctrl/myStage** with message payload like the following.

`{"command":"GOTO","d_x":"35.893","d_y":"139.954"}`

The stage receives commands on the topic and move to the position in real-time.

To install and setup, issue following commands.

    $ git clone https://github.com/misasa/demo-stage-view.git
    $ cd demo-stage-view
    $ cp docker-compose.yml.example docker-compose.yml
    $ docker-compose up -d
    Creating network "demo-stage-view_default" with the default driver
    Creating demo-stage-view_mosquitto_1 ... done
    Creating demo-stage-view_httpd_1     ... done
    Creating demo-stage-view_stage_1     ... done

This setup a web interface and a MQTT broker, and creates a stage named **myStage**.
To access the web interface for **myStage**, open a web browser with following URL. 

    http://localhost/simple.html?topic=myStage

To see communications between stage and web interface, issue following command. 

    $ docker-compose logs -f stage
    Attaching to demo-stage-view_stage_1
    stage_1      | 2020-10-09 04:00:49,092 INFO:publish message {"status": {"isConnected": "false", "isRunning": "false"}, "position": {"x_world": 0.0, "y_world": 0.0}} on topic stage/info/myStage
    stage_1      | 2020-10-09 04:00:49,093 INFO:published: 1000
    stage_1      | 2020-10-09 04:00:50,096 INFO:Received message 'b'{"command":"GOTO","d_x":"35.893","d_y":"139.954"}'' on topic 'stage/ctrl/myStage' with QoS 0
    stage_1      | 2020-10-09 04:00:51,100 INFO:publish message {"status": {"isConnected": "false", "isRunning": "false"}, "position": {"x_world": 35.893, "y_world": 139.954}} on topic stage/info/myStage
    stage_1      | 2020-10-09 04:00:51,100 INFO:published: 1001

To create another stage, issue following command.

    $ docker-compose run stage --stage-name=anotherStage
    Creating demo-stage-view_stage_run ... done
    2020-10-09 09:03:45,785 INFO:{'verbose': False, 'stage_name': 'anotherStage', 'mqtt_host': 'mosquitto', 'mqtt_port': 1883, 'log_level': 'INFO', 'topic_info': 'stage/info/anotherStage', 'topic_ctrl': 'stage/ctrl/anotherStage'}
    2020-10-09 09:03:45,788 INFO:publish message {"status": {"isConnected": "false", "isRunning": "false"}, "position": {"x_world": 0.0, "y_world": 0.0}} on topic stage/info/anotherStage
    2020-10-09 09:03:45,788 INFO:Connected with result code 0
    2020-10-09 09:03:45,788 INFO:subscribe topic |stage/ctrl/anotherStage| to receive stage control command...
    2020-10-09 09:03:45,788 INFO:published: 1
    2020-10-09 09:03:46,792 INFO:publish message {"status": {"isConnected": "false", "isRunning": "false"}, "position": {"x_world": 0.0, "y_world": 0.0}} on topic stage/info/anotherStage

To receive current position (and status) of **myStage** with a MQTT client software **mosquitto_sub**, download and install the software from http://mosquitto.org/download/ and issue following command. 

    > mosquitto_sub -h localhost -t stage/info/myStage
    
