#!/usr/bin/env python3
# Software License Agreement (BSD License)

import rospy
from actionlib_msgs.msg import GoalStatusArray

class ReadGoalStatus(object):
    def __init__(self):
        
        self._status = GoalStatusArray()
        self._status_sub =  rospy.Subscriber("/move_base/status", GoalStatusArray, self.callback)
        self.listener()

    def callback(self, msg):

        self._status  = msg.status_list
        # print("goal list size: " + str(len(self._status)))
        # for stat in self._status:
           
        #     print("status_id: " + str(stat.status))
        #     print("status_text: " + stat.text)
        stat = self._status[len(self._status)-1]
        print("status_id: " + str(stat.status))
        print("status_text: " + stat.text)
    
       
    def listener(self):

        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()


if __name__ == '__main__':
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    read_status_obj = ReadGoalStatus()