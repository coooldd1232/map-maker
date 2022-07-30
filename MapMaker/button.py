import pygame

from reusableClasses.collision import Collision

class Button:
    def __init__(self, pos, width, height, text, textSize, textColor, backgroundColorOffHover, backgroundColorOnHover):
        self.pos = pos
        self.width = width
        self.height = height

        self.textColor = textColor

        self.backgroundColor = backgroundColorOffHover
        self.backgroundColorOffHover = backgroundColorOffHover
        self.backgroundColorOnHover = backgroundColorOnHover

        self.text = text
        self.textSize = textSize
        self.font = self.font = pygame.font.Font('freesansbold.ttf', textSize)

    def Update(self, mousePos):
        if Collision.PointOnRect(mousePos, self.pos, self.width, self.height):
            self.backgroundColor = self.backgroundColorOnHover
        else:
            self.backgroundColor = self.backgroundColorOffHover

    def Draw(self, screen):
        pygame.draw.rect(screen, self.backgroundColor, (self.pos.x, self.pos.y, self.width, self.height))

        text = self.font.render(self.text, True, self.textColor)
        textRect = text.get_rect()
        textRect.center = self.pos.x + self.width / 2, self.pos.y + self.height / 2
        screen.blit(text, textRect)