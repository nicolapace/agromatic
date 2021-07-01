#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseWithCovarianceStamped
import time
from os.path import expanduser
import json


class SavePoses(object):
    def __init__(self):
        
        self._pose = Pose()
        # self.poses_list = []
        self._poses_dict = {}
        self._pose_sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped , self.sub_callback)
        self.write_to_file()

    def sub_callback(self, msg):
        
        self._pose = msg.pose.pose

    
    def write_to_file(self):
            
        i = 0
       
        with open('prova.json', 'w') as json_file:
            
            while(1):
                i+=1
                value = input("Click \"s\" to save the waypoint.\nClick \"d\" to save file.\n")
                print('You entered : '+ str(value) )
                
                if value=="s":
                        self._poses_dict["posa" + str(i)] = {
                            "posizione":{
                                "x":self._pose.position.x,
                                "y":self._pose.position.y,
                                "z":self._pose.position.z
                            }, 
                            "orientamento":{
                                "x":self._pose.orientation.x,
                                "y":self._pose.orientation.y,
                                "z":self._pose.orientation.z, 
                                "w":self._pose.orientation.w
                            }
                        }
                             
                        print("Posa salvata!\n"+str(self._pose))

                if value=="d":
                    json.dump(self._poses_dict,json_file)
                    break        
                    
        rospy.loginfo("Written all Poses to poses.json file")
        


if __name__ == "__main__":
    rospy.init_node('spot_recorder', log_level=rospy.INFO) 
    save_spots_object = SavePoses()
    #rospy.spin() # mantain the service open.