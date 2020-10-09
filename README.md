# vs-remote

Provide interface for real-time interaction with stage devices. 

# demo
    > git clone https://gitlab.misasa.okayama-u.ac.jp/DREAM/vs-remote.git
    > cd vs-remote
    > cp docker-compose.yml.example docker-compose.yml
    > docker-compose up -d
    > python -m webbrowser http://localhost/simple.html?topic=myStage

To show communications between the interface and stage. 

    > docker-compose logs -f stage
    Attaching to vs-remote_stage_1
    stage_1      | 2020-10-09 04:00:49,092 INFO:publish message {"status": {"isConnected": "false", "isRunning": "false"}, "position": {"x_world": 0.0, "y_world": 0.0}} on topic stage/info/myStage
    stage_1      | 2020-10-09 04:00:49,093 INFO:published: 1
    stage_1      | 2020-10-09 04:00:50,096 INFO:publish message {"status": {"isConnected": "false", "isRunning": "false"}, "position": {"x_world": 0.0, "y_world": 0.0}} on topic stage/info/myStage
    stage_1      | 2020-10-09 04:00:50,096 INFO:published: 3
    stage_1      | 2020-10-09 04:00:51,100 INFO:publish message {"status": {"isConnected": "false", "isRunning": "false"}, "position": {"x_world": 0.0, "y_world": 0.0}} on topic stage/info/myStage
    stage_1      | 2020-10-09 04:00:51,100 INFO:published: 4

or

    > mosquitto_sub -h localhost -t stage/info/myStage