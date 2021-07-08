#!/usr/bin/env python3

import random
import time
import rospy
from std_msgs.msg import String
#custom msg created for counter
from sending_goals_msgs.msg import Counter


class CounterClass():
    def __init__(self):
        rospy.init_node('counter', anonymous=True) 
        self._rate = rospy.Rate(1) # 1hz
        self._sub = rospy.Subscriber('counter', Counter , self.sub_callback)
        self._pub = rospy.Publisher('counter', Counter, queue_size=10)
        self._counterData = Counter()
        self._tCount = random.randint(100,140)
        rospy.loginfo("Tempo timer: " + str(self.t))
        self._tIni = time.time() 
        self.count()
        

    def callback(self, msg):
        self._counterData = msg.data

    def count(self):
        while not rospy.is_shutdown():
            if self._counterData.Reset == True:
                self.tCount = random.randint(100,140)
                print("Tempo timer: " + str(self.t))
                self.tIni = time.time()
                c = Counter()
                while time.time()-self._tIni<self._tCount:
                    c.Reset = False
                    c.ToBase = False
                    self._pub(c)  
                #when counter ended send ToBase
                c.Reset = False
                c.ToBase = True
                self._pub(c)  
        self._rate.sleep()

if __name__ == '__main__':
    try:
        counterObj = CounterClass()
    except rospy.ROSInterruptException:
        pass
