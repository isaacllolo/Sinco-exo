import math
from vpython import *

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

class Skeleton3D:
    def __init__(self):
        self.scene = canvas(title="Esqueleto 3D", width=800, height=600)

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

        self.is_update_enabled = True

    def inverse_kinematics(self, target_positions):
        for joint_name, target_position in target_positions.items():
            if joint_name in self.joints:
                joint = self.joints[joint_name]
                if joint.min_angle is not None and joint.max_angle is not None:
                    delta_x = target_position.x - joint.position.x
                    delta_y = target_position.y - joint.position.y
                    target_angle = math.degrees(math.atan2(delta_y, delta_x))
                    target_angle = max(joint.min_angle, min(joint.max_angle, target_angle))
                    joint.sphere.rotate(angle=math.radians(target_angle), axis=vector(0, 0, 1), origin=joint.position)
                else:
                    joint.position = target_position


# Crear una instancia del esqueleto 3D
skeleton_3d = Skeleton3D()

# Posiciones objetivo para las articulaciones (ajusta según tus necesidades)
target_positions = {
    'LeftWrist': vector(1, 1, 0),
    'RightWrist': vector(-2, 0, 0),
    'LeftElbow': vector(-2, 1, -2),
    'RightElbow': vector(2, 2, 0),
    'LeftShoulder': vector(-1, 2, 0),
    'RightShoulder': vector(1, 2, 0),
    'Chest': vector(0, 2, 0),
    'Head': vector(2, 2.75, 3),
    'LeftAnkle': vector(-0.5, -4, 0),
    'RightAnkle': vector(0.5, -4, 0),
    'LeftKnee': vector(-0.5, -2, 0),
    'RightKnee': vector(0.5, -2, 0),
    'LeftHip': vector(-0.5, 0, 0),
    'RightHip': vector(0.5, 0, 0),
}

# Aplicar cinemática inversa para alcanzar las posiciones objetivo
skeleton_3d.inverse_kinematics(target_positions)
skeleton_3d.update(target_positions)

