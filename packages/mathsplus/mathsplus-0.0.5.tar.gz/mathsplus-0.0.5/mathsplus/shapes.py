class Shapes():
    def __init__(self, num_sides):
        self.num_sides = num_sides
        
    def sum_interior(self, num_sides):
        return 180 * (num_sides - 2)
    
    def one_interior(self, num_sides):
        return 180 * (num_sides - 2) / num_sides

    def one_exterior(self, num_sides):
        return 360 / num_sides