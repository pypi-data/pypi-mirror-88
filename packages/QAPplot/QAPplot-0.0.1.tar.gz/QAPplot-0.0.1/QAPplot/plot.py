import os
print('installing graphics.py')
os.system('pip install graphics.py')

from graphics import *
import math
class QAPplot:
    def __init__(self, screen_width=700):
        self.screen_width = screen_width
        self.center = self.screen_width/2, self.screen_width/2+screen_width*0.1
        # self.
    def demo(self):
        win = GraphWin('Geoplot ver.0.0.1', self.screen_width, self.screen_width)
        grid = Grid(win, self.center, self.screen_width*0.6)
        grid.draw()
        grid.plot(20,30,50)
        grid.plot(45,35,20)

        while True:
            temp = win.getMouse()
    def plot(self, top, left, right, offset=0.6):
        win = GraphWin('Geoplot ver.0.0.1', self.screen_width, self.screen_width)
        grid = Grid(win, self.center, self.screen_width*offset)
        grid.draw()
        grid.plot(top,left,right)
        while True:
            temp = win.getMouse()
        
class Grid:
    def __init__(self, win, center, width):
        self.win = win
        self.x, self.y = center[0], center[1]
        self.width = width
        self.height = self.width*math.cos(math.pi/6)
        self.med = self.height*2/3 # distance from center to top
        self.center = center
        assert self.y-self.med > 0, 'too much width'
        
        #corner
        self.top = (self.x, self.y-self.med)
        self.left = (self.x-self.width/2, self.y+self.height/3)
        self.right = (self.x+self.width/2, self.y+self.height/3)
        #grid corner
        self.grid_corner = [(self.top, self.left), (self.left,self.right), (self.right, self.top)]
        #grid in
        left_points = self.get_div_points(self.top, self.left)
        right_points = self.get_div_points(self.top, self.right)
        bottom_points = self.get_div_points(self.left, self.right)
        self.grid_in = []
        for p1, p2 in [(left_points, right_points), (right_points,bottom_points),(bottom_points, left_points[::-1])]:
            self.grid_in.extend([(p1[i], p2[i]) for i in range(len(p1))])
    def line_intersection(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y
    def plot(self, top, left, right, size=5, color='blue'):
        sum_ = top+left+right
        top, left, right = top/sum_, left/sum_, right/sum_
        dist_top = self.height*(1-top)
        y = self.top[1] + dist_top
        line1 = ((0,y),(self.center[0]+self.width,y))
        
        dist_left = self.width*(1-left)
        p1 = self.left[0] + dist_left , self.left[1]
        p2 = self.left[0] + dist_left*0.5 , self.left[1]-dist_left*math.cos(math.pi/6)
        line2 = (p1, p2)
      
        # myline = Line(Point(p1[0],p1[1]), Point(p2[0],p2[1]))
        # myline.draw(self.win)
        x, y = self.line_intersection(line1, line2)
        
        # x = self.left[0] + dist_left
        # x = self.left[0]
        
        ans = Circle(Point(x,y), size)
        ans.setFill(color)
        ans.draw(self.win)
        
        
        
   
    def get_div_points(self, p1, p2):
        ans = []
        div_n = 10
        dist_x = p1[0] - p2[0]
        dist_y = p1[1] - p2[1]
        for i in range(1,div_n):
            x = p2[0] + dist_x*i/div_n 
            y = p2[1] + dist_y*i/div_n
            ans.append((x,y))
        return ans
            
            
        
    def get_corner(self, color='blue', size=3):
        point = []
        for point_ in [self.top, self.left, self.right]:
            circle = Circle(Point(point_[0],point_[1]), size)
            circle.setFill(color)
            point.append(circle)
            # print(point_)
        return point
    def get_line(self, lines, color='black', linewidth=1):
        ans = []
        for p1, p2 in lines:
            p1, p2 = Point(p1[0],p1[1]), Point(p2[0],p2[1])
            myline = Line(p1, p2)
            myline.setWidth(linewidth)
            ans.append(myline)
        return ans
    def draw(self):
        draw_ = [self.get_corner(), self.get_line(self.grid_corner), self.get_line(self.grid_in)]
        for draw__ in draw_:
            for e in draw__:
                e.draw(self.win)
    
if __name__ == "__main__":
    graph = QAPplot()
    # graph.demo()
    graph.plot(20,40,40)
   
