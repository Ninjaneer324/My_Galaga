class Ship:
    xPos = 0
    yPos = 0
    left = False
    right = False
    exist = True

    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos

    def moveLeft(self):
       if self.xPos - 5 >= 30:
            self.xPos -= 5

    def moveRight(self):
        if self.xPos + 60 <= 450:
            self.xPos += 5