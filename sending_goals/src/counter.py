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
        self._sub = rospy.Subscriber('counter_reset', Counter , self.sub_callback)
        self._pub = rospy.Publisher('counter', Counter, queue_size=10)
        self._counterData = Counter()
        self._tCount = 0
        self._tIni = 0
        self.count()
        

    def sub_callback(self, msg):
        self._counterData = msg

    def count(self):
        while not rospy.is_shutdown():
            rospy.loginfo("Reset counter: " + str(self._counterData.Reset))
            if self._counterData.Reset == True:
                self._tCount = random.randint(50,50)
                print("Tempo timer: " + str(self._tCount))
                self._tIni = time.time()
                c = Counter()
                print("Tempo passato: " + str( round(time.time()-self._tIni,2) ))
                while time.time()-self._tIni<self._tCount:
                    c.ToBase = False
                    self._pub.publish(c) 
                    print("Tempo passato: " + str( round(time.time()-self._tIni,2) ))
                    self._rate.sleep() 
                #when counter ended send ToBase
                c.ToBase = True
                self._pub.publish(c)  
            self._rate.sleep()

if __name__ == '__main__':
    try:
        counterObj = CounterClass()
    except rospy.ROSInterruptException:
        pass
