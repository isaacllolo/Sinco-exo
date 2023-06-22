import sys
import os
import json
import logging
import bpy
import numpy as np
import socket
import requests
import time
import threading

sys.path.append(os.path.join(bpy.path.abspath("//"), "scripts"))

"""
@param bone: the bone object, obtained from armature.pose.bone["<bone_name>"]
@param rotation: rotation in quaternion (w, x, y, z)
"""
def setBoneRotation(bone, rotation):
    w, x, y, z = rotation
    bone.rotation_quaternion[0] = w
    bone.rotation_quaternion[1] = x
    bone.rotation_quaternion[2] = y
    bone.rotation_quaternion[3] = z

"""
a piece of math code copied from StackOverflow
https://stackoverflow.com/questions/39000758/how-to-multiply-two-quaternions-by-python-or-numpy

@param q1: in form (w, x, y, z)
@param q0: @see q1
"""
def multiplyQuaternion(q1, q0):
    w0, x0, y0, z0 = q0
    w1, x1, y1, z1 = q1
    return np.array([-x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0,
                     x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
                     -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0,
                     x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0], dtype=np.float64)
                     
MCU_IP = "192.168.137.48"  # IP del ESP8266
MCU_PORT = 8080  # Puerto de comunicación en el ESP8266
FPS = 60

# set up logging
logger = logging.getLogger("BPY")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setStream(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(name)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(ch)

# get scene armature object
armature = bpy.data.objects["Armature"]

# get the bones we need
bones = {
    "root": armature.pose.bones.get("Root"),
    "head": armature.pose.bones.get("J_Bip_Head"),
    "left_arm_upper": armature.pose.bones.get("J_Bip_L_UpperArm"),
    "left_arm_lower": armature.pose.bones.get("J_Bip_L_LowerArm"),
    "right_arm_upper": armature.pose.bones.get("J_Bip_R_UpperArm"),
    "right_arm_lower": armature.pose.bones.get("J_Bip_R_LowerArm"),
    "left_leg_upper": armature.pose.bones.get("J_Bip_L_UpperLeg"),
    "left_leg_lower": armature.pose.bones.get("J_Bip_L_LowerLeg"),
    "right_leg_upper": armature.pose.bones.get("J_Bip_R_UpperLeg"),
    "right_leg_lower": armature.pose.bones.get("J_Bip_R_LowerLeg"),
    "left_hand": armature.pose.bones.get("J_Bip_L_Hand"),
    "right_hand": armature.pose.bones.get("J_Bip_R_Hand")
}

       
## Establish a TCP connection with the ESP8266 over WiFi
#def connect_to_esp8266():
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.connect((MCU_IP, MCU_PORT))
#    return s

## Get the connection object
#esp8266_socket = connect_to_esp8266()

# Process the received data from Arduino
def process_received_data(buffer):
    print("set in to bone")
    print(buffer)
    for data in buffer:
        print(data)
        try:
            parsed_data = json.loads(data)
            print(parsed_data)
            if("gXHD" in parsed_data[0] and "gXCOD" in parsed_data[1]):
                bone_left_arm_upper = bones.get("left_arm_upper")
                q0= np.array([0,float(parsed_data[0]["gXHD"]), float(parsed_data[0]["gYHD"]), float(parsed_data[0]["gZHD"])])
                bone_left_arm_lower = bones.get("left_arm_lower")
                q1 = np.array([0,float(parsed_data[1]["gXCOD"]), float(parsed_data[1]["gYCOD"]), float(parsed_data[1]["gZCOD"])])
     
                # get inverse transformation of q0, the parent bone
                q0_inv = q0 * np.array([1, -1, -1, -1])
                
                # rotate child about parent, to get relative position of the child
                q1_rel = multiplyQuaternion(q0_inv, q1)
                
                # apply transformation
                setBoneRotation(bone_left_arm_upper, q0)
                setBoneRotation(bone_left_arm_lower, q1)
            
            if("gXMD" in parsed_data[2]):
                bone_left_hand = bones.get("left_hand")
                bone_left_hand.rotation_quaternion = [0, float(parsed_data[2]["gXMD"]), float(parsed_data[2]["gYMD"]), float(parsed_data[2]["gZMD"])]

            
            print("Received data from Arduino")
        except json.JSONDecodeError as e:
            print("Error decoding received data:", e)

## Continuously receive data from Arduino
def receive_from_esp8266():
    url = 'http://192.168.1.51/'

    while True:
        buffer=np.array([])
        try:
            for i in range(10):
                # Realizar la solicitud HTTP
                response = requests.get(url)
                response.raise_for_status()  # Comprobar si hubo algún error en la respuesta

                data = response.text
#                print(data)
                np.append(buffer,data)
                time.sleep(0.5)
            print("---------------------- 3 send data to bone 2---------------------------")
            process_received_data(buffer)  

        except requests.exceptions.RequestException as e:
            print('Error:')
            break

        # Pausa de 100 milisegundos
        time.sleep(10)

## ... remaining script code ...

if __name__ == "__main__":
    try:
        logger.info("Starting services.")
#        bpy.utils.register_class(ModalTimerOperator)
       
        # Start receiving data from Arduino in a separate thread
        receive_thread = threading.Thread(target=receive_from_esp8266 ,daemon=True)
        
        receive_thread.start()
        

       
     
        
       
        logger.info("All started.")
    except KeyboardInterrupt:
#        esp8266_socket.close()
        logger.info("Received KeyboardInterrupt, stopped.")