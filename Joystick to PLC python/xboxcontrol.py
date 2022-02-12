import pygame
import pyads
import numpy as np
from datetime import datetime
from datetime import timedelta as td

#enter your plc program name and DUT name here
programVariable = 'run.controller'

#enter your plc AMS NET ID here, use pyads.PORT_TC2PLC1 for twincat 2
PLC_AMS = '5.37.99.176.1.1'
plc = pyads.Connection(PLC_AMS, pyads.PORT_TC3PLC1)
plc.open()
print("Connected?:",plc.is_open)
print("Local address:",plc.get_local_address())
print(plc.read_state())

def euc(joystick : list):
    radsq = 0
    for i in (joystick[0], joystick[1]):
        radsq += i**2

    rad = np.sqrt(radsq)
    return rad

holdtime = datetime.now()

pygame.init()
joysticks = []
clock = pygame.time.Clock()
keepPlaying = True
leftStick = [0,0,0]
rightStick = [0,0,0]

# for al the connected joysticks
for i in range(0, pygame.joystick.get_count()):
    # create an Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    # initialize them all (-1 means loop forever)
    joysticks[-1].init()
    # print a statement telling what the name of the controller is
    print ("Detected joystick "),joysticks[-1].get_name(),"'"
while keepPlaying:
    clock.tick(60)
    for event in pygame.event.get():
        # The 0 button is the 'a' button, 1 is the 'b' button, 2 is the 'x' button, 3 is the 'y' button
        # if event.button == 0:
        #     print ("A Has Been Pressed")
        if event.type == 1538 or event.type == 1540:
            if event.type == 1538:
                if event.value[0] != 0:
                    if event.value[0] == 1:
                        print('dpad right')
                        plc.write_by_name(programVariable + ".bDpadRight", True)
                    elif event.value[0] == -1:
                        print('dpad left')
                        plc.write_by_name(programVariable + ".bDpadLeft", True)
                if event.value[1] != 0:
                    if event.value[1] == 1:
                        print('dpad up')
                        plc.write_by_name(programVariable + ".bDpadUp", True)
                    elif event.value[1] == -1:
                        print('dpad down')
                        plc.write_by_name(programVariable + ".bDpadDown", True)
                elif [event.value[0],event.value[1]] == [0,0]:
                    print('dpad released')
                    for i in ['up', 'down', 'left', 'right']:
                        plc.write_by_name(programVariable + f".bDpad{i}", False)
            if event.type == 1540:
                if event.button == 0:
                    plc.write_by_name(programVariable + ".bAbtn", not plc.read_by_name(programVariable + ".bAbtn"))
                    print('A key pressed')
                if event.button == 1:
                    plc.write_by_name(programVariable + ".bBbtn", not plc.read_by_name(programVariable + ".bBbtn"))
                    print('B key pressed')
                if event.button == 3:
                    plc.write_by_name(programVariable + ".bXbtn", not plc.read_by_name(programVariable + ".bXbtn"))
                    print('X key pressed')
                if event.button == 4:
                    plc.write_by_name(programVariable + ".bYbtn", not plc.read_by_name(programVariable + ".bYbtn"))
                    print('Y key pressed')
        if event.type == 1536:
            if event.axis in (0,1,2):
                leftStick[event.axis] = event.value
            if event.axis in (3,4,5):
                rightStick[event.axis-3] = event.value
            plc.write_by_name(programVariable + ".leftStick", leftStick)
            plc.write_by_name(programVariable + ".rightStick", rightStick)