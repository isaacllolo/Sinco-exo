import math
from vpython import *
import tkinter as tk

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
        # Actualiza la posición de los puntos en la curva existente
        self.connection.modify(0, pos=self.joint1.position)
        self.connection.modify(1, pos=self.joint2.position)
        self.connection.visible = True  # Asegura que el hueso esté visible    
class Skeleton3D:
    def __init__(self):

        # Crear las articulaciones con límites de ángulo
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

        # Crear los huesos
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

        #self.is_update_enabled = True

    def update(self, target_positions):
        #if self.is_update_enabled:
            # Ajustar las articulaciones basadas en las posiciones objetivo
            for joint_name, target_position in target_positions.items():
               # print("Actualizando esqueleto 3D...")
                self.adjust_joint(joint_name, target_position)
            for self.bone in self.bones.values():
                self.bone.update()

    def adjust_joint(self, joint_name, target_position):
        joint = self.joints[joint_name]
        #print(self.joints['RightElbow'].position)
        joint.position = target_position
        joint.sphere.pos = joint.position
    

# Crear una instancia del esqueleto 3
skeleton_3d = Skeleton3D()
scene = canvas(title="Esqueleto 3D", width=800, height=600, center=vector(0, 0, 0))

# Bucle de simulación para actualizar el esqueleto con datos simulados
while True:
    rate(15)
    # Posiciones objetivo para cada articulación (valores simulados)
    target_positions = {
        
       
        'Hip': vector(0, 0, 0),          # Cadera (Hip)
        'Chest': vector(0, 2, 0),        # Pecho (Chest)
        'Head': vector(0, 2.75, 0),      # Cabeza (Head)
        'LeftShoulder': vector(-1, 2, 0), # Hombro Izquierdo (LeftShoulder)
        'RightShoulder': vector(1, 2, 0), # Hombro Derecho (RightShoulder)
        'LeftElbow': vector(-2, 1, 0),   # Codo Izquierdo (LeftElbow)
        'RightElbow': vector(2, 1, 0),   # Codo Derecho (RightElbow)
        'LeftWrist': vector(-3, 1, 0),   # Muñeca Izquierda (LeftWrist)
        'RightWrist': vector(3, 1, 0),   # Muñeca Derecha (RightWrist)
        'LeftHip': vector(-0.5, 0, 0),   # Cadera Izquierda (LeftHip)
        'RightHip': vector(0.5, 0, 0),   # Cadera Derecha (RightHip)
        'LeftKnee': vector(-0.5, -2, 0), # Rodilla Izquierda (LeftKnee)
        'RightKnee': vector(0.5, -2, 0), # Rodilla Derecha (RightKnee)
        'LeftAnkle': vector(-0.5, -4, 0), # Tobillo Izquierdo (LeftAnkle)
        'RightAnkle': vector(0.5, -4, 0) # Tobillo Derecho (RightAnkle)

    }
    
    skeleton_3d.update(target_positions)
    

