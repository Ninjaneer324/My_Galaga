class Bullet:
    xPos = 0
    yPos = 0
    speed = 0
    move = False

    def __init__(self, x, y, s):
        self.xPos = x
        self.yPos = y
        self.speed = s

    def moveUp(self):
        if self.yPos - self.speed >= 0:
            self.yPos -= self.speed
        elif self.yPos - self.speed < 0:
            self.move = False

    def moveDown(self):
        if self.yPos + 25 <= 800:
            self.yPos += self.speed
        elif self.yPos + 25 > 800:
            self.move = False