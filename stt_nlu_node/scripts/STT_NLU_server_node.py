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

        #print( goal )

        timeout = goal.expected_timeout.data

        feedback = NLExpectationsFeedback()
        result = NLExpectationsResult()
        goal_group=goal.waitfor.goal_group

        rospy.loginfo("Begin NLExpectations action.")

        parseNLP = ParseNLP()

        id = parseNLP.get_id()
        parseNLP.set_goal(goal.waitfor)

        is_result_set= False
        

        # Exécution d'une boucle pendant 10 secondes interruptible
        rate = rospy.Rate(2)  #  2 Hz
        for i in range(timeout*2):
            if self.server.is_preempt_requested():
                # Le client a demandé de préempter l'action
                rospy.loginfo("Action NLExpectations preempted.")
                self.server.set_preempted()
                return

            # Mise à jour du feedback
            feedback.feedback = timeout - (i/2) # Compte à rebour timeout
            self.server.publish_feedback(feedback)

            rate.sleep()

            id_cmp = parseNLP.get_id()
          
            if( id < id_cmp):

                result.answer = parseNLP.get_result()


                if (    result.answer.ack.data      == '' and
                        result.answer.action.data   == '' and
                        result.answer.drink.data    == '' and
                        result.answer.location.data == '' and
                        result.answer.object.data   == '' and
                        result.answer.person.data   == ''       ):
                    print("Still waiting for expected answer...")

                else:

                    result.answer.goal_group=goal_group
                    self.server.set_succeeded(result)
                    is_result_set = True

                    print("\nGot Something\n")

                    print(result.answer)

                    id = id_cmp
                    break


            #rate.sleep()
            if i%2 == 0:
                print(i/2)

        #Need to check if no answer
        if(not is_result_set):
            result.answer.goal_group=goal_group
            self.server.set_succeeded(result)
            #self.server.set_aborted(result)

        # Fin de l'exécution de l'action
        rospy.loginfo("End of NLExpectations action.")       

        rospy.sleep(1)

if __name__ == '__main__':
    rospy.init_node('nl_expectations_server')
    server = NLExpectationsServer()
    rospy.spin()