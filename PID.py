class myPID:
    dt = 0.0
    max = 0.0
    min = 0.0
    kp = 0.0
    ki = 0.0
    kd = 0.0
    err = 0.0
    int = 0.0

    def __init__(self, dt, max, min, kp, ki, kd):
        self.dt = dt
        self.max = max
        self.min = min
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def run(self, set, act):
        error = set - act

        P = self.kp * error

        self.int += error * self.dt
        I = self.ki * self.int

        D = self.kd * (error - self.err) / self.dt

        output = P + I + D

        if (output > self.max):
            output = self.max
        elif (output < self.min):
            output = self.min

        self.error = error
        return output
    
'''
def main() :
  pid = myPID(0.1, 100, -100, 0.1, 0.01, 0.5)
 
  val = 20;
  for i in range(100) :
    inc = pid.run(0, val)
    print('val:','{:7.3f}'.format(val),' inc:','{:7.3f}'.format(inc) )
    val += inc

main()

'''
        
