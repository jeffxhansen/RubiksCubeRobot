
import time
import maestro

"""
This section includes Constants that are used for the robot
"""

G1 = 0  # gripper motor 1
G2 = 1  # gripper motor 2
G3 = 2  # gripper motor 3
G4 = 3  # gripper motor 4

S1 = 8  # slider motor 1
S2 = 9  # slider motor 1
S3 = 10  # slider motor 1
S4 = 11  # slider motor 1

G1_INIT = 3968  # gripper motor 1 default position
G2_INIT = 4200  # gripper motor 2 default position
G3_INIT = 4200  # gripper motor 3 default position
G4_INIT = 3968  # gripper motor 4 default position

G1_END = 6600    # gripper motor 1 clockwise-rotated position
G2_END = 6800    # gripper motor 2 clockwise-rotated position
G3_END = 6900    # gripper motor 3 clockwise-rotated position
G4_END = 6900    # gripper motor 4 clockwise-rotated position

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

"""
Simple class to represent a motor with properties of 
id, initial position, end position, and type of motor 
("G" for gripper or "S" for slidder)
"""
class Motor:
    def __init__(self, id:int, init:int, end:int):
        self.id = id
        self.init = init
        self.end = end
        self.type = ""
        if id < 4: 
            self.type = "G"
        else:
            self.type = "S"
        self.label = self.type + str(self.id%4+1)
        
    def __str__(self):
        return "{}{}: id({}), init({}), end({})"\
            .format(self.type, self.id % 4+1, self.id, self.init, self.end)
            
    def __repr__(self):
        return "Motor({}, {}, {})"\
            .format(self.id, self.init, self.end, self.type)

class Robot:
    
    grippers = [Motor(G1, G1_INIT, G1_END),
                Motor(G2, G2_INIT, G2_END),
                Motor(G3, G3_INIT, G3_END),
                Motor(G4, G4_INIT, G4_END)]
    
    sliders = [Motor(S1, S1_INIT, S1_END),
               Motor(S2, S2_INIT, S2_END),
               Motor(S3, S3_INIT, S3_END),
               Motor(S4, S4_INIT, S4_END)]
    
    motors = grippers.copy() + sliders.copy()
    
    def __init__(self):
        self.servo = maestro.Controller('/dev/ttyAMA0')
        # set each motor to a slow acceleration
        for motor in self.motors:
            self.setAcceleration(motor, ACCEL_SLOW)
            
    def __str__(self):
        returnString = ""
        
        returnString += "DEFAULTS:\n"
        for m in self.motors:
            returnString += "  "
            returnString += str(m)
            returnString += "\n"
        
        returnString += "\nCURRENT:\n"
        for m in self.motors:
            returnString += "  "
            returnString += m.label + " "
            returnString += str(self.getPosition(m))
            returnString += "\n"
            
        return returnString
            
    def setAcceleration(self, motor:Motor, value):
        self.servo.setAccel(motor.id, value)
        
    def setPosition(self, motor:Motor, position):
        self.servo.setTarget(motor.id, position)
        
    def getPosition(self, motor:Motor):
        return self.servo.getPosition(motor.id)

    def tightenVertical(self):
        self.setPosition(S1, S1_INIT-1000)
        self.setPosition(S3, S3_INIT-1000)

    def loosenVertical(self):
        self.setPosition(S1, S1_INIT)
        self.setPosition(S3, S3_INIT)

    def tightenHorizontal(self):
        self.setPosition(S2, S2_INIT-1000)
        self.setPosition(S4, S4_INIT-1000)

    def loosenHorizontal(self):
        self.setPosition(S2, S2_INIT)
        self.setPosition(S4, S4_INIT)

    # sets the robot to the default open position
    def defaultOpen(self):
        print("Setting robot to default open position")

        STEP = 5

        # lists with the intermediate positions and how much to be incremented in between each
        # intermediate position
        positions = [int(s.end) for s in self.sliders]
        increments = [int(abs(s.init-s.end)/STEP) for s in self.sliders]

        for i in range(STEP):
            if i < STEP-1:
                # set each slider to the next intermediate position
                for j, s in enumerate(self.sliders):
                    self.setPosition(s, positions[j])
                # increment the intermediate positions
                positions = [val + increments[i] for i, val in enumerate(positions)]
                
            # if on the last step, just set to default end position
            else:
                for s in self.sliders:
                    self.setPosition(s, s.end)

        time.sleep(SLEEP)

        # move gripppers to default positions
        for g in self.grippers:
            self.setPosition(g, g.init)

    # sets the robot to the default closed position
    def defaultClose(self):
        print("Setting robot to default closed position")

        time.sleep(SLEEP)

        STEP = 5

        # lists with the intermediate positions and how much to be incremented in between each
        # intermediate position
        positions = [int(s.init) for s in self.sliders]
        increments = [int(abs(s.end-s.init)/STEP) for s in self.sliders]

        # set movtors to default open position
        for g in self.grippers:
            self.setPosition(g, g.init)
        time.sleep(SHORT)

        # first does even motors then odd motors
        for i in range(2):
            # increments each motor STEP even number of times
            for j in range(STEP):
                for k, s in enumerate(self.sliders):
                    if k % 2 != i: # if odd or even motor
                        if j < STEP-1:
                            self.setPosition(s, positions[k])
                            positions[k] -= increments[k]
                        else:
                            self.setPosition(s, s.init)
                        time.sleep(SHORT)

    def acceptCube(self):
        self.defaultOpen()
        time.sleep(SLEEP)
        self.defaultClose()
        time.sleep(SHORT)

    def inDefaultPosition(self, motor):
        
        for m, i in enumerate(self.motors):
            if m == motor:
                if self.servo.getPosition(motor) == self.DEFAULT_POSITIONS[i]:
                    return True
    
        print("   provided wrong input in isInDefaultPosition():robot.py 117")
        print("   argument: " + str(motor))
        return False

    def setMotorOff(self, motor):
        if not self.inDefaultPosition(motor):
            for i in range(len(self.motors)):
                if self.motors[i] == motor:
                    self.setPosition(
                        self.motors[i], self.DEFAULT_POSITIONS[i])
                    break
                

    def setMotorOn(self, motor):
        if not self.inDefaultPosition(motor):
            for i in range(len(self.motors)):
                if self.motors[i] == motor:
                    self.setPosition(
                        self.motors[i], self.ACTIVATED_POSITIONS[i])
                    break

    def setMotorsAcceleration(self, accel, list=motors):
        for m in list:
            self.setAcceleration(m, accel)
            
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
            the command that needs to be performed
        """
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
        


