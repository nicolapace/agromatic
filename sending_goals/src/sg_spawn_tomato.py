#!/usr/bin/env python3
# Software License Agreement (BSD License)


import rospy
import random
import time

# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult
from geometry_msgs.msg import Pose, PoseStamped, PoseArray, Quaternion, Point
from tf.transformations import quaternion_from_euler
from actionlib_msgs.msg import GoalStatusArray, GoalStatus
from gazebo_msgs.srv import SpawnModel
from gazebo_msgs.srv import GetModelState
#json
import json
from os.path import expanduser


#classe che gestisce tutto
class Sending_goal():

    def __init__(self):
        self._rate = rospy.Rate(1) # 1hz
        self._status = GoalStatus()
        self.model_coordinates = rospy.ServiceProxy( '/gazebo/get_model_state', GetModelState)
        rospy.wait_for_service("/gazebo/spawn_sdf_model")
        self._status_sub = rospy.Subscriber('/move_base/status', GoalStatusArray , self.sub_callback)
        self.pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
        self.t = random.randint(250,250)
        print("Tempo timer: " + str(self.t))
        self.t_ini = time.time() 
        self.talker()

    def setPose(self,pose):
        p = PoseStamped()
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
        
        self.pub.publish(p)

    def contr_timer(self,pose):
        print("tempo passato "+ str(time.time()-self.t_ini))
        if time.time()-self.t_ini>self.t:
            p = PoseStamped()
            p.pose.position.x = -7  # posizione del check-point
            p.pose.position.y = -6
            p.pose.position.z = 0
            p.header.frame_id="map"
            q = quaternion_from_euler(0.0, 0.0, 0.0)
            p.pose.orientation = Quaternion(*q)
            self.pub.publish(p)
            print("RITORNO ALLA BASE")
            while self._status.status != 3:
                rospy.sleep(1.)
                print("Ritorno...")
          
            #recupero il goal che avevo sospeso
            self.setPose(pose)
            print("x: " + str(pose['posizione']['x']) + ", y: "+ str(pose['posizione']['y']))
            rospy.sleep(1.)
            while self._status.status != 3:
                        print(str(self._status.text))
                        rospy.sleep(1.)
            self.t = random.randint(250,250)
            self.t_ini = time.time()


    def finalpose(self):
        p = PoseStamped()
        p.pose.position.x = -7 # posizione del check-point
        p.pose.position.y = -6
        p.pose.position.z = 0
        p.header.frame_id="map"
        q = quaternion_from_euler(0.0, 0.0, 0.0)
        p.pose.orientation = Quaternion(*q)
        self.pub.publish(p)
        print("FINITO: RITORNO ALLA BASE")
        while self._status.status != 3:
            rospy.sleep(1.)
            print("Ritorno...")

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
        file = open(str(expanduser("~"))+'/catkin_ws/src/sending_goals/pose/poses.json',)
        poses_list = json.load(file)
        i = 0
        for pose in poses_list:
            if i==0:
                print("Goal numero: "+str(i))
                print("x: " + str(pose['posizione']['x']) + ", y: "+ str(pose['posizione']['y']))
                self.setPose(pose)
                print(self._status.text)
            elif i==1:
                print("Goal numero: "+str(i))
                print("x: " + str(pose['posizione']['x']) + ", y: "+ str(pose['posizione']['y']))
                self.setPose(pose)
                print(self._status.text)
                while self._status.status != 3:
                    self.contr_timer(pose) 
                    print(self._status.text)
                    rospy.sleep(1.)
            else:
                print("Goal numero: "+str(i))
                print(self._status.text)
                if self._status.status == 3: #goal reached
                    self.setPose(pose)
                    print("x: " + str(pose['posizione']['x']) + ", y: "+ str(pose['posizione']['y']))
                    rospy.sleep(1.)
                    while self._status.status != 3:
                        self.contr_timer(pose) # Quando il timer scade viene inviata la posizione del 
                        # check-point e in seguito rinviato all'ultima posa raggiunta
                        print(self._status.text)
                        rospy.sleep(1.)
                    spawn_model_client = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
                    # self.object_coordinates = self.model_coordinates("husky", "")
                    # y = self.object_coordinates.pose.position.y
                    # x = self.object_coordinates.pose.position.x
                    posa = Pose()
                    posa.position.x = -0.1
                    posa.position.y = 0
                    posa.position.z = 1
                    posa.orientation = Quaternion(*quaternion_from_euler(0.0, 0.0, 0.0))
                    spawn_model_client('Fruit'+str(i), open(str(expanduser("~"))+"/.gazebo/models/tomato_fruit/model.sdf",'r').read(), "/foo", posa ,"base_link")
                   
                # else:
                #     while self._status.status != 3:
                #         print(str(self._status.text))
                #         rospy.sleep(1.)
            i+=1 
            self._rate.sleep()

        self.finalpose()

        

if __name__ == '__main__':
    rospy.init_node('sending_goals', anonymous=True) 
    prova = Sending_goal()