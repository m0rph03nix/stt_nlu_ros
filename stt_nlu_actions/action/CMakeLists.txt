cmake_minimum_required(VERSION 2.8.3)
project(stt_nlu_actions)

## Add support for C++11, supported in ROS Kinetic and newer
# add_definitions(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
    rospy
    std_msgs
    actionlib_msgs 
    actionlib
    stt_nlu_msgs
    
)


## Generate actions in the 'action' folder
 add_action_files(
   FILES
   NLExpectations.action
 )

## Generate added messages and services with any dependencies listed here
 generate_messages(
   DEPENDENCIES
   std_msgs
   actionlib_msgs
   stt_nlu_msgs
   # Or other packages containing msgs
 )


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES people_face_identification
  CATKIN_DEPENDS message_runtime
#  DEPENDS system_lib
)
