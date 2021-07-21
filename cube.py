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
    
    values = [0,0,0,0,0,0,0,0,
              1,1,1,1,1,1,1,1,
              2,2,2,2,2,2,2,2,
              3,3,3,3,3,3,3,3,
              4,4,4,4,4,4,4,4,
              5,5,5,5,5,5,5,5]
    
    colors = {0:"r",1:"o",2:"y",3:"g",4:"b",5:"w"}
    
    sides = ["L", "R", "B", "U", "D", "F"]
    
    def set(self,values,colors):
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
        string = ""
        # string += self.chartString()
        # string += "\n"
        string += self.unfoldedCubeString()
        return str(string)
    
    
            
       
        
        
