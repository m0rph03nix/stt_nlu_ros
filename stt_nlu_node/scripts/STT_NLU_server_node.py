#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rospy
import actionlib
from stt_nlu_actions.msg import NLExpectationsAction, NLExpectationsResult, NLExpectationsFeedback
from stt_nlu_msgs.msg import Results_NLU, Goals_NLU, Result_items

from process.parseNLP import ParseNLP

class NLExpectationsServer(object):
    def __init__(self):
        # Initialisation du serveur d'action
        self.server = actionlib.SimpleActionServer('nl_expectations', NLExpectationsAction, self.execute, False)
        self.server.start()

    def execute(self, goal):

        print( goal )

        feedback = NLExpectationsFeedback()
        result = NLExpectationsResult()

        rospy.loginfo("Begin NLExpectations action.")

        parseNLP = ParseNLP()

        id = parseNLP.get_id()
        parseNLP.set_goal(goal.waitfor)
        

        # Exécution d'une boucle pendant 10 secondes interruptible
        rate = rospy.Rate(2)  #  2 Hz
        for i in range(20):
            if self.server.is_preempt_requested():
                # Le client a demandé de préempter l'action
                rospy.loginfo("Action NLExpectations preempted.")
                self.server.set_preempted()
                return

            # Mise à jour du feedback
            feedback.feedback = 10 - (i/2) # Compte à rebour timeout
            self.server.publish_feedback(feedback)

            id_cmp = parseNLP.get_id()
            if( id != id_cmp):
                result.answer = parseNLP.get_result()

                self.server.set_succeeded(result)

                print(result.answer)

            rate.sleep()

        # Fin de l'exécution de l'action
        rospy.loginfo("End of NLExpectations action.")       

        rospy.sleep(1)

if __name__ == '__main__':
    rospy.init_node('nl_expectations_server')
    server = NLExpectationsServer()
    rospy.spin()