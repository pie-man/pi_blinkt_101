#!/usr/bin/python

from time import sleep
from blinkt import set_pixel, show

def rotate(list,shift):
    return list[shift:] + list[:shift]

def show_state(state):
     for pixel in range(8):
        set_pixel(pixel, *state[pixel])
     show()

def cycle(times,states,sleep_time=1,gap=1):
    for count in range(times):
        state = states[0::gap]
        show_state(state)
        print("{0:} : red = {1:} | green = {2:} | blue = {3:}"
                                            .format(count, *state[0]))
        sleep(sleep_time)
        states = rotate(states,1)

def chase(state, max_count=40, delay=1, style=1, bounce=7):
    direction = 1
    if style == 2 or style == 3:
    #if style == 2:
        direction = -1

    show_state(state)
    state = rotate(state, direction)
    count = 0
    
    while count <= max_count:
        count += 1
        show_state(state)
        state = rotate(state, direction)
        if style == 3 and (count % bounce) == 0:
            direction = 0 - direction
            print("count = {0:3d} : mod = {1:1d} : dir = {2:3d}".format(
                  count, count % bounce, direction))
        sleep(delay)
    
def turn_off():
    for pixel in range(8):
        set_pixel(pixel, 0, 0, 0)
    show()

def set_one_on(single_colour, background=(0, 0, 0)):
    state=[]
    state.append(single_colour)
    for pixel in range(1,8):
        state.append(background)
    return state

red = ([x*2.125 for x in range(120)] +
       [255 - (x*2.125) for x in range(120)] +
       [0 for x in range(120)])
green = rotate(red, 120)
blue = rotate(green, 120)

single_red=(255, 0, 0)
single_grn=(0, 255, 0)
single_blu=(0, 0, 255)
single_blk=(0, 0, 0)

degrees = zip(red, green, blue)

rainbow = []
for pixel in range(8):
    loc = pixel * 45
    rainbow.append(degrees[loc])

# cycle(360, degrees, .1, 20)
# 
# sleep(5)
# turn_off()
# 
# chase(rainbow, 60, 0.1)
# chase(rainbow, 60, 0.1, 2)
# chase(rainbow, 60, 0.1, 3)
# sleep(2)
# 
# state = set_one_on(single_red)
# chase(state, 63, 0.1, 3)
# state = set_one_on(single_grn)
# chase(state, 63, 0.1, 3)
state = set_one_on(single_blu, single_grn)
chase(state, 63, 0.1, 3)
state = [single_blk, single_blk, single_blk, single_blk,
         single_blk, single_blk, single_red, single_red]
chase(state, 60, 0.2, 3, 6)
sleep(3)
turn_off()
