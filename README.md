# vs-remote

Provide interface for real-time interaction with stage devices. 

# demo
    > git clone https://gitlab.misasa.okayama-u.ac.jp/DREAM/vs-remote.git
    > cd vs-remote
    > cp docker-compose.yml.example docker-compose.yml
    > docker-compose up -d
    > python -m webbrowser http://localhost/simple.html?topic=myStage

    > mosquitto_pub -h localhost -d -t stage/info/myStage -m "{\"position\":{\"x_world\":\"0.0\", \"y_world\":\"0.0\"}}"
    
    > mosquitto_sub -h localhost -d -t stage/info/myStage