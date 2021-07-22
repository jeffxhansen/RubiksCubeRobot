# ---KEY---
'''
values order
L 0-7
R 8-15
B 16-23
U 24-31
D 32-39
F 40-47

Unfolded cube value indices
-- -- -- 16 17 18 -- -- --
-- -- -- 23 BB 19 -- -- --
-- -- -- 22 21 20 -- -- --
00 01 02 24 25 26 08 09 10
07 LL 03 31 UU 27 15 RR 11
06 05 04 30 29 28 14 13 12
-- -- -- 40 41 42 -- -- --
-- -- -- 47 FF 43 -- -- --
-- -- -- 46 45 44 -- -- --
-- -- -- 32 33 34 -- -- --
-- -- -- 39 DD 35 -- -- --
-- -- -- 38 37 36 -- -- --
'''

# constants to increase readability
NUM_COLORS = 8
NUM_SIDES = 6

# a cube object that stores the colors on a cube in a list with 48 elements


class Cube:
    
    sides = ("L", "R", "B", "U", "D", "F")
    sideToValue = {"L": 0, "R": 1, "B": 2, "U": 3, "D": 4, "F": 5}
    edges = {"L": [24, 31, 30, 40, 47, 46, 32, 39, 38, 16, 23, 22],
             "R": [28, 27, 26, 20, 19, 18, 36, 35, 34, 44, 43, 42],
             "B": [26, 25, 24, 2, 1, 0, 38, 37, 36, 10, 9, 8],
             "U": [4, 3, 2, 22, 21, 20, 8, 15, 14, 42, 41, 40],
             "D": [0, 7, 6, 46, 45, 44, 12, 11, 10, 18, 17, 16],
             "F": [30, 29, 28, 14, 13, 12, 34, 33, 32, 6, 5, 4]}
    
    def __init__(self):
        self.values = [0, 0, 0, 0, 0, 0, 0, 0,
                       1, 1, 1, 1, 1, 1, 1, 1,
                       2, 2, 2, 2, 2, 2, 2, 2,
                       3, 3, 3, 3, 3, 3, 3, 3,
                       4, 4, 4, 4, 4, 4, 4, 4,
                       5, 5, 5, 5, 5, 5, 5, 5]
        self.colors = {0: "r", 1: "o", 2: "y", 3: "g", 4: "b", 5: "w"}

    def set(self, values, colors):
        self.values = values

        for i in range(NUM_SIDES):
            self.colors[i] = colors[i]

    def chartString(self):
        string = ""
        for i in range(NUM_SIDES):
            side = self.sides[i]
            color = self.colors[i]

            string += f"{side} {color} \t"
            if color == "red" or color == "blue":
                string += "\t"

            for j in range(NUM_COLORS):
                value = self.values[i*NUM_COLORS + j]
                character = self.colors[value]
                string += f"{character} "
            string += "\n"

        return str(string)

    def unfoldedCubeString(self):
        string = ""
        file = open("unfoldedCubeKey.txt")
        content = file.readlines()

        for line in content:
            values = line.split()

            for val in values:
                val = val.strip()
                if val == "--":
                    string += " "
                elif val == "LL":
                    string += self.colors[0]
                elif val == "RR":
                    string += self.colors[1]
                elif val == "BB":
                    string += self.colors[2]
                elif val == "UU":
                    string += self.colors[3]
                elif val == "DD":
                    string += self.colors[4]
                elif val == "FF":
                    string += self.colors[5]
                else:
                    index = self.values[int(val)]
                    string += self.colors[index]
                string += " "
            string += "\n"

        return str(string)

    def __str__(self):
        string = "\n"
        # string += self.chartString()
        # string += "\n"
        string += self.unfoldedCubeString()
        return str(string)
    
    def rotations(self, algorithm):
        commands = algorithm.split()
        for command in commands:
            command = command.strip()
            self.rotation(command)

    def rotation(self, command):
        print(command, end=" ")
        if len(command) == 1:
            self.rotate(command, False)
        elif len(command) == 2:
            if command[1] == "'":
                self.rotate(command[0], True)
            elif command[1] == "2":
                self.rotate(command[0], False)
                self.rotate(command[0], False)

    def rotate(self, side, prime):
        valuesCopy = self.values.copy()

        # rotate the face
        start = self.sideToValue[side]*8
        old = start
        pivot = 2
        new = start + pivot
        for i in range(8):
            
            if prime:
                self.values[old] = valuesCopy[new]
            else:
                self.values[new] = valuesCopy[old]

            pivot = (pivot + 1) % 8
            old = old + 1
            new = start + pivot

        # rotate the edges touching the face
        edges = self.edges[side].copy()
        pivot = 3
        for i in range(12):
            if prime:
                newIndex = edges[pivot]
                oldIndex = edges[i]
            else:
                newIndex = edges[i]
                oldIndex = edges[pivot]

            self.values[oldIndex] = valuesCopy[newIndex]

            pivot = (pivot + 1) % 12
            
    def checkerBoard(self):
        self.rotation("R2")
        self.rotation("L2")
        self.rotation("F2")
        self.rotation("B2")
        self.rotation("U2")
        self.rotation("D2")
        
    def colorAt(self, index):
        return self.values[index]
    
    def getValues(self):
        return self.values
    
    def getColorsOrder(self):
        return self.colors
            
