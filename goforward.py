#!/usr/bin/env python

'''
Copyright (c) 2015, Mark Silliman
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# A very basic TurtleBot script that moves TurtleBot forward indefinitely. Press CTRL + C to stop.  To run:
# On TurtleBot:
# roslaunch turtlebot_bringup minimal.launch
# On work station:
# python goforward.py

import rospy
from geometry_msgs.msg import Twist
from array import *

class GoForward():
    def __init__(self):
        # initiliaze
        rospy.init_node('GoForward', anonymous=False)

	# tell user how to stop TurtleBot
        rospy.loginfo("To stop TurtleBot CTRL + C")

        # What function to call when you ctrl + c
        rospy.on_shutdown(self.shutdown)

	# Create a publisher which can "talk" to TurtleBot and tell it to move
        # Tip: You may need to change cmd_vel_mux/input/navi to /cmd_vel if you're not using TurtleBot2
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

	#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(10);

        # Twist is a datatype for velocity
        move_cmd = Twist()
	# let's go forward at 0.2 m/s
        move_cmd.linear.x = 0.20
	# let's turn at 0 radians/s
        move_cmd.angular.z = 0



        controlist = [[0.2, 0],
                      [0.3, 0],
                      [0.2, 0],
                      [0.4, 0],
                      [0.2, 0],
                      [0.2, 0],
                      [0.4, 0],
                      [0.2, 0],
                      [0.3, 0],
                      [0.2, 0],
                      [0.2, 0]]
        counter = 0
        interv = 10
        wait = 15
        con_counter = 0
	# as long as you haven't ctrl + c keeping doing...
        while not rospy.is_shutdown():
            if con_counter<len(controlist)-1:
                if counter < interv:
	              #publish the velocity
                  move_cmd.linear.x = controlist[con_counter][0]
                  move_cmd.angular.z = controlist[con_counter][1]
                  self.cmd_vel.publish(move_cmd)
                  #rospy.loginfo("Forward")
                #elif counter>= interv and counter<wait:
                  #move_cmd.linear.x = 0.00
                  #move_cmd.angular.z = 0
                  #self.cmd_vel.publish(move_cmd)
                  ##rospy.loginfo("Stop")
                else:
                  #reset time counter
                  counter = -1
                  #move to the next control input
                  con_counter += 1

                #update the time counter
                counter += 1

            #all comands from controllist have been executed
            else:
              move_cmd.linear.x = 0.00
              move_cmd.angular.z = 0
              self.cmd_vel.publish(move_cmd)

            r.sleep()


    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)

if __name__ == '__main__':
    try:
    	GoForward()
    except:
    	rospy.loginfo("GoForward node terminated.")
