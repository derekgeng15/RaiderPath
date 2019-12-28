import os
import csv
import math
import pygame
import pygame.gfxdraw
import HermiteUtil as hu
import Geometry as geo
import RobotSim
import UserInput
import GUIUtil

pygame.init()
LENGTH = int(319 * 1.5)
WIDTH = int(649 * 1.5)
Display = pygame.display.set_mode((WIDTH + 200, LENGTH))
pygame.scrap.init()

pygame.display.set_caption("RaiderPath")
Run = True
curve = hu.Curve(UserInput.startTheta * math.pi/180,
                 UserInput.endTheta * math.pi/180)
Dragging = False
ShowWaypoints = True
Dragpoint = geo.WayPoint(0, 0)
bkimg = pygame.image.load("images\\2019-Field.jpg")


nameBox = GUIUtil.Textbox(WIDTH + 25, 50, 150, 30, "Path Name")
startHeadingBox = GUIUtil.NumBox(WIDTH + 50, 125, 100, 30, "Start Heading")
endHeadingBox = GUIUtil.NumBox(WIDTH + 50, 200, 100, 30, "End Heading")
robotWidthBox = GUIUtil.NumBox(WIDTH + 50, 275, 100, 30, "Robot Width")
robotLengthBox = GUIUtil.NumBox(WIDTH + 50, 350, 100, 30, "Robot Length")
saveButton = GUIUtil.Button(WIDTH + 50, 425, 100, 30, "Save")

textboxes = []
textboxes.append(nameBox)
textboxes.append(startHeadingBox)
textboxes.append(endHeadingBox)
textboxes.append(robotWidthBox)
textboxes.append(robotLengthBox)
writing = False


def readFile():
    curve.waypoints = []
    if os.path.exists("paths\\" + UserInput.fileName + ".csv"):
        with open("paths\\" + UserInput.fileName + ".csv") as file:
            csv_reader = csv.reader(file, delimiter=',')
            line = 0
            for row in csv_reader:
                if line == 0:
                    UserInput.robotWidth = float(row[0])
                elif line == 1:
                    UserInput.robotLength = float(row[0])
                elif line != 2:
                    curve.add_point(geo.WayPoint(
                        float(row[0]), float(row[1])))
                    curve.waypoints[-1].theta = float(row[2]) * math.pi/180
                line += 1
            file.close()
        if curve.waypoints is not []:
            UserInput.startTheta = curve.waypoints[0].theta * 180/math.pi
            UserInput.endTheta = curve.waypoints[-1].theta * 180/math.pi
        else:
            UserInput.startTheta = 0.0
            UserInput.endTheta = 0.0
        startHeadingBox.text = str(UserInput.startTheta)
        endHeadingBox.text = str(UserInput.endTheta)
        robotLengthBox.text = str(UserInput.robotLength)
        robotWidthBox.text = str(UserInput.robotWidth)


def saveFile():
    if UserInput.fileName is not "":
        print("..saving..")
        file = open("paths\\" + UserInput.fileName + ".csv", 'w')
        file.write(str(UserInput.robotWidth) + '\n')
        file.write(str(UserInput.robotLength) + '\n')
        file.write("x, y, heading\n")
        for point in curve.waypoints:
            file.write(str(point.x) + ',' + str(point.y) + ',' +
                       str(point.theta * 180/math.pi) + '\n')
        file.close()


readFile()

robot = RobotSim.Robot(
    geo.Pose(0, 0, 0), UserInput.robotWidth, UserInput.robotLength)
bkimg = pygame.transform.scale(bkimg, (WIDTH, LENGTH))
while Run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Run = False
        if event.type == pygame.MOUSEBUTTONUP:
            Dragging = False
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if Dragging and pos[0] <= WIDTH / 2:
                Dragpoint.x = pos[0] / 1.5
                Dragpoint.y = (LENGTH - pos[1]) / 1.5
                curve.calc_tang()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for wp in curve.waypoints:
                if pos[0] >= wp.x * 1.5 - 5 and pos[0] <= wp.x * 1.5 + 5 and LENGTH - pos[1] >= wp.y * 1.5 - 5 and LENGTH - pos[1] <= wp.y * 1.5 + 5:
                    Dragpoint = wp
                    Dragging = True
                    break
            if not Dragging and pos[0] <= WIDTH / 2:
                curve.add_point(geo.WayPoint(pos[0] / 1.5, (LENGTH - pos[1])/1.5))
            for box in textboxes:
                box.isClicked(pos)
            saveButton.isClicked(pos)
        if event.type == pygame.MOUSEBUTTONUP:
            if saveButton.active:
                saveFile()
                saveButton.active = False
        if event.type == pygame.KEYDOWN:
            mod = pygame.key.get_mods()
            writing = False
            for box in textboxes:
                if box.active:
                    if mod & pygame.KMOD_CAPS or mod & pygame.KMOD_LSHIFT or mod & pygame.KMOD_RSHIFT:
                        box.addText(event.key + 65 - 97)
                    elif (mod & pygame.KMOD_LCTRL or mod & pygame.KMOD_RCTRL):
                        if chr(event.key) is 'v':
                            text = list(pygame.scrap.get(pygame.SCRAP_TEXT))
                            for c in text:
                                if not box.addText(c):
                                    break
                        if event.key is 8:
                            box.text = ""
                    else:
                        box.addText(event.key)
                    writing = True
                    break
            if not writing:
                if event.key == pygame.K_BACKSPACE:
                    curve.waypoints.pop()
                    curve.calc_tang()
                elif event.key == pygame.K_BACKSLASH:
                    if ShowWaypoints:
                        ShowWaypoints = False
                    else:
                        ShowWaypoints = True
    Display.fill([100, 100, 100])
    Display.blit(bkimg, (0, 0))
    curve.drawCurve(Display, hu.BLACK)
    if ShowWaypoints:
        curve.drawWayPoints(Display, hu.RED)
    if curve.waypoints != []:
        robot.pos = geo.Pose(
            curve.waypoints[0].x, curve.waypoints[0].y, curve.startHeading)
        robot.draw(Display, [255, 255, 0])
    if len(curve.waypoints) >= 2:
        robot.pos = geo.Pose(
            curve.waypoints[-1].x, curve.waypoints[-1].y, curve.endHeading)
        robot.draw(Display, [255, 255, 0])
    if Dragging:
        Dragpoint.draw_point(Display, hu.GREEN, 10)
    for box in textboxes:
        if not box.active and box.text is not "":
            if box.name == "Path Name" and box.text is not UserInput.fileName:
                saveFile()
                UserInput.fileName = box.text
                pygame.display.set_caption("RaiderPath (" + box.text + ")")
                readFile()
            elif box.name == "Start Heading" and list(box.text)[0] >= '0' and list(box.text)[0] <= '9':
                curve.startHeading = float(box.text) * math.pi/180
                curve.calc_tang()
            elif box.name == "End Heading" and list(box.text)[0] >= '0' and list(box.text)[0] <= '9':
                curve.endHeading = float(box.text) * math.pi/180
                curve.calc_tang()
            elif box.name == "Robot Width" and list(box.text)[0] >= '0' and list(box.text)[0] <= '9':
                robot.width = float(box.text)
                UserInput.robotWidth = robot.width
            elif box.name == "Robot Length" and list(box.text)[0] >= '0' and list(box.text)[0] <= '9':
                robot.length = float(box.text)
                UserInput.robotLength = robot.length
        box.draw(Display)
    saveButton.draw(Display)
    pygame.display.update()

saveFile()

pygame.quit()
