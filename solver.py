from cube import Cube

class Solver:
    
    edges = {"UL":(31,3), "UR":(27,15), "UB":(25,21), "UF":(29,41),
             "FL":(47,5), "FR":(43,13), "BL":(23,1), "BR":(19,9),
             "DL":(39,7), "DR":(35,11), "DB":(37,17), "DF":(33,45)}
    
    corners = {"UFL":(30,40,4), "URF":(28,14,42), "UBR":(26,20,8), "ULB":(24,2,22),
               "DLF":(32,6,46), "DFR":(34,44,12), "DBL":(38,16,0), "DRB":(36,10,18)}
    
    def __init__(self, cube: Cube):
        self.cube = cube
        
    
        