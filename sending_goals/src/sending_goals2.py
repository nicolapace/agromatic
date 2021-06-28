#!/usr/bin/env python3
# Software License Agreement (BSD License)


import rospy

# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult
from geometry_msgs.msg import Pose, PoseStamped, PoseArray, Quaternion
from tf.transformations import quaternion_from_euler

def talker():
    pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)   
    rospy.init_node('BASE_CLIENT_PY', anonymous=True)
    rate = rospy.Rate(0.1) # 10sec
    while not rospy.is_shutdown():
        p = PoseStamped()
            
        p.pose.position.x = 9  
        p.pose.position.y = 5
        p.pose.position.z = 0

        p.header.frame_id="map"
        
        q = quaternion_from_euler(0.0, 0.0, 0.0)
        p.pose.orientation = Quaternion(*q)
        
        rospy.loginfo(p)
        pub.publish(p)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
        
        
#catkin_create_pkg sending_goals rospy actionlib move_base_msgs 
