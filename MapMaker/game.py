import pygame
import math
import datetime
from tkinter import *
from tkinter import filedialog

from reusableClasses.vector2 import Vector2
from reusableClasses.collision import Collision

from camera import Camera
from rect import Rect
from button import Button
from loadMap import LoadMap

class Game:
    def __init__(self, screenWidth, screenHeight, rects):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.camera = Camera(Vector2(0, 0))

        self.rects = rects
        if self.rects == []:
            self.rects.append(Rect(Vector2(200, 200), 100, 100))

        self.rectSelected = None
        self.pointSelected = None

        self.hoveringOnTopEdge = False
        self.hoveringOnRightEdge = False
        self.hoveringOnBotEdge = False
        self.hoveringOnLeftEdge = False

        self.isLeftClicking = False

        self.zoom = 1

        self.font = pygame.font.Font('freesansbold.ttf', 30)

        self.normalCursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.resizeCursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

        self.mousePos = Vector2()

        self.saveButton = Button(Vector2(screenWidth - 150, 0), 150, 70, "save map", 25, (0, 0, 0), (0, 255, 255), (0, 204, 204))
        self.loadButton = Button(Vector2(screenWidth - 150, 80), 150, 70, "load map", 25, (0, 0, 0), (0, 255, 255), (0, 204, 204))

    def Update(self, mousePos):
        self.mousePos = mousePos
        mousePosCam = mousePos - self.camera.offset

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.camera.pos.x -= 5 * 1 / self.zoom
        if keys[pygame.K_d]:
            self.camera.pos.x += 5 * 1 / self.zoom
        if keys[pygame.K_w]:
            self.camera.pos.y -= 5 * 1 / self.zoom
        if keys[pygame.K_s]:
            self.camera.pos.y += 5 * 1 / self.zoom

        self.saveButton.Update(mousePos)
        self.loadButton.Update(mousePos)

        if self.rectSelected is not None:
            # check if you hover on edge of selected Rect
            if self.isLeftClicking is False:
                rect = self.rectSelected
                self.hoveringOnTopEdge = False
                self.hoveringOnRightEdge = False
                self.hoveringOnBotEdge = False
                self.hoveringOnLeftEdge = False
                # hover with top side of rect
                if Collision.PointOnRect(mousePosCam, Vector2(rect.pos.x + 5, rect.pos.y), rect.width - 10, 5):
                    self.hoveringOnTopEdge = True
                # hover with right side of rect
                elif Collision.PointOnRect(mousePosCam, Vector2(rect.pos.x + rect.width - 5, rect.pos.y + 5), 5, rect.height - 10):
                    self.hoveringOnRightEdge = True
                # hover with bot side of rect:
                elif Collision.PointOnRect(mousePosCam, Vector2(rect.pos.x + 5, rect.pos.y + rect.height - 5), rect.width - 10, 5):
                    self.hoveringOnBotEdge = True
                # hover with left side of rect:
                elif Collision.PointOnRect(mousePosCam, Vector2(rect.pos.x, rect.pos.y + 5), 5, rect.height - 10):
                    self.hoveringOnLeftEdge = True

                if not(self.hoveringOnTopEdge or self.hoveringOnRightEdge or self.hoveringOnBotEdge or self.hoveringOnLeftEdge):
                    pygame.mouse.set_cursor(self.normalCursor)
                else:
                    pygame.mouse.set_cursor(self.resizeCursor)

        # reshape rects
        if self.isLeftClicking:
            if self.hoveringOnRightEdge:
                self.rectSelected.width = math.ceil((mousePosCam.x - self.rectSelected.pos.x) / 5) * 5
            elif self.hoveringOnBotEdge:
                self.rectSelected.height = math.ceil((mousePosCam.y - self.rectSelected.pos.y) / 5) * 5
            elif self.hoveringOnLeftEdge:
                prevPos = self.rectSelected.pos.x
                self.rectSelected.pos.x = math.ceil(mousePosCam.x / 5) * 5
                self.rectSelected.width += prevPos - self.rectSelected.pos.x
            elif self.hoveringOnTopEdge:
                prevPos = self.rectSelected.pos.y
                self.rectSelected.pos.y = math.ceil(mousePosCam.y / 5) * 5
                self.rectSelected.height += prevPos - self.rectSelected.pos.y

        # updates rect pos if you are dragging and moving
        # self.pointSelected should only be none if self.rectSelected is None
        if self.zoom == 1:
            if self.rectSelected is not None and self.isLeftClicking:
                if not(self.hoveringOnTopEdge or self.hoveringOnRightEdge or self.hoveringOnBotEdge or self.hoveringOnLeftEdge):
                    newPos = round((mousePosCam - self.pointSelected) / 5) * 5
                    self.rectSelected.pos = newPos

    def Draw(self, screen):
        screen.fill((100, 100, 100))

        for rect in self.rects:
            pygame.draw.rect(screen, (0, 0, 0), ((rect.pos.x + self.camera.offset.x) * self.zoom, (rect.pos.y + self.camera.offset.y) * self.zoom, rect.width * self.zoom, rect.height * self.zoom))

        # draw selected rect details
        if self.rectSelected is not None:
            text = self.font.render(f'pos: {self.rectSelected.pos} | dim: {self.rectSelected.width}, {self.rectSelected.height}', True, (26, 247, 253))
            textRect = text.get_rect()
            textRect.center = self.screenWidth / 2, self.screenHeight - self.screenHeight / 7
            screen.blit(text, textRect)

        self.saveButton.Draw(screen)
        self.loadButton.Draw(screen)

        pygame.display.flip()

    def OnKeyDown(self, key):
        if key == pygame.K_SPACE:
            # check if mouse is on rect
            for rect in self.rects:
                if Collision.PointOnRect(self.mousePos + self.camera.pos, rect.pos, rect.width, rect.height):
                    self.rects.append(Rect(rect.pos, rect.width, rect.height))
                    return

            self.rects.append(Rect(self.mousePos+self.camera.pos - Vector2(50, 50), 100, 100))

    def OnClick(self, button, mousePos):
        mousePosCam = mousePos - self.camera.offset

        if button == 1:
            self.isLeftClicking = True

            # check if you are clicking on a Rect, if you are update rectSelected
            clickedOnRect = False
            for rect in self.rects:
                if Collision.PointOnRect(mousePosCam, rect.pos, rect.width, rect.height):
                    self.rectSelected = rect
                    self.pointSelected = mousePosCam - rect.pos
                    clickedOnRect = True
                    break
            if clickedOnRect is False:
                self.rectSelected = None
                self.pointSelected = None

        if button == 1:
            # save button
            if Collision.PointOnRect(mousePos, self.saveButton.pos, self.saveButton.width, self.saveButton.height):
                # get time and date
                timeMade = str(datetime.datetime.now())

                timeMade = str(timeMade[12:-7])
                timeMade = timeMade.replace(':', ';')

                textFileName = f'map made at {timeMade}'

                with open(f'maps/{textFileName}.txt', 'w') as f:
                    for rect in self.rects:
                        f.write(f'{rect.pos.x}, {rect.pos.y}, {rect.width}, {rect.height}\n')

            # load button
            elif Collision.PointOnRect(mousePos, self.loadButton.pos, self.loadButton.width, self.loadButton.height):
                root = Tk()
                root.withdraw()

                root.filename = filedialog.askopenfilename(initialdir="/", title="select a map",
                                                           filetypes=(("txt files", "*.txt"), ("all files", "*.*")))

                # if you pressed cancel or no filed opened
                if root.filename == '':
                    return
                rects = LoadMap(root.filename)
                self.__init__(self.screenWidth, self.screenHeight, rects)

        if button == 2:
            if self.zoom == 1:
                self.camera.pos = Vector2(0, 0)
            self.zoom = 1

        if button == 3:
            # delete rect
            for rect in self.rects:
                if Collision.PointOnRect(mousePos + self.camera.pos, rect.pos, rect.width, rect.height):
                    self.rects.remove(rect)
                    break

    def OnClickRelease(self, button, mousePos):
        if button == 1:
            self.isLeftClicking = False

    def OnScroll(self, x, y):
        # scrolling up is 1 scrolling down is -1
        if y == 1:
            self.zoom *= 1.5
        if y == -1:
            self.zoom /= 1.5

    def OnWindowResize(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.saveButton.pos.x = screenWidth - 150
        self.loadButton.pos.x = screenWidth - 150
