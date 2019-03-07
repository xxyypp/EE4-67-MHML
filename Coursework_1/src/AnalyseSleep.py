##  @package docstring
#   Documentation for Sleep Analysis Algorithm
#
#   Implements the 5 phases of sleep, where 0 is awake and 5 is the deepest sleep. (Refer to diagram on github).

import math

##  AnalyseSleep Class
#
#   Implementation of sleep analysis algorithm. Uses accelerometer and microphone.
class AnalyseSleep:

    ##  Sleep Phase thresholds. Uses reperesents accelerations in m/s^2.
    stage_threshold = [0.5, 0.2, 0.15, 0.07] 
    
    ##  Microphone threshold values. Measured in decibels (dB).
    mic_threshold = [1.6, 2.5]
    
    ##  Threshold to make sure the phases is changing.
    #   Control the error rate of changing wrong states.
    rep_threshold = 2

    ##  Number of sleep phases. States: 0 (Awake), 1 (First stage of sleep), 2, 3, 4, 5 (last stage of sleep). 
    max_depth = 5
   

    ## Constructor to initialise parameters/variables
    def __init__(self):
        ## Current state
        self.current_state = 0
        ## Refer to diagrams in datasheet.
        self.l_thr = 1 
        ## After going to higher threshold phase, sleep cannot go lower than this.
        # until after a reset (ie user wakes up, phase = 0).
        self.h_thr = self.max_depth     
        ## Counter to indicate whether change state or not.                               
        self.counter = 0
        ## Boolean to indicate increase or decrease the phases.
        self.inc = True
        ## Next high threshold
        self.next_h = self.max_depth

    ##  Categorises sleep into phases
    #   @param self The object pointer
    #   @param data 3 element array containing x,y,z accelerations
    #   @param mic  Microphone reading in dB
    def categ_sleep(self, data, mic):
        if len(data) == 0:
            raise Exception("No data input given")
        
        prev_state = self.current_state
        inc_bool = 0
        # If h_thr == 1, reset
        if self.h_thr <= 1:
            self.next_h = self.max_depth
            self.current_state = 0

        # Increment or Decrement the phases
        if self.inc == True:
            self.inc_sleep_state(data, mic)

        else:
            for i in range(len(data)):
                if self.dec_sleep_state(math.fabs(data[i]), mic):
                    break
            

        self.h_thr = self.next_h

        print("First time:", "l_thr:", self.l_thr, "h_thr:", self.h_thr, sep=" ")
        # Change the threshold and determine whether to increment or decremeent 
        if (self.current_state >= self.h_thr):
            self.inc = False
        elif self.current_state <= self.l_thr:
            self.inc = True
            if (prev_state != self.current_state and prev_state != 0):
                self.next_h = self.h_thr-1


        print("First time:", "l_thr:", self.l_thr, "h_thr:", self.h_thr, sep=" ")

        # Check if the state has gone from sleeping to awake or vice versa
        if (prev_state == 0 and self.current_state == 1 
            or prev_state == 1 and self.current_state == 0
            or self.h_thr == 1):
            return self.write_out(self.current_state, 1)
        else:
            return self.write_out(self.current_state, 0)

    ##  Categorise the input data. State machine to increase the phases
    #   @param self The object pointer.
    #   @param data 3 element array containing x,y,z accelerations
    #   @param mic Microphone reading in dB
    def inc_sleep_state(self, data, mic):
        # Used to count if x, y, z are lower than threshold
        inc_count = 0

        # Microphone data determines if the user has gone from awake to sleep phase 1
        if(mic < self.mic_threshold[0] and self.current_state == 0):
            #increment state by setting to 3
            inc_count = 3
        else:
            # Iterate through data array, checking if each direction is below threshold
            for i in range(len(data)):
                if     ((math.fabs(data[i]) < self.stage_threshold[0] and self.current_state == self.max_depth - 4)
                    or (math.fabs(data[i]) < self.stage_threshold[1] and self.current_state == self.max_depth - 3)
                    or (math.fabs(data[i]) < self.stage_threshold[2] and self.current_state == self.max_depth - 2)
                    or (math.fabs(data[i]) < self.stage_threshold[3] and self.current_state == self.max_depth - 1)):
                    inc_count = inc_count + 1 #Increment if x, y or z lower than threshhold
        
        # If all 3 directions are below the threshold, increment state
        if(inc_count == 3):
            if self.counter >= self.rep_threshold: 
               self.current_state = self.current_state + 1
               self.counter = 0
               return True
            else:
               self.counter = self.counter + 1
               return False
        else:
            return False
    
    ## State machine to decrease the phases.
    # Differes from increment. If any of the directions
    # are above the threshold, then decrease the phase.
    def dec_sleep_state(self, x, mic):
        if    ((mic > self.mic_threshold[1] and self.current_state == self.max_depth - 4)
           or (x > self.stage_threshold[0] and self.current_state == self.max_depth - 3)
           or (x > self.stage_threshold[1] and self.current_state == self.max_depth - 2)
           or (x > self.stage_threshold[2] and self.current_state == self.max_depth - 1)
           or (x > self.stage_threshold[3] and self.current_state == self.max_depth)):
            if self.counter >= self.rep_threshold: 
                self.current_state = self.current_state - 1
                self.counter = 0
                return True
            else:
                self.counter = self.counter + 1
                return False
        else:
            return False
    
    ## Send the phase in Json format
    def write_out(self, p, st):
        return {'phase': p, 'sleeptoggle': st}



# """ JSON - to send
# Sleep phase
# Bool sleep_toggle
# 
# {1, 2, 3, 4, 1, 1, 2, 2, 2, 3, 4, 4, 3, 2, 2, 1, 1, 1, 2, 3, 3, 3, 4, 1, 1, 1, 1, 1}
# {0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0}
# """
#
#http://www.centerforsoundsleep.com/sleep-disorders/stages-of-sleep/
#https://www.tuck.com/stages/
#https://blog.health.nokia.com/blog/2015/03/17/the-4-different-stages-of-sleep/
#https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grovepi.py
