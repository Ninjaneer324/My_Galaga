class Alien:
    xPos = 0
    yPos = 0
    left = False
    right = True
    exist = True
    num = 1

    def __init__(self, x, y, num):
        self.xPos = x
        self.yPos = y
        self.num = num

    def moveLeft(self):
        if self.left and self.xPos - 3 >= 0:
            self.xPos -= 3
        if self.xPos - 3 < 0:
            self.left = False
            self.right = True

    def moveRight(self):
        if self.right and self.xPos + 28 <= 480:
            self.xPos += 3
        if self.xPos + 28 > 480:
            self.left = True
            self.right = False