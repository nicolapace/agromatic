#!/usr/bin/env python3
# Software License Agreement (BSD License)


import rospy
import time
import random

# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult
from geometry_msgs.msg import Pose, PoseStamped, PoseArray, Quaternion
from tf.transformations import quaternion_from_euler

flag=True # Lavoro non ancora ultimato

def talker():
    pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)   
    rospy.init_node('BASE_CLIENT_PY', anonymous=True)
    rate = rospy.Rate(0.1) # 10sec

    t = random.randint(30,40)
    print("tempo timer: " + str(t))

    while not rospy.is_shutdown():
        while flag==True:
            
            t_ini = time.time()
            print( "RICARICA")
            while time.time()-t_ini<t:
                tempo_passato = time.time()-t_ini
                print( "livello del contatore: " + str(tempo_passato))
                p = PoseStamped()

                p.pose.position.x = random.randint(0,5)  
                p.pose.position.y = random.randint(0,5) 
                p.pose.position.z = 0
                # aggiungere codice in modo che quando finisce il giro, setta flag=False

                p.header.frame_id="odom"

                q = quaternion_from_euler(0.0, 0.0, 0.0)
                p.pose.orientation = Quaternion(*q)
                pub.publish(p)
                #rospy.loginfo(p)
                print("goal: "+ str(p.pose.position.x) + ", "  +str(p.pose.position.y))
                rate.sleep()

            p = PoseStamped()
            p.pose.position.x = 8  # posizione del check-point
            p.pose.position.y = 8
            p.pose.position.z = 0
            p.header.frame_id="odom"
            q = quaternion_from_euler(0.0, 0.0, 0.0)
            p.pose.orientation = Quaternion(*q)
            pub.publish(p)
            #rospy.loginfo(p)
            print("goal: "+ str(p.pose.position.x) + ", "  +str(p.pose.position.y))
            rate.sleep()
            
        p = PoseStamped()
        p.pose.position.x = 8  # posizione del check-point
        p.pose.position.y = 8
        p.pose.position.z = 0
        p.header.frame_id="odom"
        q = quaternion_from_euler(0.0, 0.0, 0.0)
        p.pose.orientation = Quaternion(*q)
        #rospy.loginfo(p)
        pub.publish(p)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
        
        
#catkin_create_pkg sending_goals rospy actionlib move_base_msgs 
