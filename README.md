# remote stage control demo

Demo for real-time control with xy-stage devices via web browser. 
This demo uses a web server, a stage, and a MQTT broker.
A MQTT broker is required to bidirectional communication between stage and web interface.
In MQTT, the word topic refers to a string that the broker uses to filter messages for each connected client. 
A stage named **myStage** publishes current position (and status) on the topic **stage/info/myStage** 
with a JSON encoded message payload like **{"status": {"isConnected": "false", "isRunning": "false"}, "position": {"x_world": 0.0, "y_world": 0.0}}**.
A web interface for **myStage** receives the position on the topic and updates interface in real-time.
The web interface publishes stage control commands on the topic **stage/ctrl/myStage** with message payload of **{"command":"GOTO","d_x":"35.893","d_y":"139.954"}**.
The stage receives commands on the topic and move to the position in real-time.

To install and setup, issue following commands.

    > git clone https://gitlab.misasa.okayama-u.ac.jp/DREAM/vs-remote.git
    > cd vs-remote
    > cp docker-compose.yml.example docker-compose.yml
    > docker-compose up -d
    Creating network "vs-remote_default" with the default driver
    Creating vs-remote_httpd_1     ... done
    Creating vs-remote_mosquitto_1 ... done
    Creating vs-remote_stage_1     ... done

To access the web interface for **myStage**, open a web browser with following URL. 

    http://localhost/simple.html?topic=myStage

To monitor communications between stage and web interface, issue following command. 

    > docker-compose logs -f stage
    Attaching to vs-remote_stage_1
    stage_1      | 2020-10-09 04:00:49,092 INFO:publish message {"status": {"isConnected": "false", "isRunning": "false"}, "position": {"x_world": 0.0, "y_world": 0.0}} on topic stage/info/myStage
    stage_1      | 2020-10-09 04:00:49,093 INFO:published: 1000
    stage_1      | 2020-10-09 04:00:50,096 INFO:Received message 'b'{"command":"GOTO","d_x":"35.893","d_y":"139.954"}'' on topic 'stage/ctrl/myStage' with QoS 0
    stage_1      | 2020-10-09 04:00:51,100 INFO:publish message {"status": {"isConnected": "false", "isRunning": "false"}, "position": {"x_world": 35.893, "y_world": 139.954}} on topic stage/info/myStage
    stage_1      | 2020-10-09 04:00:51,100 INFO:published: 1001

To receive current position (and status) of **myStage** with a MQTT client software (such as mosquitto_sub), issue following command. 

    > mosquitto_sub -h localhost -t stage/info/myStage
    
