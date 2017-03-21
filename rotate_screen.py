#!/usr/bin/env python
#
import os
import sys
import subprocess
import argparse

direction = 1
screens = ['left', 'normal', 'right', 'inverted']
state_file = '/home/ryan/src/python_scripts/.screen_state'

def get_state():
    """
    Function to read the current state from file.
    """
    return open(state_file,'r').readline().strip()

def set_state(curr_state):
    """
    Function to write the current state from file.
    """
    try:
        new_indx = (screens.index(curr_state) + direction) % len(screens)
        new_state = screens[new_indx]
    except ValueError as e:
        new_state = 'normal'
    
    with open(state_file,'w') as fh:
        fh.write(new_state)

    return new_state

def get_screen():
    """
    Function to make a system call to get the screen dimensions.
    """
    cmd = r"/usr/bin/xrandr -q | grep Screen | tr -d ',' | awk '{print $8,$10}'"
    w,h = [int(item) for item in subprocess.check_output(cmd,shell=True).split()]
    return (w,h)

def rotate_screen(ornt):
    """
    Function to rotate the screen to a given orientation.

    Parameters
    ----------
    ornt : Rotation position (left, right, normal, inverted)
    """

    if ornt in screens:
        cmd = "/usr/bin/xrandr -o %s"%ornt
        subprocess.call(cmd,shell=True)

if __name__ == '__main__':
    
    # arg to switch direction
    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--reverse', help='change direction',
                        action='store_true')
    args = parser.parse_args()
    if args.reverse:
        direction = -1

    # w,h = get_screen()
    # # Currently in normal, switch to left
    # if (w > h):
    #     rotate_screen('left')
    # # Currently in left mode, switch to normal
    # elif (w < h):
    #     rotate_screen('normal')
    curr_state = get_state()
    new_state = set_state(curr_state)
    rotate_screen(new_state)
