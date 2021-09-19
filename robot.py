
import time
import maestro

"""
This section includes Constants that are used for the robot
"""

M1 = 0  # gripper motor 1
M2 = 1  # gripper motor 2
M3 = 2  # gripper motor 3
M4 = 3  # gripper motor 4

S1 = 8  # slider motor 1
S2 = 9  # slider motor 1
S3 = 10  # slider motor 1
S4 = 11  # slider motor 1

M1_INIT = 3968  # gripper motor 1 default position
M2_INIT = 4200  # gripper motor 2 default position
M3_INIT = 4200  # gripper motor 3 default position
M4_INIT = 3968  # gripper motor 4 default position

M1_90 = 6600    # gripper motor 1 clockwise-rotated position
M2_90 = 6800    # gripper motor 2 clockwise-rotated position
M3_90 = 6900    # gripper motor 3 clockwise-rotated position
M4_90 = 6900    # gripper motor 4 clockwise-rotated position

S1_INIT = 3900  # slider motor 1 closed position
S2_INIT = 4600  # slider motor 2 closed position
S3_INIT = 4400  # slider motor 3 closed position
S4_INIT = 3900  # slider motor 4 closed position

S1_END = 9000  # slider motor 1 open position
S2_END = 9000  # slider motor 2 open position
S3_END = 9000  # slider motor 3 open position
S4_END = 9000  # slider motor 4 open position

NUM_MOTORS = 8

# arrays that hold all of the previous data in order for loop accessing

ACCEL_SLOW = 30     # self.servo acceleration rate slow
ACCEL_NORMAL = 50   # self.servo acceleration rate normal

SLEEP = 0.4  # sleep value used inbetween different motor movements
SHORT = 0.1
MEDIUM = 0.2

class Robot:
    
    MOTORS = [M1, M2, M3, M4, S1, S2, S3, S4]
    DEFAULT_POSITIONS = [M1_INIT, M2_INIT, M3_INIT,
                        M4_INIT, S1_INIT, S2_INIT, S3_INIT, S4_INIT]
    ACTIVATED_POSITIONS = [M1_90, M2_90, M3_90,
                        M4_90, S1_END, S2_END, S3_END, S4_END]
    
    def __init__(self):
        self.servo = maestro.Controller('/dev/ttyAMA0')
        pass
    
    def resetToDefault(self):
        print("Reseting to default positions")
        self.servo.setAccel(M1, ACCEL_NORMAL)
        self.servo.setAccel(S1, ACCEL_NORMAL)
        self.servo.setTarget(M1, M1_INIT)
        self.servo.setTarget(S1, S1_INIT)
        time.sleep(1)

        self.servo.setAccel(M2, ACCEL_NORMAL)
        self.servo.setAccel(S2, ACCEL_NORMAL)
        self.servo.setTarget(M2, M2_INIT)
        self.servo.setTarget(S2, S2_INIT)
        time.sleep(1)

        self.servo.setAccel(M3, ACCEL_NORMAL)
        self.servo.setAccel(S3, ACCEL_NORMAL)
        self.servo.setTarget(M3, M3_INIT)
        self.servo.setTarget(S3, S3_INIT)
        time.sleep(1)

        self.servo.setAccel(M4, ACCEL_NORMAL)
        self.servo.setAccel(S4, ACCEL_NORMAL)
        self.servo.setTarget(M4, M4_INIT)
        self.servo.setTarget(S4, S4_INIT)
        time.sleep(1)

    def setToClosed(self):
        print("Setting to clsed position")

        step = 5

        increment1 = int((S1_END - S1_INIT)/step)
        increment2 = int((S2_END - S2_INIT)/step)
        increment3 = int((S3_END - S3_INIT)/step)
        increment4 = int((S4_END - S4_INIT)/step)

        a1 = int(S1_END)
        a2 = int(S2_END)
        a3 = int(S3_END)
        a4 = int(S4_END)

        self.servo.setTarget(M1, M1_INIT)
        self.servo.setTarget(M2, M2_INIT)
        self.servo.setTarget(M3, M3_INIT)
        self.servo.setTarget(M4, M4_INIT)

        for i in range(step):

            self.servo.setTarget(S2, a2)
            self.servo.setTarget(S4, a4)

            a2 -= increment2
            a4 -= increment4

            if i == step-1:
                self.servo.setTarget(S2, S2_INIT)
                self.servo.setTarget(S4, S4_INIT)

        time.sleep(1)

        for i in range(step):

            self.servo.setTarget(S1, a1)
            self.servo.setTarget(S3, a3)

            a1 -= increment1
            a3 -= increment3

            if i == step-1:
                self.servo.setTarget(S1, S1_INIT)
                self.servo.setTarget(S3, S3_INIT)

        print(a1)
        print(a2)
        print(a3)
        print(a4)

    def setToOpen(self):
        print("Setting to open position")

        step = 5

        increment1 = int((S1_END - S1_INIT)/step)
        increment2 = int((S2_END - S2_INIT)/step)
        increment3 = int((S3_END - S3_INIT)/step)
        increment4 = int((S4_END - S4_INIT)/step)

        a1 = int(S1_INIT)
        a2 = int(S2_INIT)
        a3 = int(S3_INIT)
        a4 = int(S4_INIT)

        self.servo.setAccel(M1, ACCEL_SLOW)
        self.servo.setAccel(S1, ACCEL_SLOW)
        self.servo.setAccel(M2, ACCEL_SLOW)
        self.servo.setAccel(S2, ACCEL_SLOW)
        self.servo.setAccel(M3, ACCEL_SLOW)
        self.servo.setAccel(S3, ACCEL_SLOW)
        self.servo.setAccel(M4, ACCEL_SLOW)
        self.servo.setAccel(S4, ACCEL_SLOW)

        for i in range(step):
            self.servo.setTarget(S1, a1)
            self.servo.setTarget(S2, a2)
            self.servo.setTarget(S3, a3)
            self.servo.setTarget(S4, a4)

            a1 += increment1
            a2 += increment2
            a3 += increment3
            a4 += increment4

        self.servo.setTarget(M1, M1_INIT)
        self.servo.setTarget(M2, M2_INIT)
        self.servo.setTarget(M3, M3_INIT)
        self.servo.setTarget(M4, M4_INIT)

        print(a1)
        print(a2)
        print(a3)
        print(a4)


    def tightenVertical(self):
        self.servo.setTarget(S1, S1_INIT-1000)
        self.servo.setTarget(S3, S3_INIT-1000)


    def loosenVertical(self):
        self.servo.setTarget(S1, S1_INIT)
        self.servo.setTarget(S3, S3_INIT)


    def tightenHorizontal(self):
        self.servo.setTarget(S2, S2_INIT-1000)
        self.servo.setTarget(S4, S4_INIT-1000)

    def loosenHorizontal(self):
        self.servo.setTarget(S2, S2_INIT)
        self.servo.setTarget(S4, S4_INIT)

    def acceptCube(self):
        time.sleep(2)
        setToOpen()
        time.sleep(SLEEP)
        setToClosed()
        time.sleep(SLEEP)


    # sets the robot to the default open position
    def defaultOpen(self):
        print("Setting robot to default open position")

        # for simultaneous motor movoment, multiple motors take turns incrementing small amounts
        # step determines the number of turns each motor takes (i.e number of iterations of the loop)
        step = 5

        # increment values for each motor, used in the loop
        increment1 = int((S1_END - S1_INIT)/step)
        increment2 = int((S2_END - S2_INIT)/step)
        increment3 = int((S3_END - S3_INIT)/step)
        increment4 = int((S4_END - S4_INIT)/step)

        # target position at the end of each iteration
        position1 = int(S1_INIT)
        position2 = int(S2_INIT)
        position3 = int(S3_INIT)
        position4 = int(S4_INIT)

        # set each motor to a slow acceleration
        self.servo.setAccel(M1, ACCEL_SLOW)
        self.servo.setAccel(S1, ACCEL_SLOW)
        self.servo.setAccel(M2, ACCEL_SLOW)
        self.servo.setAccel(S2, ACCEL_SLOW)
        self.servo.setAccel(M3, ACCEL_SLOW)
        self.servo.setAccel(S3, ACCEL_SLOW)
        self.servo.setAccel(M4, ACCEL_SLOW)
        self.servo.setAccel(S4, ACCEL_SLOW)

        # move all sliders out symultanesously
        for i in range(step):
            if i < step-1:
                self.servo.setTarget(S1, position1)
                self.servo.setTarget(S2, position2)
                self.servo.setTarget(S3, position3)
                self.servo.setTarget(S4, position4)

                position1 += increment1
                position2 += increment2
                position3 += increment3
                position4 += increment4
            else: # if i == step-1, or the last iteration
                self.servo.setTarget(S1, S1_END)
                self.servo.setTarget(S2, S2_END)
                self.servo.setTarget(S3, S3_END)
                self.servo.setTarget(S4, S4_END)

        time.sleep(SLEEP)

        # move gripppers to default positions
        self.servo.setTarget(M1, M1_INIT)
        self.servo.setTarget(M2, M2_INIT)
        self.servo.setTarget(M3, M3_INIT)
        self.servo.setTarget(M4, M4_INIT)

    # sets the robot to the default closed position
    def defaultClose(self):
        print("Setting robot to default closed position")

        time.sleep(SLEEP)

        # for simultaneous motor movoment, multiple motors take turns incrementing small amounts
        # step determines the number of turns each motor takes (i.e number of iterations of the loop)
        step = 5

        # increment values for each motor, used in the loop
        increment1 = int((S1_END - S1_INIT)/step)
        increment2 = int((S2_END - S2_INIT)/step)
        increment3 = int((S3_END - S3_INIT)/step)
        increment4 = int((S4_END - S4_INIT)/step)

        # target position at the end of each iteration
        position1 = int(S1_END)
        position2 = int(S2_END)
        position3 = int(S3_END)
        position4 = int(S4_END)

        self.servo.setTarget(M1, M1_INIT)
        self.servo.setTarget(M2, M2_INIT)
        self.servo.setTarget(M3, M3_INIT)
        self.servo.setTarget(M4, M4_INIT)

        for i in range(step):

            self.servo.setTarget(S2, position2)
            self.servo.setTarget(S4, position4)

            position2 -= increment2
            position4 -= increment4

            if i == step-1:
                self.servo.setTarget(S2, S2_INIT)
                self.servo.setTarget(S4, S4_INIT)

            time.sleep(SHORT)
        
        time.sleep(MEDIUM)

        for i in range(step):

            self.servo.setTarget(S1, position1)
            self.servo.setTarget(S3, position3)

            position1 -= increment1
            position3 -= increment3

            if i == step-1:
                self.servo.setTarget(S1, S1_INIT)
                self.servo.setTarget(S3, S3_INIT)
            
            time.sleep(SHORT)

    def acceptCube(self):
        self.defaultOpen()
        time.sleep(SLEEP)
        self.defaultClose()
        time.sleep(SHORT)


    def inDefaultPosition(self, motor):
        if motor == M1:
            if self.servo.getPosition(motor) == M1_INIT:
                return True
        elif motor == M2:
            if self.servo.getPosition(motor) == M2_INIT:
                return True
        elif motor == M3:
            if self.servo.getPosition(motor) == M3_INIT:
                return True
        elif motor == M4:
            if self.servo.getPosition(motor) == M4_INIT:
                return True
        elif motor == S1:
            if self.servo.getPosition(motor) == S1_INIT:
                return True
        elif motor == S2:
            if self.servo.getPosition(motor) == S2_INIT:
                return True
        elif motor == S3:
            if self.servo.getPosition(motor) == S3_INIT:
                return True
        elif motor == S4:
            if self.servo.getPosition(motor) == S4_INIT:
                return True
        else:
            print("   provided wrong input in isInDefaultPosition():robot.py 117")
            print("   argument: " + str(motor))

        return False

    def setMotorOff(self, motor):
        if not self.inDefaultPosition(motor):
            for i in range(len(MOTORS)):
                if MOTORS[i] == motor: 
                    self.servo.setTarget(MOTORS[i], DEFAULT_POSITIONS[i])
                    break
                

    def setMotorOn(self, motor):
        if not self.inDefaultPosition(motor):
            for i in range(len(MOTORS)):
                if MOTORS[i] == motor:
                    self.servo.setTarget(MOTORS[i], ACTIVATED_POSITIONS[i])
                    break

    def setMotorsAcceleration(self, accel, list=MOTORS):
        for m in list:
            self.servo.setAccel(m, accel)
            
    def prepare_UD(self, tighten:bool):
        """Prepares the U and D motors for a L/R rotation
        by either tightening its grip or comletely letting go
        
        Parameters
        ----------
        tighten : bool
            determines whether to tighten or to loosen
        """
        pass
        
    def prepare_LR(self, tighten:bool):
        """Prepares the L and R motors for a U/D rotation
        by either tightening its grip or comletely letting go
        
        Parameters
        ----------
        tighten : bool
            determines whether to tighten or to loosen
        """
        pass
            
    def translate_solution(self, solution:str,rotation_command:str):
        """Optimizes the amount of full cube rotations 
        when the robot needs to make in response to an F/B cube movement.
        It specifically replaces the coming commands with their rotated 
        counter-parts as if the cube rotation never happened
        
        Parameters
        ----------
        solution : str
            the rest of the solution string for the cube
        rotation_command : str
            the rotation command that just occured, helps the function
            know which sides should be translated to which sides
            Ex: if the rotation was a "y", then all of the "B" rotations
                will now be translated as a "L" rotation
                
        Returns
        ----------
        str
            the translated solution
        """
        pass
            

    def rotate_cube(self, rotation_command: str, prime: bool):
        """Rotates the entire cube
        
        rotation_command examples: "y", "x'", "z"
        """
        pass
            
    def rotate_side(self, side_command:str, prime:bool):
        """Rotates a specified side of the cube from the
        passed in side_command (Ex: "R", "F'", "D2")
        
        Parameters
        ----------
        side_command : str
            the command that needs to be performed"""
        pass

    def parse_solution(self, algorithm:str):
        """Takes in a solution for the cube, parses it, 
        and rotates the motors to solve the physical
        Rubik's Cube
        
        Parameters
        ----------
        algorithm : str
            the set of movements from cube.py that will solve the cube
        """
        algorithm = "R U R' R U R' U R U R' R U' R' U' R U R'"
        movements = algorithm.split(" ")
        
        for movement in movements:
            
            if movement[0].lower():
                if len(movement) == 1:
                    self.rotate_cube(movement, False)
                else:
                    if movement[1] == "'":
                        self.rotate_cube(movement, True)
                    elif movement[1] == "2":
                        for i in range(2):
                            self.rotate_cube(movement, False)
            else:
                if len(movement) == 1:
                    self.rotate_side(movement, False)
                else:
                    if movement[1] == "'":
                        self.rotate_side(movement, True)
                    elif movement[1] == "2":
                        for i in range(2):
                            self.rotate_side(movement, False)
        


