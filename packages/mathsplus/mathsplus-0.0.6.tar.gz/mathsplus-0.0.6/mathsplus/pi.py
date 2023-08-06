class Pi():
    def __init__(self, radius, pi_value, type):
        self.radius = radius
        self.pi_value = pi_value
        self.type = type
    
    def diameter(self, radius, type):
        return radius * 2
    
    def circumference(self, radius, pi_value, type):
        return 2 * pi_value * radius
    
    def area(self, radius, pi_value, type):
        if type == "circle":
            return pi_value * radius * radius
        else:
            return 0

    def volume_of_sphere(self, radius, pi_value, type):
        if type == "sphere":
            part1 = 4/3
            part2 = pi_value * radius**3
            return part1 * part2
        else:
            return 0