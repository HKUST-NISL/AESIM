# Active Event Camera Simulator
[![AESIM](pictures/video_screenshot.jpg)](https://youtu.be/1CFUxxfl1Hs)

An active event camera simulator based on [DAVIS simulator](https://github.com/uzh-rpg/rpg_davis_simulator) and [ESIM](https://github.com/uzh-rpg/rpg_esim)

## Features
* Active control of 6DOF camera
* Allow keyboard and mouse to control the camera
* Allow dynamic 3D environment

## Prerequisites

Install the following libraries:

```
pip3 intall numpy pygame PyOpenGL pyrr opencv-python
```

## Running the demo

```
python Demo_AESIM_KeyMouseControl
```

## Acknowledgments

We modified our code based on [Learn OpenGL](https://learnopengl.com/) tutorials in our OpenGL rendering engine.
The display and control part is done by using [Pygame](https://www.pygame.org)
AESIM generates the simulated event data from rendered images. The code of this part is modified from the [DAVIS simulator](https://github.com/uzh-rpg/rpg_davis_simulator).
