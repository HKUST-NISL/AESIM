import pygame
import numpy as np
from OpenGL.GLU import *
from OpenGL.GL import *
import cv2
import graphics

from DvsSimulator import *

class EnvironmentSimulator:
    
    def __init__(self):

        self.surface_ground = graphics.load_texture("objects/textures/brick.jpg")
        self.ground = graphics.ObjLoader("objects/plane.txt")

        glTranslatef(1, 0, 0)
        glRotatef(-90, 0, 1, 0)
        self.ground.render_texture(self.surface_ground, ((0,0),(1,0),(1,1),(0,1)))

    def render(self, ChangeTextureFlag):

        if ChangeTextureFlag:
            self.surface_ground = graphics.load_texture("objects/textures/brick.jpg")

        glTranslatef(1, 0, 0)  
        glRotatef(-90, 0, 1, 0)
        self.ground.render_texture(self.surface_ground, ((0,0),(1,0),(1,1),(0,1)))

        
        # glTranslatef(-7.5,2,0)
        # glRotatef(self.cube_angle, 0, 1, 0)

    def getRenderImages(self, width, height):
        data = glReadPixels(0, 0, width, height, GL_RGB, GL_FLOAT)
        arr = np.fromstring(data, dtype="float32", count=width*height*3)
        arr = arr.reshape((height, width, 3))

        R_raw = glReadPixels(0, 0, width, height, GL_RED, GL_FLOAT)
        G_raw = glReadPixels(0, 0, width, height, GL_GREEN, GL_FLOAT)
        B_raw = glReadPixels(0, 0, width, height, GL_BLUE, GL_FLOAT)

        R_img0 = np.fromstring(R_raw, dtype="float32", count=width*height)
        G_img0 = np.fromstring(G_raw, dtype="float32", count=width*height)
        B_img0 = np.fromstring(B_raw, dtype="float32", count=width*height)
        R_img = R_img0.reshape((height, width))
        G_img = G_img0.reshape((height, width))
        B_img = B_img0.reshape((height, width))

        rgb_img = cv2.merge([B_img, G_img, R_img])
        gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)

        return gray_img