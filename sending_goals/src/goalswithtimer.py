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

def talker():
    pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)   
    rospy.init_node('BASE_CLIENT_PY', anonymous=True)
    rate = rospy.Rate(0.5) # 20sec

    flag=True # Lavoro non ancora ultimato

    t = random.randint(20,22)
    print("tempo timer: " + str(t))
    t_ini = time.time()

    i=1 #numero di goals inviati
    while not rospy.is_shutdown():
        while flag==True:  # sostituire if con while        
 #           t_ini = time.time()
 #           print( "RICARICA")
            while time.time()-t_ini<t:
                    print(str(i)+"° goal")
                    tempo_passato = time.time()-t_ini
                    print( "Tempo trascorso: " + str(tempo_passato))
                    p = PoseStamped()

                    p.pose.position.x = random.randint(-2,2)  
                    p.pose.position.y = random.randint(-2,2) 
                    p.pose.position.z = 0
                    # aggiungere codice in modo che quando finisce il giro, setta flag=False

                    p.header.frame_id="map"

                    q = quaternion_from_euler(0.0, 0.0, 0.0)
                    p.pose.orientation = Quaternion(*q)
                    pub.publish(p)
                    #rospy.loginfo(p)
                    print("goal: "+ str(p.pose.position.x) + ", "  +str(p.pose.position.y))
                    i+=1
                    rate.sleep()

            p = PoseStamped()
            p.pose.position.x = 0  # posizione del check-point
            p.pose.position.y = 0
            p.pose.position.z = 0
            p.header.frame_id="map"
            q = quaternion_from_euler(0.0, 0.0, 0.0)
            p.pose.orientation = Quaternion(*q)
            pub.publish(p)
            #rospy.loginfo(p)
            print("RITORNO ALLA BASE")
            print("goal: "+ str(p.pose.position.x) + ", "  +str(p.pose.position.y))
            flag=False
            rate.sleep()
            
        # p = PoseStamped()
        # p.pose.position.x = 8  # posizione del check-point
        # p.pose.position.y = 8
        # p.pose.position.z = 0
        # p.header.frame_id="map"
        # q = quaternion_from_euler(0.0, 0.0, 0.0)
        # p.pose.orientation = Quaternion(*q)
        # #rospy.loginfo(p)
        # pub.publish(p)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
        
        
#catkin_create_pkg sending_goals rospy actionlib move_base_msgs 

# Il problema del primo goal non trovato potrebbe essere risolto implementando il codice di conferma arrivo al punto, in quanto
# potrebbe dipendere da un ritardo nella ricezione dei goals (vedi frequenza di lettura dell'amcl_demo).
# RESTA DA CAPIRE PERCHE' POI NE INVIA DUE CONSECUTIVI