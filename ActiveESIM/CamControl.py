import pygame
from pygame.locals import *
from pyrr import Vector3, Matrix44, vector, vector3
from math import sin, cos, radians
import cv2

class CamControl:
    
    def __init__(self):
        self.camera_pos = Vector3([0.0, 0.0, 0.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 0.5
        self.velocity = 0.05
        self.yaw = 0.0
        self.pitch = 0.0
        
        self.lastX = 64
        self.lastY = 64

    ### Use keys to control the camera translation,
    ### Use mouse to control the camera rotation.
    def getviewmat_keymouseCtrl(self):
        pressedkey = pygame.key.get_pressed()
        mousepos = pygame.mouse.get_pos()
        self.process_key_movement(pressedkey)
        self.process_mouse_movement(mousepos)
        return self.look_at()

    ### Use keys to control the camera translation,
    ### The input commands control the camera rotation.
    def getviewmat_keyTranslationCtrl(self, yawcmd, pitchcmd):
        pressedkey = pygame.key.get_pressed()
        self.process_key_movement(pressedkey)

        self.yaw = yawcmd
        self.pitch = pitchcmd
        self.update_camera_vectors()
        return self.look_at()

    ### The camera position is fixed at the origin,
    ### The input commands control the camera rotation.
    def getviewmat_CmdCtrl(self, yawcmd, pitchcmd):
        self.yaw = yawcmd
        self.pitch = pitchcmd
        self.update_camera_vectors()
        return self.look_at()

    def process_key_movement(self,pressedkey):
        if pressedkey[K_w]:
            self.camera_pos += self.camera_front * self.velocity
        if pressedkey[K_s]:
            self.camera_pos -= self.camera_front * self.velocity
        if pressedkey[K_d]:
            self.camera_pos += self.camera_right * self.velocity
        if pressedkey[K_a]:
            self.camera_pos -= self.camera_right * self.velocity
        if pressedkey[K_q]:
            self.camera_pos += self.camera_up * self.velocity
        if pressedkey[K_e]:
            self.camera_pos -= self.camera_up * self.velocity


    def process_mouse_movement(self, mousepos):

        xpos = mousepos[0]
        ypos = mousepos[1]
        # print(xpos, ypos)

        self.yaw = (xpos - self.lastX)*self.mouse_sensitivity
        self.pitch = (self.lastY - ypos)*self.mouse_sensitivity

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.yaw)) * cos(radians(self.pitch))

        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_front))

    def look_at(self):
        position = self.camera_pos
        target = self.camera_pos + self.camera_front
        world_up = self.camera_up

        # 1.Position = known
        # 2.Calculate cameraDirection
        zaxis = vector.normalise(position - target)
        # 3.Get positive right axis vector
        xaxis = vector.normalise(vector3.cross(vector.normalise(world_up), zaxis))
        # 4.Calculate the camera up vector
        yaxis = vector3.cross(zaxis, xaxis)

        # create translation and rotation matrix
        translation = Matrix44.identity()
        translation[3][0] = -position.x
        translation[3][1] = -position.y
        translation[3][2] = -position.z

        rotation = Matrix44.identity()
        rotation[0][0] = xaxis[0]
        rotation[1][0] = xaxis[1]
        rotation[2][0] = xaxis[2]
        rotation[0][1] = yaxis[0]
        rotation[1][1] = yaxis[1]
        rotation[2][1] = yaxis[2]
        rotation[0][2] = zaxis[0]
        rotation[1][2] = zaxis[1]
        rotation[2][2] = zaxis[2]

        return rotation * translation