### Source code from: https://www.willmcgugan.com/blog/tech/post/opengl-sample-code-for-pygame/

import os
from DvsSimulator import *
from EnvironmentSimulator import *
from CamControl import *

SCREEN_SIZE = (128, 128)

def winresize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def sysinit():
    ### Set window's location
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,300)

    pygame.display.set_mode(
        SCREEN_SIZE, HWSURFACE | OPENGL | DOUBLEBUF)
    winresize(*SCREEN_SIZE)
    
    pygame.init()
    glEnable(GL_DEPTH_TEST)

    glShadeModel(GL_FLAT)
    glClearColor(1.0, 1.0, 1.0, 0.0)

    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLight(GL_LIGHT0, GL_POSITION, (0, 1, 1, 0))

    glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
    glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))



def main():
    
    ### System initialization
    sysinit()

    ### Create object for rendering the environment
    envsim = EnvironmentSimulator()

    ### Create object for controlling the camera
    camctrl = CamControl()

    counter = 1 
    
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYUP and event.key == K_ESCAPE:
                exit()

        ### Clear the screen, and z-buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        ### Move the camera and get matrix of camera pose
        camera_matrix = camctrl .getviewmat_keymouseCtrl()
        
        ### Upload the inverse camera matrix to OpenGL
        glLoadMatrixd(camera_matrix.ravel())

        ### Light must be transformed as well
        glLight(GL_LIGHT0, GL_POSITION, (0, 1.5, 1, 0))

        ### Render the environment
        envsim.render(False)

        ### Show the screen
        pygame.display.flip()

        ### Get rendered image
        gray_img = envsim.getRenderImages(*SCREEN_SIZE)

        if counter == 2:
            ### Initialize DVS simulator
            dvssim = DvsSimulator(0, gray_img, 0.5)
            events = []

        elif counter > 2:
            timestamp = float(counter) / 1000.
            
            cur_events = dvssim.update(timestamp, gray_img)
            print(counter, timestamp, len(cur_events))

            cur_events = sorted(cur_events, key=lambda e: e[3])
            events += cur_events
            memim = np.ones((SCREEN_SIZE[1],SCREEN_SIZE[0],3))
            if cur_events:
                cur_events = np.array(cur_events)
                memim[cur_events[:, 1].astype(int), cur_events[:, 0].astype(int), 2*cur_events[:, 2].astype(int)] -= 1
                memim[cur_events[:, 1].astype(int), cur_events[:, 0].astype(int), 1] -= 1
            cv2.imshow('Events', cv2.flip(memim, 0))


        counter += 1

if __name__ == '__main__':
    main()