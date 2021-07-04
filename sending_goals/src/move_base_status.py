#! /usr/bin/env python3
import rospy
from actionlib_msgs.msg import GoalStatusArray

class Status(object):
    def __init__(self):
        self._status_sub = rospy.Subscriber('/move_base/status', GoalStatusArray , self.sub_callback)
    
    def sub_callback(self, msg):
        self._status = msg.status_list[0].status
               
        if self._status == 3:
            print("goal raggiunto")
            print(str(self._status))
                
        else:
            print("goal non raggiunto")
            print(str(self._status))
                


if __name__ == "__main__":
    rospy.init_node('status', log_level=rospy.INFO) 
    status_object = Status()