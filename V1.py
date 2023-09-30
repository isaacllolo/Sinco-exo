import math
from vpython import *

class Joint:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.sphere = sphere(pos=position, radius=0.2, color=color.blue)

class Bone:
    def __init__(self, name, joint1, joint2):
        self.name = name
        self.joint1 = joint1
        self.joint2 = joint2
        self.connection = curve(pos=[joint1.position, joint2.position], radius=0.05, color=color.red)

class Skeleton3D:
    def __init__(self):
        self.scene = canvas(title="Esqueleto 3D", width=800, height=600)

        # Crear las articulaciones
        self.joints = {
            'Hip': Joint('Hip', vector(0, 0, 0)),
            'Chest': Joint('Chest', vector(0, 2, 0)),
            'Head': Joint('Head', vector(0, 2.75, 0)),
            'LeftShoulder': Joint('LeftShoulder', vector(-1, 2, 0)),
            'RightShoulder': Joint('RightShoulder', vector(1, 2, 0)),
            'LeftElbow': Joint('LeftElbow', vector(-2, 1, 0)),
            'RightElbow': Joint('RightElbow', vector(2, 2, 0)),
            'LeftWrist': Joint('LeftWrist', vector(-3, 1, 0)),
            'RightWrist': Joint('RightWrist', vector(3, 1, 0)),
            'LeftHip': Joint('LeftHip', vector(-0.5, 0, 0)),
            'RightHip': Joint('RightHip', vector(0.5, 0, 0)),
            'LeftKnee': Joint('LeftKnee', vector(-0.5, -2, 0)),
            'RightKnee': Joint('RightKnee', vector(0.5, -2, 0)),
            'LeftAnkle': Joint('LeftAnkle', vector(-0.5, -4, 0)),
            'RightAnkle': Joint('RightAnkle', vector(0.5, -4, 0)),
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

        self.is_update_enabled = True
   
    def update(self, target_positions):
        if self.is_update_enabled:
            # Ajustar las articulaciones basadas en las posiciones objetivo
            self.adjust_joint('LeftWrist', target_positions['LeftWrist'])
            self.adjust_joint('RightWrist', target_positions['RightWrist'])
            self.adjust_joint('LeftElbow', target_positions['LeftElbow'])
            self.adjust_joint('RightElbow', target_positions['RightElbow'])
            self.adjust_joint('LeftShoulder', target_positions['LeftShoulder'])
            self.adjust_joint('RightShoulder', target_positions['RightShoulder'])
            self.adjust_joint('Chest', target_positions['Chest'])
            self.adjust_joint('Head', target_positions['Head'])
            self.adjust_joint('LeftAnkle', target_positions['LeftAnkle'])
            self.adjust_joint('RightAnkle', target_positions['RightAnkle'])
            self.adjust_joint('LeftKnee', target_positions['LeftKnee'])
            self.adjust_joint('RightKnee', target_positions['RightKnee'])
            self.adjust_joint('LeftHip', target_positions['LeftHip'])
            self.adjust_joint('RightHip', target_positions['RightHip'])

    def adjust_joint(self, joint_name, target_position):
        joint = self.joints[joint_name]
        # Calcula el ángulo necesario para que el joint alcance el target_position
        dx = target_position.x - joint.position.x
        dy = target_position.y - joint.position.y
        # Calcula el ángulo usando la función atan2 (ángulo en radianes)
        angle = math.atan2(dy, dx)
        # Convierte el ángulo de radianes a grados
        angle_degrees = math.degrees(angle)
        # Ajusta la rotación del joint en función del ángulo calculado
        joint.sphere.rotate(angle=angle_degrees, axis=vector(0, 0, 1), origin=joint.position)

# Crear una instancia del esqueleto 3D
skeleton_3d = Skeleton3D()


# Bucle de simulación para actualizar el esqueleto con datos simulados
while True:
    rate(60)
    # Posiciones objetivo para cada articulación (por ejemplo, valores simulados)
    target_positions = {
        'LeftWrist': vector(1, 1, 0),
        'RightWrist': vector(-1, 1, 0),
        # Agrega las posiciones objetivo para las demás articulaciones aquí
    }
    skeleton_3d.update(target_positions)