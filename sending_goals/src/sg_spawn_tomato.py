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
from gazebo_msgs.srv import DeleteModel, SpawnModel
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
        self.maxWeight=50*0.09

        self.spawn_model_client = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        self.delete_model = rospy.ServiceProxy("gazebo/delete_model", DeleteModel)

        self.nFruits = 0
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

    def svuota_cassetta(self,i):
        #svuoto la cassetta
            for x in range(0, self.nFruits):
                self.delete_model("Fruit"+str(x))

                posa = Pose()
                posa.position.x = -7+random.randint(0,600)/1000-0.3
                posa.position.y = -9+random.randint(0,600)/1000-0.3
                posa.position.z = 2.5
                posa.orientation = Quaternion(*quaternion_from_euler(0.0, 0.0, 0.0))
                self.spawn_model_client('Fruit_pick_up'+str(x)+str(i),
                                        open(str(expanduser("~"))+"/.gazebo/models/tomato_fruit/model.sdf",'r').read(),
                                        "/foo",
                                        posa ,
                                        "map")
            self.nFruits = 0

    def contr_timer(self,pose,i):
        print("Peso attuale: "+ str(self.nFruits*0.09))
        if self.nFruits*0.09>=self.maxWeight:
            p = PoseStamped()
            p.pose.position.x = -6.9 # posizione del check-point
            p.pose.position.y = -6.1
            p.pose.position.z = 0
            p.header.frame_id="map"
            q = quaternion_from_euler(0.0, 0.0, 0.022140)
            p.pose.orientation = Quaternion(*q)
            self.pub.publish(p)
            print("RITORNO ALLA BASE")
            while self._status.status != 3:
                rospy.sleep(1.)
                print("Ritorno...")

            self.svuota_cassetta(i)

            #recupero il goal che avevo sospeso
            self.setPose(pose)
            print("x: " + str(pose['posizione']['x']) + ", y: "+ str(pose['posizione']['y']))
            rospy.sleep(1.)
            while self._status.status != 3:
                        print(str(self._status.text))
                        rospy.sleep(1.)
                        self.spawn_fruits(1)
            


    def finalpose(self):
        p = PoseStamped()
        p.pose.position.x = -6.9 # posizione del check-point
        p.pose.position.y = -6.1
        p.pose.position.z = 0
        p.header.frame_id="map"
        q = quaternion_from_euler(0.0, 0.0, 0.022140)
        p.pose.orientation = Quaternion(*q)
        self.pub.publish(p)
        print("FINITO: RITORNO ALLA BASE")
        rospy.sleep(1.)
        while self._status.status != 3:
            rospy.sleep(1.)
            print("Ritorno...")
        self.svuota_cassetta(10e5)

    def spawn_fruits(self,n):
        n_fruits = int(random.randint(int(n),2*int(n))/2)
        for i in range(self.nFruits,self.nFruits+n_fruits):
            posa = Pose()
            posa.position.x = -0.07+random.randint(0,8)/100-0.04
            posa.position.y = 0+random.randint(0,8)/100-0.04
            posa.position.z = 0.8
            posa.orientation = Quaternion(*quaternion_from_euler(0.0, 0.0, 0.0))
            self.spawn_model_client('Fruit'+str(i),
                                    open(str(expanduser("~"))+"/.gazebo/models/tomato_fruit/model.sdf",'r').read(),
                                    "/foo",
                                    posa ,
                                    "base_link")
        self.nFruits+=n_fruits
                   

    #callback dello status 
    def sub_callback(self, msg):
        if(len(msg.status_list)>0):
            self._status  = msg.status_list[len(msg.status_list)-1]

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
                rospy.sleep(1.)
                self.setPose(pose)
                print(self._status.text)
                while self._status.status != 3:
                    self.contr_timer(pose,i) 
                    print(self._status.text)
                    rospy.sleep(1.)
                    self.spawn_fruits(1)
                self.spawn_fruits(6)
               
            else:
                print("Goal numero: "+str(i))
                print(self._status.text)
                if self._status.status == 3: #goal reached
                    self.setPose(pose)
                    print("x: " + str(pose['posizione']['x']) + ", y: "+ str(pose['posizione']['y']))
                    rospy.sleep(1.)
                    while self._status.status != 3:
                        self.contr_timer(pose,i) # Quando il timer scade viene inviata la posizione del 
                        # check-point e in seguito rinviato all'ultima posa raggiunta
                        print(self._status.text)
                        rospy.sleep(1.)
                        self.spawn_fruits(1)
                    self.spawn_fruits(6)
            i+=1 
            self._rate.sleep()

        self.finalpose()

        

if __name__ == '__main__':
    rospy.init_node('sending_goals', anonymous=True) 
    prova = Sending_goal()