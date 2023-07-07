#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import actionlib
from stt_nlu_actions.msg import NLExpectationsAction, NLExpectationsGoal, NLExpectationsResult

class NLExpectationsClient(object):
    def __init__(self):
        # Initialisation du client d'action
        self.client = actionlib.SimpleActionClient('nl_expectations', NLExpectationsAction)
        self.client.wait_for_server()

    def send_goal(self):
        goal = NLExpectationsGoal()

        goal.waitfor.person = ['John', 'Tom', 'Tony', 'Alex']

        goal.waitfor.drink = ['Fanta', 'Coke', 'Water', 'Beer']

        goal.waitfor.location = ['Living room', 'Kitchen', 'Bedroom', 'Corridor']

        goal.waitfor.action = ['Go', 'Take', 'Give']

        # Wait for an anwser among ["yes", "no", "ok", "okay" ]
        goal.waitfor.ack.data = True


        # Envoi de l'objectif (goal) au serveur
        self.client.send_goal(goal)

        # Attente du résultat avec un délai maximum de ... secondes
        self.client.wait_for_result(rospy.Duration(30))

        # Récupération du résultat de l'action
        result = self.client.get_result()

        # Traitement du résultat
        if result:
            for attr in result.answer.__slots__:
                if attr in ["person", "drink", "location", "action", "object", "ack"]:
                    value = getattr(result.answer, attr)
                    if value.data != None and value.data != '':
                        print("{name}: {value}".format(name=attr, value=value.data) )

                # elif attr == "ack":
                #     value = result.answer.ack
                #     if value.data != None and value.data != '':
                #         print("{name}: {value}".format(name=attr, value=value.data) )



if __name__ == '__main__':
    rospy.init_node('nl_expectations_client')
    client = NLExpectationsClient()
    client.send_goal()
