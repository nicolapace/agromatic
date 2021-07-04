#!/usr/bin/env python3
# Software License Agreement (BSD License)


import rospy

# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult
from geometry_msgs.msg import Pose, PoseStamped, PoseArray, Quaternion
from tf.transformations import quaternion_from_euler
from actionlib_msgs.msg import GoalStatusArray, GoalStatus
#json
import json
from os.path import expanduser


def setPose(p, pose):
    p.header.frame_id="map"
    p.pose.position.x = pose['posizione']['x']
    p.pose.position.y = pose['posizione']['y']
    p.pose.position.z = pose['posizione']['z']
    # q = quaternion_from_euler(0.0, 0.0, 0.0)
    # p.pose.orientation = Quaternion(*q)
    p.pose.orientation.w = pose['orientamento']['w']
    p.pose.orientation.x = pose['orientamento']['x']
    p.pose.orientation.y = pose['orientamento']['y']
    p.pose.orientation.z = pose['orientamento']['z']
    return p

#classe che gestisce tutto
class Sending_goal():
    def __init__(self):
        self._rate = rospy.Rate(1) # 1hz
        self._status = GoalStatus()
        self._status_sub = rospy.Subscriber('/move_base/status', GoalStatusArray , self.sub_callback)
        self.talker()

    #callback dello status 
    def sub_callback(self, msg):
        if(len(msg.status_list)>0):
            self._status  = msg.status_list[len(msg.status_list)-1]
        # print("goal list size: " + str(len(self._status)))
        # for stat in self._status:
           
        #     print("status_id: " + str(stat.status))
        #     print("status_text: " + stat.text)
        
        # print("il valore è: "+str(self._status)) 


    def talker(self):
        pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)   
        # rospy.init_node('BASE_CLIENT_PY', anonymous=True)
        file = open(str(expanduser("~"))+'/catkin_ws/src/sending_goals/pose/poses.json',)
        poses_list = json.load(file)

        while not rospy.is_shutdown():
            i = 0
           
            
            for pose in poses_list:
                if i==0:
                    p = PoseStamped()
                    p = setPose(p, pose)
                    #rospy.loginfo(p)
                    pub.publish(p)
                    print(str(self._status.text))
                    rospy.sleep(1.)
                else:
                    print(str(self._status.text))
                    if self._status.status == 3: #goal reached
                        
                        print(str(self._status.text))
                        p = PoseStamped()
                        p = setPose(p, pose)
                        print(i)
                        print("x: " + str(pose['posizione']['x']) + ", y: "+ str(pose['posizione']['y']))
               
                        #rospy.loginfo(p)
                        pub.publish(p) 
                        rospy.sleep(1.)
                        while self._status.status != 3:
                            print(str(self._status.text))
                            rospy.sleep(1.)
                            
                    # else:
                    #     while self._status.status != 3:
                    #         print(str(self._status.text))
                    #         rospy.sleep(10.)
                i+=1 
                self._rate.sleep()
        

if __name__ == '__main__':
    rospy.init_node('status', anonymous=True) 
    prova = Sending_goal()
        
        
#catkin_create_pkg sending_goals rospy actionlib move_base_msgs 
