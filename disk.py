class Disk:
    """A disk"""
    def __init__(self, SPACE, rows, col_idx, disks_of_col, isRed, diam):
        self.SPACE = SPACE
        self.diam = diam
        self.x = col_idx*self.diam + self.diam/2
        self.y = self.SPACE['h'] - rows*self.diam - self.diam/2
        self.disks_of_col = disks_of_col  # show how many disks of the col
        self.isRed = isRed
        if self.isRed:
            self.fill_color = (0.8, 0.2, 0.2)
        else:
            self.fill_color = (1.0, 1.0, 0)
        self.y_vel = 1  # initialize disk falling speed to 0
        self.g = 3  # acceleration of disk falling speed
        # calculate a lowest point(largest y value) a disk can reach
        self.lowest_point = self.SPACE['h'] - self.diam*self.disks_of_col - \
            self.diam/2

    def draw_me(self):
        factor = 0.85  # set diameter to 0.85 times self.diam
        noStroke()
        fill(*self.fill_color)
        ellipse(self.x, self.y, self.diam*factor, self.diam*factor)

    def display(self):
        if self.y < self.lowest_point:
            self.y += self.y_vel
            self.y_vel += self.g  # update acceleration of speed
        else:
            self.y = self.lowest_point
        self.draw_me()
