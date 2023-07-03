import docker
from typing import Optional
import re
from time import sleep

from stt_nlu_msgs.msg import Results_NLU, Goals_NLU, Result_items

class ParseNLP(object):

    def __init__(self):

        # goal contains the word woncepts we are waiting for
        self.goal = Goals_NLU()

        # Create a Docker client
        self.client = docker.from_env()

        # Get the container ID or name
        self.container_id = 'whisper.cpp'

        self.last_ids = []

        check_docker = False
        timeout = 10

        while( check_docker != True):

            check_docker = self.is_container_running(self.container_id)

            if(timeout > 0):
                timeout = timeout - 1
                print("Check if " + self.container_id + " is running ...")
            else:
                assert(self.container_id + " container NOT Running")

        print("Container " + self.container_id + " is RUNNING")




    def is_container_running(self, container_name):
        """Verify the status of a container by it's name

        :param container_name: the name of the container
        :return: boolean or None
        """
        RUNNING = "running"

        docker_client = docker.from_env()

        try:
            container = docker_client.containers.get(container_name)
        except docker.errors.NotFound as exc:
            print("Check container name!\n" + exc.explanation)
        else:
            container_state = container.attrs["State"]
            return container_state["Status"] == RUNNING


    def parse_transcriptions(self, text):
        start_tag = "### Transcription"
        end_tag = "END"
        regex_pattern = r"{} (\d+) {}".format(re.escape(start_tag), re.escape(end_tag))
        matches = re.findall(regex_pattern, text, re.MULTILINE)

        transcriptions = []

        for match in matches:
            start_index = text.find("{} {} START".format(start_tag, match))
            end_index = text.find("{} {} END".format(start_tag, match))
            if start_index == -1 or end_index == -1:
                continue

            start_index = text.find("\n", start_index) + 1
            end_index = text.rfind("\n", start_index, end_index)

            transcription = text[start_index:end_index]
            transcription = re.sub(r'\[.*?\]', '', transcription)  # Ignore content between brackets
            transcription = re.sub(r'\(.*?\)', '', transcription)  # Ignore content between parentheses
            transcriptions.append(transcription.strip())

        return transcriptions



    def find_element_in_sentence(self, element_list, sentence):
        for element in element_list:
            pattern = r'\b{}\b'.format(re.escape(element))
            if re.search(pattern, sentence, re.IGNORECASE):
                return element
        return None



    def get_transcription(self):
        logs = self.client.containers.get(self.container_id).logs()

        # Decode the logs from bytes to string
        decoded_logs = logs.decode('utf-8')

        transcriptions = self.parse_transcriptions(decoded_logs)

        return transcriptions    


    def get_id(self):
        transcription = self.get_transcription()

        return len(transcription)     
    
    def set_goal(self, goal):
        self.goal = goal


    def get_result(self):

        res = Results_NLU()

        transcriptions = self.get_transcription()

        for i,attr in enumerate(self.goal.__slots__):
            if attr in ["person", "drink", "location", "action", "object"]:
                value = getattr(self.goal, attr)
                print(attr, value)
                item = self.find_element_in_sentence(value, transcriptions[-1])
                if item:
                    if attr in res.__slots__:

                        resi = Result_items()
                        #print()
                        resi.data = str(item)
                        setattr(res, res.__slots__[res.__slots__.index(attr)], resi)

                elif ((len(transcriptions)-1) not in self.last_ids) and (len(transcriptions)>=2):
                    item = self.find_element_in_sentence(value, transcriptions[-2])
                    if item:
                        if attr in res.__slots__:

                            resi = Result_items()
                            #print()
                            resi.data = str(item)
                            setattr(res, res.__slots__[res.__slots__.index(attr)], resi)                    


            elif attr == "ack":
                value = self.goal.ack
                if value.data == True:
                    item = self.find_element_in_sentence(["yes", "no", "ok", "okay" ], transcriptions[-1])
                    if item:
                        item = item.lower()
                        if item in ['yes', 'ok', 'okay'] :
                            res.ack.data = "yes"
                        elif item in ["no"]:
                            res.ack.data = "no"
                    elif ((len(transcriptions)-1) not in self.last_ids) and (len(transcriptions)>=2) :
                        item = self.find_element_in_sentence(["yes", "no", "ok", "okay" ], transcriptions[-2])
                        if item:
                            item = item.lower()
                            if item in ['yes', 'ok', 'okay'] :
                                res.ack.data = "yes"
                            elif item in ["no"]:
                                res.ack.data = "no"
                        else:
                            res.ack.data = ''
                    else:
                        res.ack.data = ''

        return res