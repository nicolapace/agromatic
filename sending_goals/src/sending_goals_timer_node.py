#!/usr/bin/env python3
# Software License Agreement (BSD License)


import rospy
import random
import time

# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult
from geometry_msgs.msg import Pose, PoseStamped, PoseArray, Quaternion
from tf.transformations import quaternion_from_euler
from actionlib_msgs.msg import GoalStatusArray, GoalStatus
#custom msg created for counter
from sending_goals_msgs.msg import Counter

#json
import json
from os.path import expanduser


#classe che gestisce tutto
class Sending_goal():

    def __init__(self):
        rospy.init_node('sending_goals', anonymous=True) 
        self._rate = rospy.Rate(1) # 1hz
        self._status = GoalStatus()
        self._status_sub = rospy.Subscriber('/move_base/status', GoalStatusArray , self.sub_status_callback)
        self._goal_pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)

        self._counterData = Counter()
        self._counter_sub = rospy.Subscriber('counter', Counter , self.sub_counter_callback)
        self._counter_pub = rospy.Publisher('counter_reset', Counter, queue_size=10)

        self.talker()

    #callback dello status 
    def sub_status_callback(self, msg):
        if(len(msg.status_list)>0):
            self._status  = msg.status_list[len(msg.status_list)-1]

    def sub_counter_callback(self, msg):
        self._counterData = msg

    def setPose(self,pose):
        p = PoseStamped()
        p.header.frame_id="map"
        p.pose.position.x = pose['posizione']['x']
        p.pose.position.y = pose['posizione']['y']
        p.pose.position.z = pose['posizione']['z']
        p.pose.orientation.w = pose['orientamento']['w']
        p.pose.orientation.x = pose['orientamento']['x']
        p.pose.orientation.y = pose['orientamento']['y']
        p.pose.orientation.z = pose['orientamento']['z']
        self._goal_pub.publish(p)

    def counterReset(self, reset):
        c = Counter()
        c.ToBase = False
        c.Reset = reset
        self._counter_pub.publish(c)

    def contr_timer(self,pose):
        
        if self._counterData.ToBase: #se dal topic del counter leggo il flag di toBase

            self.counterReset(False)

            p = PoseStamped()
            p.pose.position.x = -7  # posizione del check-point
            p.pose.position.y = -6
            p.pose.position.z = 0
            p.header.frame_id="map"
            q = quaternion_from_euler(0.0, 0.0, 0.0)
            p.pose.orientation = Quaternion(*q)
            self._goal_pub.publish(p)
            rospy.loginfo("RITORNO ALLA BASE")
            while self._status.status != 3:
                rospy.sleep(1.)
                rospy.loginfo("Ritorno alla base in corso...")
          
            #recupero il goal che avevo sospeso
            self.setPose(pose)
            rospy.loginfo("GOAL: x: " + str(round(pose['posizione']['x'],2)) + ", y: "+ str(round(pose['posizione']['y'],2)))
            rospy.sleep(1.)
            while self._status.status != 3:
                        print(str(self._status.text))
                        rospy.sleep(1.)

            self.counterReset(True)


    def finalpose(self):
        p = PoseStamped()
        p.pose.position.x = -7 # posizione del check-point
        p.pose.position.y = -6
        p.pose.position.z = 0
        p.header.frame_id="map"
        q = quaternion_from_euler(0.0, 0.0, 0.0)
        p.pose.orientation = Quaternion(*q)
        self._goal_pub.publish(p)
        print("FINITO: RITORNO ALLA BASE")
        while self._status.status != 3:
            rospy.sleep(1.)
            print("Ritorno...")

    def talker(self):
        file = open(str(expanduser("~"))+'/catkin_ws/src/sending_goals/pose/poses.json',)
        poses_list = json.load(file)
        i = 0
        for pose in poses_list:
            if i==0:
                self.setPose(pose)

                rospy.loginfo("Goal numero: "+str(i))
                rospy.loginfo("GOAL: x: " + str(round(pose['posizione']['x'],2)) + ", y: "+ str(round(pose['posizione']['y'],2)))
                rospy.loginfo(self._status.text)
                rospy.sleep(1.)
                rospy.sleep(1.)

            elif i==1:
                self.counterReset(True)
                self.setPose(pose)
                

                rospy.loginfo("Goal numero: "+str(i))
                rospy.loginfo("GOAL: x: " + str(round(pose['posizione']['x'],2)) + ", y: "+ str(round(pose['posizione']['y'],2)))
                rospy.loginfo(self._status.text)

                self.setPose(pose)
                while self._status.status != 3:
                    self.contr_timer(pose) 
                    rospy.loginfo(self._status.text)
                    rospy.sleep(1.)
            else:

                rospy.loginfo("Goal numero: "+str(i))
                rospy.loginfo(self._status.text)

                if self._status.status == 3: #goal reached
                    self.setPose(pose)

                    rospy.loginfo("GOAL: x: " + str(round(pose['posizione']['x'],2)) + ", y: "+ str(round(pose['posizione']['y'],2)))
                    rospy.sleep(1.)
                    while self._status.status != 3:

                        # Quando il timer scade viene inviata la posizione del 
                        # check-point e in seguito rinviato all'ultima posa raggiunta
                        self.contr_timer(pose)
                        
                        rospy.loginfo(self._status.text)
                        rospy.sleep(1.)
               
            i+=1 
            self._rate.sleep()

        self.finalpose()

        

if __name__ == '__main__':
    try:
        sendingGoals = Sending_goal()
    except rospy.ROSInterruptException:
        pass
    
        
        
#catkin_create_pkg sending_goals rospy actionlib move_base_msgs 
