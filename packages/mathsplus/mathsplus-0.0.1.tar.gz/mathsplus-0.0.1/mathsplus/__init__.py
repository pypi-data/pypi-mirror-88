#MathsPlus By Tom and Connor
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

sphere = Pi(3, 3.14, "sphere")
circle = Pi(3, 3.14, "circle")
print(sphere.volume_of_sphere(sphere.radius, sphere.pi_value, sphere.type))

class Shapes():
    def __init__(self, num_sides):
        self.num_sides = num_sides
        
    def sum_interior(self, num_sides):
        return 180 * (num_sides - 2)
    
    def one_interior(self, num_sides):
        return 180 * (num_sides - 2) / num_sides

    def one_exterior(self, num_sides):
        return 360 / num_sides

class Hcm():
    def __init__(self, numbers):
        self.numbers = numbers
    
    def find_hcf(self, numbers):
        x = numbers[0]
        y = numbers[1]

        if x > y:
            smaller = y
        else:
            smaller = x
        for i in range(1, smaller+1):
            if ((x % i == 0) and (y % i == 0)):
                hcf = i
        return hcf

    def find_lcm(self, numbers):
        x = numbers[0]
        y = numbers[1]
        if x > y:
            greater = x
            smaller = y
        else:
            greater = y
            smaller = x

        while(True):
            if((greater % x == 0) and (greater % y == 0)):
                lcm = greater
                break
            greater += smaller
        return lcm
                

class Graphs():
    #BIG BERTHA NEEDS LOTS OF WORK
    def __init__(self, x, y, xx, yy):
        self.x = x
        self.y = y
        self.xx = xx
        self.yy = yy

    def gradient(self, x, y, xx, yy):
        dif_x = x - xx
        dif_y = y - yy
        return dif_y / dif_x


        