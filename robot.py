
import time

#from serial.serialposix import PlatformSpecificBase
import maestro
from cameraSensor import CameraSensor
import numpy as np

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
G2_INIT = 6700  # gripper motor 2 default position
G3_INIT = 4200  # gripper motor 3 default position
G4_INIT = 6800  # gripper motor 4 default position

G1_END = 6600   # gripper motor 1 clockwise-rotated position
G2_END = 4200   # gripper motor 2 clockwise-rotated position
G3_END = 6850   # gripper motor 3 clockwise-rotated position
G4_END = 3968   # gripper motor 4 clockwise-rotated position

S1_INIT = 4300  # slider motor 1 closed position
S2_INIT = 4300  # slider motor 2 closed position
S3_INIT = 4000  # slider motor 3 closed position
S4_INIT = 4300  # slider motor 4 closed position

S1_END = 7000  # slider motor 1 open position
S2_END = 9000  # slider motor 2 open position
S3_END = 9000  # slider motor 3 open position
S4_END = 9000  # slider motor 4 open position

NUM_MOTORS = 8

# arrays that hold all of the previous data in order for loop accessing

ACCEL_SLOW = 30     # self.servo acceleration rate slow
ACCEL_NORMAL = 50   # self.servo acceleration rate normal
ACCEL_FAST = 70     # self.servo acceleration rate fast

SLEEP = 0.6  # sleep value used inbetween different motor movements
SHORT = 0.3
MEDIUM = 0.4

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
            self.name = self.type + str((id % 4) + 1)
        else:
            self.type = "S"
            self.name = self.type + str((id % 4) + 1)
        
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
    
    g1 = grippers[0]
    g2 = grippers[1]
    g3 = grippers[2]
    g4 = grippers[3]
    
    s1 = sliders[0]
    s2 = sliders[1]
    s3 = sliders[2]
    s4 = sliders[3]
    
    motors = grippers.copy() + sliders.copy()
    
    def __init__(self):
        self.servo = maestro.Controller('/dev/ttyAMA0')
        # set each motor to a slow acceleration
        for motor in self.motors:
            self.setAcceleration(motor, ACCEL_FAST)
            
        self.translation = {"L": "L", "R": "R", "B": "B",
                            "U": "U", "D": "D", "F": "F",
                            "x": "x", "y": "y", "z": "z"}
        
        self.camSensor = CameraSensor()
            
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
            returnString += m.name + " "
            returnString += str(self.getPosition(m))
            returnString += "\n"
            
        return returnString
            
    def setAcceleration(self, motor:Motor, value):
        self.servo.setAccel(motor.id, value)
        
    def setPosition(self, motor:Motor, position, pause=True):
        self.servo.setTarget(motor.id, position)
        if pause:
            time.sleep(MEDIUM)
            
    def crashCheck(self, slider:Motor):
        sIndex = self.sliders.index(slider)
        sGripper = self.grippers[sIndex]
        g1 = self.grippers[(sIndex - 1) % 4]
        g2 = self.grippers[(sIndex + 1) % 4]
        gBad = (self.getPosition(sGripper) == sGripper.end)
        
        if gBad:
            if self.getPosition(g1) == g1.end:
                print(f"Saving crash of g1:{g1}")
                self.moveGripper(g1, g1.init)
            if self.getPosition(g2) == g2.end:
                print(f"Saving crash of g2:{g2}")
                self.moveGripper(g2, g2.init)
            
    def moveSlider(self, motor:Motor, position, pause=True, save3=True, crashCheck=True):
        
        if self.getPosition(motor) == position:
            return
        
        if position == motor.init and crashCheck:
            self.crashCheck(motor)
            
        if motor.id != self.s3.id:
            save3 = False

        if save3:
            self.tightenHorizontal(True)
            
        self.setPosition(motor, position, pause)
            
        if save3:
            self.resetHorizontal(crashCheck=False)
            
    def moveGripper(self, motor:Motor, position, pause=True, interrupt=False):
        if motor not in self.grippers:
            raise ValueError(f"{motor} is a slider passed into setGripperNoInterrupt")
        
        if self.getPosition(motor) == position:
            return
        
        if interrupt:
            self.setPosition(motor, position, pause)
        else:
            s = self.sliders[self.grippers.index(motor)]
            self.moveSlider(s, s.end, True)
            self.setPosition(motor, position, True)
            self.moveSlider(s, s.init, True)
            self.resetHorizontal()
        
    def getPosition(self, motor:Motor):
        return self.servo.getPosition(motor.id)
    
    def inDefault(self, motor:Motor):
        current = self.getPosition(motor)
        desired = motor.init
        #print(f"{motor.name} {current}-{desired}={abs(current - desired)}")
        return abs(current - desired) < 300

    # sets the robot to the default open position
    def defaultOpen(self):
        print("\nSetting robot to default open position")

        self.openSliders()
        motors = [self.g1, self.g2, self.g3, self.g4]
        for g in motors:
            self.moveGripper(g, g.init, False, interrupt=True)
        time.sleep(SHORT)

    # sets the robot to the default closed position
    def defaultClose(self):
        print("\nSetting robot to default closed position")

        motors = [self.g1, self.g2, self.g3, self.g4]
        for i, g in enumerate(motors):
            if not self.inDefault(g):
                self.moveGripper(g, g.init, False, interrupt=False)
                time.sleep(SHORT)
        print("Grippers good")
        self.closeSliders(save3=False)
        self.resetHorizontal()
        time.sleep(SHORT)

    def acceptCube(self):
        self.defaultOpen()
        input("Ready?")
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
    
    def tightenHorizontal(self, extra=False):
        amount = 100
        if extra:
            amount += 100
        self.setPosition(self.s2, self.s2.init, False) # -amount
        self.setPosition(self.s4, self.s4.init, True) # -amount
        
    def resetHorizontal(self, crashCheck=True):
        self.moveSlider(self.s2, self.s2.init, False, crashCheck=crashCheck)
        self.moveSlider(self.s4, self.s4.init, True, crashCheck=crashCheck)
        
    def openHorizontal(self):
        self.moveSlider(self.s2, self.s2.end, False)
        self.moveSlider(self.s4, self.s4.end, True)
        
    def resetVertical(self):
        self.moveSlider(self.s1, self.s1.init, False)
        self.moveSlider(self.s3, self.s3.init, True)
        
    def openVertical(self):
        self.moveSlider(self.s1, self.s1.end, False)
        self.moveSlider(self.s3, self.s3.end, True)
        
    def openSliders(self):
        self.moveSlider(self.s1, self.s1.end, False, crashCheck=False)
        self.moveSlider(self.s2, self.s2.end, False, crashCheck=False)
        self.moveSlider(self.s3, self.s3.end, False, crashCheck=False, save3=False)
        self.moveSlider(self.s4, self.s4.end, crashCheck=False)

    def closeSliders(self, save3=True):
        self.moveSlider(self.s1, self.s1.init, False)
        self.moveSlider(self.s3, self.s3.init, True, save3)
        self.moveSlider(self.s2, self.s2.init, False)
        self.moveSlider(self.s4, self.s4.init, True)
        
            
    def prepareVertical(self, extra=False):
        """Prepares the U and D motors for a L/R rotation
        by maving the U and D motors into the initial position
        """
        
        gs = [self.g3, self.g1]
        ss = [self.s3, self.s1]
        for i in range(len(gs)):
            g = gs[i]
            if not self.inDefault(g):
                self.tightenHorizontal(extra)
                self.moveGripper(g, g.init)
                self.resetHorizontal()
        for s in ss:
            self.moveSlider(s, s.init, False)
        time.sleep(SHORT)
        
    def prepareHorizontal(self, extra=False):
        """Prepares the L and R motors for a U/D rotation
        by maving the L and R motors into the initial position
        """
        gs = [self.g2, self.g4]
        ss = [self.s2, self.s4]
        for i in range(len(gs)):
            g = gs[i]
            if not self.inDefault(g):
                self.moveGripper(g, g.init)
        for s in ss:
            self.moveSlider(s,s.init, False)
        time.sleep(SHORT)
                
    def updateTranslation(self, rotation_command:str, prime:bool):
        """Optimizes the amount of full cube rotations 
        when the robot needs to make in response to an F/B cube movement.
        It specifically changes the translation of each future command.
        """
        patterns = {"y":["F", "R", "B", "L"],
                    "x":["F", "U", "B", "D"],
                    "z":["L", "U", "R", "D"]}
        
        oldTranslation = self.translation.copy()
        
        increment = 1
        if prime:
            increment = -1
        pattern = patterns[rotation_command]
        for i in range(len(pattern)):
            curr = pattern[i]
            trans = oldTranslation[pattern[(i+increment)%4]]
            self.translation[curr] = trans
            
        #print(self.translation)
        
    def rotate_z(self, prime):
        self.rotate_y(False)
        self.rotate_x(prime)
        self.rotate_y(True)
    
    def rotate_x(self, prime):
        if not prime:
            # prepare left and right gripper for turn
            self.moveGripper(self.g2, self.g2.end)
            self.moveGripper(self.g4, self.g4.init)
            self.openVertical()
            # do the simultaneous turn
            time.sleep(0.2)
            self.setPosition(self.g2, self.g2.init, pause=False)
            self.setPosition(self.g4, self.g4.end, pause=True)
            #self.moveGripper(self.g2, self.g2.init, False, True)
            #self.moveGripper(self.g4, self.g4.end, True, True)
        else:
            # prepare left and right gripper for turn
            self.moveGripper(self.g2, self.g2.init)
            self.moveGripper(self.g4, self.g4.end)
            self.openVertical()
            # do the simultaneous turn
            time.sleep(0.2)
            self.setPosition(self.g2, self.g2.end, pause=False)
            self.setPosition(self.g4, self.g4.init, pause=True)
            #self.moveGripper(self.g2, self.g2.end, False, True)
            #self.moveGripper(self.g4, self.g4.init, True, True)
        self.resetVertical()
        self.defaultClose()
        
    def rotate_y(self, prime):
        if prime:
            # position top and bottom grippers
            self.moveGripper(self.g3,self.g3.init)
            self.moveGripper(self.g1, self.g1.end)
            self.moveSlider(self.s1, self.s1.init)
            self.openHorizontal()
            # do the simultaneous turn of top and bottom
            time.sleep(0.2)
            self.setPosition(self.g3, self.g3.end, pause=False)
            self.setPosition(self.g1, self.g1.init, pause=True)
            #self.moveGripper(self.g3, self.g3.end, False, True)
            #self.moveGripper(self.g1, self.g1.init, True, True)
        else:
            # position top and bottom grippers
            self.moveGripper(self.g3, self.g3.end)
            self.moveGripper(self.g1, self.g1.init)
            self.moveSlider(self.s1, self.s1.init)
            self.openHorizontal()
            # do the simultaneous turn of top and bottom
            time.sleep(0.2)
            self.setPosition(self.g3, self.g3.init, pause=False)
            self.setPosition(self.g1, self.g1.end, pause=True )
            #self.moveGripper(self.g3, self.g3.init, False, True)
            #self.moveGripper(self.g1, self.g1.end, True, True)
        self.resetHorizontal()
        self.defaultClose()
        

    def rotate_cube(self, rotation_command: str, prime: bool, double=False):
        """Rotates the entire cube
        
        rotation_command examples: "y", "x'", "z"
        """
        if rotation_command == "x":
            if double:
                self.prepareVertical()
                self.rotate_x(prime)
            self.prepareVertical()
            self.rotate_x(prime)
        elif rotation_command == "y":
            if double:
                self.prepareHorizontal()
                self.rotate_y(prime)
            self.prepareHorizontal()
            self.rotate_y(prime)
        elif rotation_command == "z":
            if double:
                self.rotate_z(prime)
            self.rotate_z(prime)
        else:
            raise ValueError(
                "rotate_cube command not valid {} prime({})".format(rotation_command, prime))
    
    def rotate_L(self, prime):
        if prime:
            self.moveGripper(self.g4, self.g4.init)
            self.moveSlider(self.s4, self.s4.init)
            self.moveGripper(self.g4, self.g4.end, interrupt=True)
        else:
            self.moveGripper(self.g4, self.g4.end)
            self.moveSlider(self.s4, self.s4.init)
            self.moveGripper(self.g4, self.g4.init, interrupt=True)
                
    def rotate_R(self, prime):
        if prime:
            self.moveGripper(self.g2, self.g2.init)
            self.moveSlider(self.s2, self.s2.init)
            self.moveGripper(self.g2, self.g2.end, interrupt=True)
        else:
            self.moveGripper(self.g2, self.g2.end)
            self.moveSlider(self.s2, self.s2.init)
            self.moveGripper(self.g2, self.g2.init, interrupt=True)
                
    def rotate_U(self, prime):
        if not prime:
            self.moveGripper(self.g1, self.g1.init)
            self.moveSlider(self.s1, self.s1.init)
            self.moveGripper(self.g1, self.g1.end, interrupt=True)
        else:
            self.moveGripper(self.g1, self.g1.end)
            self.moveSlider(self.s1, self.s1.init)
            self.moveGripper(self.g1, self.g1.init, interrupt=True)
                
    def rotate_D(self, prime):
        if not prime:
            self.moveGripper(self.g3, self.g3.init)
            self.moveSlider(self.s3, self.s3.init)
            self.moveGripper(self.g3, self.g3.end, interrupt=True)
        else:
            self.moveGripper(self.g3, self.g3.end)
            self.moveSlider(self.s3, self.s3.init)
            self.moveGripper(self.g3, self.g3.init, interrupt=True)
            
    def rotate_F(self, prime, double=False):
        self.rotate_cube("y", True)
        if double:
            self.rotate_side("R", prime)
        self.rotate_side("R", prime)
        self.updateTranslation("y",False)
    
    def rotate_B(self, prime, double=False):
        self.rotate_cube("y", True)
        if double:
            self.rotate_side("L", prime)
        self.rotate_side("L", prime)
        self.updateTranslation("y", False)
            
    def rotate_side(self, side_command:str, prime:bool, double=False):
        """Rotates a specified side of the cube from the
        passed in side_command (Ex: "R", "F'", "D2")
        
        Parameters
        ----------
        side_command : str
            the command that needs to be performed
        """
        #print("rotate_side: " + side_command)
        if side_command == "F":
            self.rotate_F(prime, double)
        elif side_command == "B":
            self.rotate_B(prime, double)
        elif side_command == "L":
            self.prepareVertical()
            if double:
                self.rotate_L(prime)
            self.rotate_L(prime)
        elif side_command == "R":
            self.prepareVertical()
            if double:
                self.rotate_R(prime)
            self.rotate_R(prime)
        elif side_command == "U":
            self.prepareHorizontal()
            if double:
                self.rotate_U(prime)
            self.rotate_U(prime)
        elif side_command == "D":
            self.prepareHorizontal(extra=True)
            if double:
                self.rotate_D(prime)
            self.rotate_D(prime)
            self.resetHorizontal()
        else:
            raise ValueError(
                "rotate_side command not valid {} prime({})".format(side_command, prime))

    def parse_solution(self, algorithm:str, close=True):
        """Takes in a solution for the cube, parses it, 
        and rotates the motors to solve the physical
        Rubik's Cube
        
        Parameters
        ----------
        algorithm : str
            the set of movements from cube.py that will solve the cube
        """
        if close:
            self.defaultClose()
        #algorithm = "R U R' R U R' U R U R' R U' R' U' R U R'"
        movements = algorithm.split()
        print(movements)
        
        for movement in movements:
            #print("parse_solution: " + movement, end=" : ")
            movement = self.translation[movement[0]] + movement[1:]
            print(movement, end=" ")
            if movement[0].islower():
                if len(movement) == 1:
                    # x y z
                    self.rotate_cube(movement[0], False)
                else:
                    if movement[1] == "'":
                        # x' y' z'
                        self.rotate_cube(movement[0], True)
                    elif movement[1] == "2":
                        # x2 y2 z2
                        self.rotate_cube(movement[0], False, double=True)
                            
            else:
                if len(movement) == 1:
                    # any normal side movement
                    self.rotate_side(movement[0], False)
                else:
                    if movement[1] == "'":
                        # any prime side movement
                        self.rotate_side(movement[0], True)
                    elif movement[1] == "2":
                        # any side double movement
                        self.rotate_side(movement[0], False, double=True)
                        
    def picturePosition(self):
        self.moveGripper(self.g3, self.g3.end, pause=True, interrupt=False)
        self.moveSlider(self.s3, self.s3.init, True)
        self.moveSlider(self.s1, self.s1.end, False)
        self.moveSlider(self.s2, self.s2.end, False)
        self.moveSlider(self.s4, self.s4.end, False)
        
    def referencePicture(self):
        self.camSensor.referencePicture()
        
    def takePicture(self, fileName):
        self.camSensor.takePicture(fileName)
        
    def takePictures(self):
        #self.picturePosition()
        movements = ["y", "y", "x", "y", "y", "UN"]
        # U y L y D x F y R y B
        sides = ["U", "L", "D", "F", "R", "B"]
        for i, movement in enumerate(movements):
            side = sides[i]
            fileName = "./webcam/" + side + ".jpg"
            self.picturePosition()
            #self.camSensor.referencePicture()
            self.camSensor.takePicture(fileName)
            c = False
            if movement == "x":
                c = True
            self.parse_solution(movement, close=c)
            
        self.defaultClose()
            
    def getCubeVals(self):
        sides = ["L", "R", "B", "U", "D", "F"]
        files = [str("./webcam/" + side + ".jpg") for side in sides]
        return self.camSensor.getValues(files)
    
    def redOrangeTest(self):
        file1 = "./webcam/"
        file2 = ".jpg"
        #self.picurePosition()
        for i in range(11):
            redName = file1 + "r" + str(i) + file2
            self.camSensor.takePicture(redName)
            averages = self.camSensor.averages(redName)
            if i == 0:
                reds = np.array([averages[5]])
                oranges = np.array([averages[4]])
                continue
            for i, val in enumerate(averages):
                if i%2==0:
                    reds = np.append(reds, [val], axis=0)
                else:
                    oranges = np.append(oranges, [val], axis=0)
        print(np.average(reds, axis=0))
        print(np.average(oranges, axis=0))


        
                            
        


