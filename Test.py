import math
from vpython import *
import tkinter as tk
from graphics import *
import keyboard
from time import sleep
import time
from win32api import GetKeyState
from pyautogui import position as mousePos
from math import atan2, cos, sin, pi

class Joint:
    def __init__(self, name, position, min_angle=None, max_angle=None):
        self.name = name
        self.position = position
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.sphere = sphere(pos=position, radius=0.2, color=color.blue)

class Bone:
    def __init__(self, name, joint1, joint2):
        self.name = name
        self.joint1 = joint1
        self.joint2 = joint2
        self.connection = curve(pos=[joint1.position, joint2.position], radius=0.05, color=color.red)
    
    def update(self):
        self.connection.modify(0, pos=self.joint1.position)
        self.connection.modify(1, pos=self.joint2.position)
        self.connection.visible = True

class Skeleton3D:
    def __init__(self):
        self.joints = {
            'Hip': Joint('Hip', vector(0, 0, 0)),
            'Chest': Joint('Chest', vector(0, 2, 0)),
            'Head': Joint('Head', vector(0, 2.75, 0)),
            'LeftShoulder': Joint('LeftShoulder', vector(-1, 2, 0)),
            'RightShoulder': Joint('RightShoulder', vector(1, 2, 0)),
            'LeftElbow': Joint('LeftElbow', vector(-2, 1, 0), -math.pi/2, math.pi/2),
            'RightElbow': Joint('RightElbow', vector(2, 1, 0), -math.pi/2, math.pi/2),
            'LeftWrist': Joint('LeftWrist', vector(-3, 1, 0), -math.pi/4, math.pi/4),
            'RightWrist': Joint('RightWrist', vector(3, 1, 0), -math.pi/4, math.pi/4),
            'LeftHip': Joint('LeftHip', vector(-0.5, 0, 0), -math.pi/4, math.pi/4),
            'RightHip': Joint('RightHip', vector(0.5, 0, 0), -math.pi/4, math.pi/4),
            'LeftKnee': Joint('LeftKnee', vector(-0.5, -2, 0), -math.pi/2, math.pi/2),
            'RightKnee': Joint('RightKnee', vector(0.5, -2, 0), -math.pi/2, math.pi/2),
            'LeftAnkle': Joint('LeftAnkle', vector(-0.5, -4, 0), -math.pi/4, math.pi/4),
            'RightAnkle': Joint('RightAnkle', vector(0.5, -4, 0), -math.pi/4, math.pi/4),
        }

        self.bones = {
            'HipToChest': Bone('HipToChest', self.joints['Hip'], self.joints['Chest']),
            'ChestToHead': Bone('ChestToHead', self.joints['Chest'], self.joints['Head']),
            'ChestToLeftShoulder': Bone('ChestToLeftShoulder', self.joints['Chest'], self.joints['LeftShoulder']),
            'ChestToRightShoulder': Bone('ChestToRightShoulder', self.joints['Chest'], self.joints['RightShoulder']),
            'LeftShoulderToLeftElbow': Bone('LeftShoulderToLeftElbow', self.joints['LeftShoulder'], self.joints['LeftElbow']),
            'RightShoulderToRightElbow': Bone('RightShoulderToRightElbow', self.joints['RightShoulder'], self.joints['RightElbow']),
            'LeftElbowToLeftWrist': Bone('LeftElbowToLeftWrist', self.joints['LeftElbow'], self.joints['LeftWrist']),
            'RightElbowToRightWrist': Bone('RightElbowToRightWrist', self.joints['RightElbow'], self.joints['RightWrist']),
            'HipToLeftHip': Bone('HipToLeftHip', self.joints['Hip'], self.joints['LeftHip']),
            'HipToRightHip': Bone('HipToRightHip', self.joints['Hip'], self.joints['RightHip']),
            'LeftHipToLeftKnee': Bone('LeftHipToLeftKnee', self.joints['LeftHip'], self.joints['LeftKnee']),
            'RightHipToRightKnee': Bone('RightHipToRightKnee', self.joints['RightHip'], self.joints['RightKnee']),
            'LeftKneeToLeftAnkle': Bone('LeftKneeToLeftAnkle', self.joints['LeftKnee'], self.joints['LeftAnkle']),
            'RightKneeToRightAnkle': Bone('RightKneeToRightAnkle', self.joints['RightKnee'], self.joints['RightAnkle']),
        }

    def update(self, target_positions):
        for joint_name, target_position in target_positions.items():
            self.adjust_joint(joint_name, target_position)
        for bone in self.bones.values():
            bone.update()

    def adjust_joint(self, joint_name, target_position):
        joint = self.joints[joint_name]
        joint.position = target_position
        joint.sphere.pos = joint.position

skeleton_3d = Skeleton3D()
scene = canvas(title="Esqueleto 3D", width=800, height=600, center=vector(0, 0, 0))

class window:
    width = 1080
    height = 1080
    vertical_resolution = 256
    horizontal_resolution = 256
    ratio = height / width

class FPS:
    value = int()
    maxValue = 'auto'
    timer = 0
    counter = object

    if maxValue == 0 or maxValue == 'none':
        maxValue = 999
    elif maxValue == 'auto':
        maxValue = getattr(EnumDisplaySettings(
            EnumDisplayDevices().DeviceName, -1), 'DisplayFrequency')

    lastValue = maxValue

start_clock_time = time.time()
last_clock_time = 0

def rgb(red, green, blue):
    hexValue = '#%02x%02x%02x' % (red, green, blue)
    return hexValue

class setting:
    regularChain = True
    chainLength = 20
    jointLength = 60
    showJointCounter = True
    showVectors = False
    showLastVector = True
    colorFade = True
    color = rgb(63,93,178)
    sizeFade = True
    maxWidth = 10
    instantUpdate = False
    showTrail = False
    trailLength = chainLength*15
    trail = []
    origin = (-300,0)
    showOrigin = True
    showTarget = True
    showFPS = True

originPX, originPY = setting.origin[0], setting.origin[1]

if setting.regularChain:
    joints = [[setting.jointLength, [originPX, originPY+setting.jointLength*chainJoint]]for chainJoint in range(setting.chainLength+1)]
else:
    joints = [[200, [0, 200]], [200, [0, 400]], [200, [0, 600]], [200, [0, 800]], [200, [0, 1000]], [200, [0, 1200]], [200, [0, 1400]], [200, [0, 1600]], [200, [0, 1800]], [200, [0, 2000]], [200, [0, 2200]], [200, [0, 2400]]

render = GraphWin('render', window.width, window.height, autoflush=False)
render.setCoords(-window.width, -window.height, window.width, window.height)

targetX, targetY = 1000, 0
gotoX, gotoY = 1000, 0

def rotateJoint(origin, point, shiftAngle):
    originX, originY = origin[1][0], origin[1][1]
    pointX, pointY = point[1][0], point[1][1]

    shiftX = originX + cos(shiftAngle) * (pointX - originX) - sin(shiftAngle) * (pointY - originY)
    shiftY = originY + sin(shiftAngle) * (pointX - originX) + cos(shiftAngle) * (pointY - originY)

    return [origin[0], [shiftX, shiftY]]

def clear():
    for item in render.items[:]:
        item.undraw()

def refresh():
    clear()
    global FPS, last_clock_time

    clock_time = time.time() - start_clock_time
    FPS.timer = clock_time - last_clock_time
    FPS.value += 1

    global joints, targetX, targetY, originPX, originPY

    if setting.showTrail:
        for _trail in joints:
            setting.trail.append(Point(_trail[1][0],_trail[1][1]))
            if len(setting.trail) == setting.trailLength:
                del setting.trail[0]

        for _trail in range(len(setting.trail)-1,0,-1):
            trailFade = rgb(255,255-int((_trail+1)/len(setting.trail)*255),255-int((_trail+1)/len(setting.trail)*255))
            if (_trail != 0) and not(setting.trail[_trail].x == originPX and int(setting.trail[_trail].y) == originPY):
                Line(setting.trail[_trail], setting.trail[_trail-1]).draw(render).setFill(trailFade)

    for _joint in range(len(joints)):
        if _joint == 0:
            jointOrigin = Point(originPX, originPY)
        else:
            jointOrigin = Point(joints[_joint-1][1][0],joints[_joint-1][1][1])

        jointTarget = Point(joints[_joint][1][0],joints[_joint][1][1])
        jointLine = Line(jointOrigin, jointTarget)

        jointWidth = 3*abs(1-(len(joints)/(_joint+1)))+1

        if setting.sizeFade:
            if jointWidth > setting.maxWidth:
                jointWidth = setting.maxWidth
        else:
            jointWidth = setting.maxWidth

        jointLine.setWidth(jointWidth)

        if setting.showVectors:
            jointLine.setArrow('last')

        if setting.showLastVector and _joint == len(joints)-1:
            jointLine.setArrow('last')

        if setting.colorFade:
            jointLine.setFill(rgb(64,128,round(abs((_joint+1)/len(joints))*255)))
        else:
            jointLine.setFill(setting.color)

        jointLine.draw(render)

    for _joint in range(len(joints)-1,-1,-1):
        if _joint == len(joints)-1:
            anchor = (targetX, targetY)
        else:
            anchor = (joints[len(joints)-1][1][0],joints[len(joints)-1][1][1])

        if _joint == 0:
            origin = (originPX,originPY)
        else:
            origin = (joints[_joint-1][1][0],joints[_joint-1][1][1])

        target = (targetX, targetY)

        angle = -atan2((anchor[0]-origin[0]) , (anchor[1]-origin[1]))+pi/2
        targetAngle = -atan2((target[0]-origin[0]) , (target[1]-origin[1]))+pi/2
        shiftAngle = targetAngle - angle

        if _joint == len(joints)-1:
            joints[_joint][1][0] = origin[0] + joints[_joint][0] * cos(angle)
            joints[_joint][1][1] = origin[1] + joints[_joint][0] * sin(angle)
        else:
            for __joint in range(_joint,len(joints)):
                if _joint == 0:
                    joints[__joint] = rotateJoint([joints[0][0],[originPX,originPY]], joints[__joint], shiftAngle)
                else:
                    joints[__joint] = rotateJoint(joints[_joint-1], joints[__joint], shiftAngle)

    mousePos = [int(content) for content in render.master.winfo_geometry().split("+",1)[1].split("+",1)]
    mouseX = (mousePos()[0] - renderPos[0])*2 - render.width - 16
    mouseY = (-mousePos()[1] - renderPos[1])*2 + render.height + 64

    if GetKeyState(0x01) < 0:
        mousePressed = True
        gotoX, gotoY = mouseX, mouseY
    else:
        mousePressed = False

    if setting.instantUpdate:
        targetX, targetY = gotoX, gotoY
    else:
        targetX, targetY = targetX + (gotoX-targetX)/20, targetY + (gotoY-targetY)/20

    clock_time = time.time() - start_clock_time
    refresh()
    update(FPS.maxValue*1.05)

    inputSpeed = 1.0 / ((FPS.lastValue+0.01) / 120)

    if keyboard.is_pressed('&'):
        if not(setting.showLastVector):
            setting.showLastVector = True
        else:
            setting.showLastVector = False
        while keyboard.is_pressed('&'):
            sleep(0.1)

    if keyboard.is_pressed('é'):
        if not(setting.showTarget):
            setting.showTarget = True
        else:
            setting.showTarget = False
        while keyboard.is_pressed('é'):
            sleep(0.1)

    if keyboard.is_pressed('"'):
        if not(setting.instantUpdate):
            setting.instantUpdate= True
        else:
            setting.instantUpdate = False
        while keyboard.is_pressed('"'):
            sleep(0.1)

    if keyboard.is_pressed("'"):
        if not(setting.showTrail):
            setting.showTrail = True
        else:
            setting.showTrail = False
        while keyboard.is_pressed("'"):
            sleep(0.1)

    if keyboard.is_pressed('esc'):
        render.close()
