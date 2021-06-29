#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseWithCovarianceStamped
import time
from os.path import expanduser


class SavePoses(object):
    def __init__(self):
        
        self._pose = Pose()
        # self.poses_list = []
        self._pose_sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped , self.sub_callback)
        self.write_to_file()

    def sub_callback(self, msg):
        
        self._pose = msg.pose.pose
    
    def write_to_file(self):
            
        i = 0
        #aggiungere /agromatic
        with open( str(expanduser("~"))+'/catkin_ws/src/sending_goals/pose/poses.txt', 'w') as file:
            while(1):
                i+=1
                value = input("Click \"s\" to save the waypoint.\nClick \"d\" to save file.\n")
                print('You entered : '+ str(value) )
                
                if value=="s":
                        print("Posa salvata!\n"+str(self._pose))
                        file.write("posa n."+str(i) + ':\n----------\n' + str(self._pose) + '\n===========\n')

                if value=="d":
                    break        
                    
        rospy.loginfo("Written all Poses to poses.txt file")
        


if __name__ == "__main__":
    rospy.init_node('spot_recorder', log_level=rospy.INFO) 
    save_spots_object = SavePoses()
    #rospy.spin() # mantain the service open.
