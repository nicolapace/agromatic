#!/usr/bin/env python3

import random
import time
import rospy
from std_msgs.msg import String
#custom msg created for counter
from sending_goals_msgs.msg import Weight


class WeightClass():
    def __init__(self):
        rospy.init_node('weight_node', anonymous=True) 
        self._rate = rospy.Rate(1) # 1hz
        self._sub = rospy.Subscriber('weight_data', Weight , self.sub_callback)
        self._pub = rospy.Publisher('weight_toBase', Weight, queue_size=10)
        self._weightData = Weight()
        self._maxWeight = 45
        self._tomatoWeight = 0.9
        self.check_weight()
        

    def sub_callback(self, msg):
        self._weightData = msg

    def check_weight(self):

        w = Weight()

        while not rospy.is_shutdown():
            w.ToBase = False
            self._pub.publish(w)  

            print("Current weight: " + str(self._weightData.nFruits*self._tomatoWeight))
            print("Max weight: " + str(self._maxWeight))
            if self._weightData.nFruits*self._tomatoWeight>=self._maxWeight :
                self._tCount = random.randint(50,50)
                print("Max weight exceded. Going to base. ")
                self._tIni = time.time()

                w.ToBase = True
                self._pub.publish(w)  
                self._rate.sleep()
            self._rate.sleep()

if __name__ == '__main__':
    try:
        weightObj = WeightClass()
    except rospy.ROSInterruptException:
        pass
