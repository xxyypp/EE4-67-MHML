"""
Use the sleep cycle data to analyse sleep
"""

class AnalyseSleep:

    ######## Global variables ##########
    current_state = 1 # Between 1 and 5 --> 1 = awake and 5 is deepest phase
    stage_threshold = [{0.6, 0.3, 0.15, 0.05}]
    mic_threshold = [10, 11, 12]
    phase = []
    sleepToggle = []
    # Assumes all the data is read and put in an array
    #{2.5, 1.5, 3, 2}
    
    def __init__(self):
        self.current_state = 1


    def categ_sleep(self, data, mic):
        if len(acc_data) == 0:
            raise Exception("No data input given")
        
        inc = True
        l_thr = 1
        h_thr = 5
        for x in data:
            prev_state = self.current_state
            # Change the threshold and determine whether to increment or decremeent 
            if (self.current_state > h_thr):
               inc = False
               h_thr--
            elif self.current_state == l_thr:
                	inc = True
            # Increment or Decrement
            if inc == True:
                for i in range(len(x)):
                    self.inc_sleep_state(self.absol(x[i]))
            else:
                for i in range(len(x)):
                    self.dec_sleep_state(self.absol(x[i]))
            # Check if the state has gone from sleeping to awake or vice versa
            # if prev_state == 0 and self.current_state == 1
              # or prev_state == 1 and self.current_state == 0:
                  # self.write_out(self.current_state, 1)
            # else:
                # self.write_out(self.current_state, 0)
    
    
    def absol(self, x):
        if x < 0:
            return -x
        else:
            return x
    # Categorise the input data
    # def inc_sleep_state(self, x):
    #     if   (x < self.stage_threshold[0] and self.current_state == 1)
    #        or (x < self.stage_threshold[1] and self.current_state == 2)
    #        or (x < self.stage_threshold[2] and self.current_state == 3)
    #        or (x < self.stage_threshold[3] and self.current_state == 4)
    #        :
    #         self.current_state+=1
                
    
    # def dec_sleep_state(self, x):
    #     if   (x > self.stage_threshold[0] and self.current_state == 1)
    #        or (x > self.stage_threshold[1] and self.current_state == 2)
    #        or (x > self.stage_threshold[2] and self.current_state == 3)
    #        or (x > self.stage_threshold[3] and self.current_state == 4)
    #        :
    #         self.current_state-=1
    
    
    # def write_out(self, p, st):
        # self.phase.append(p)
        # self.sleepToggle.append(st)
        # return {'phase:': p, 'sleeptoggle': st}




""" JSON - to send
Sleep phase
Bool sleep_toggle

{1, 2, 3, 4, 1, 1, 2, 2, 2, 3, 4, 4, 3, 2, 2, 1, 1, 1, 2, 3, 3, 3, 4, 1, 1, 1, 1, 1}
{0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0}
"""


'''filepath = "test.csv"
def read_file():
	with open(filepath) as f:
		array = []
		for line in f:
			array.append([int(x) for x in line.split()])

	return array
'''
#http://www.centerforsoundsleep.com/sleep-disorders/stages-of-sleep/
#https://www.tuck.com/stages/
#https://blog.health.nokia.com/blog/2015/03/17/the-4-different-stages-of-sleep/
#https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grovepi.py
