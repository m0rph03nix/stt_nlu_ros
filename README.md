# STT_NLU_ROS



## Install & Run

### Prerequisites
- ROS (tested with Melodic)
- Docker
### Run

- STT
```bash
sudo ./run.sh # Run the Whisper.cpp container with audio streaming from microphone
```
- Action server with NLU and inputs from STT
```bash
rosrun stt_nlu_node STT_NLU_server_node.py
```
- Code exemple (action client) to test the solution
```bash
rosrun stt_nlu_node client_exemple.py
``` 
 
### Errors
Because I use ROS melodic, I had to run the script in python 2.7, and I had to do this:
```bash
sudo pip uninstall backports.ssl-match-hostname
sudo apt-get install python-backports.ssl-match-hostname
```


## Warning
For now, the action server listen to whisper.cpp though docker logs (python API)... which is ugly... I know... but until I do something better, it works very well !



## Messages

### action : NLExpectations.action
```yaml
#goal
stt_nlu_msgs/Goals_NLU waitfor
---
#result
stt_nlu_msgs/Results_NLU answer
---
#feedback
int32 feedback
```

### msg : stt_nlu_msgs/Goals_NLU :
```yaml
# answers to expect
string[] person         # e.g. ['John', 'Alex', 'Tom']
string[] object         # e.g. ['Book', 'Cup', 'Sponge']
string[] drink          # e.g. ['Coke', 'Beer', 'Coffee']
string[] location       # e.g. ['Living room', 'Bedroom', 'Kitchen']
string[] action         # e.g. ['Go', 'Take', 'Give']
std_msgs/Bool ack       # e.g. True (wait for a yes/no answser with variants like 'okay', 'ok', ...
```

### msg : stt_nlu_msgs/Results_NLU
```yaml
# Answer (Best match) for each category with data and confidence (confidence is always 1 for the moment) 
stt_nlu_msgs/Result_items person
stt_nlu_msgs/Result_items object
stt_nlu_msgs/Result_items drink
stt_nlu_msgs/Result_items location
stt_nlu_msgs/Result_items action
stt_nlu_msgs/Result_items ack
```

### msg : stt_nlu_msgs/Result_items
```yaml
# word found
string data
# word confidence
float32 confidence
```
