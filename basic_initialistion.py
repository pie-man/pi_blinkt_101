#!/usr/bin/python

from time import sleep
from blinkt import set_pixel, show

def rotate(list,shift):
    return list[0 - shift:] + list[:0 - shift]

def show_state(state):
     for pixel in range(8):
        set_pixel(pixel, *state[pixel])
     show()

def cycle(times,states,sleep_time=1,gap=None):
    if gap is None:
        gap = states / 8
    for count in range(times):
        state = states[0::gap]
        show_state(state)
        print("{0:4d} : red = {1:3.2f} | green = {2:3.2f} | blue = {3:3.2f}"
                                            .format(count, *state[0]))
        sleep(sleep_time)
        states = rotate(states,1)
    return state

def chase(state, max_count=40, delay=1, style=1, bounce=7):
    direction = 1
    if style == 2:
        direction = -1
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
    return state
    
def turn_off():
    state = set_two_tone((0,0,0), split=8)
    show_state(state)
    return state

def set_two_tone(colour_a, colour_b=(0, 0, 0), split=1):
    state=[]
    for pixel in range(split):
        state.append(colour_a)
    for pixel in range(split,8):
        state.append(colour_b)
    return state

def kit_chase(colour, iterations=7, fade=5, delay=1, background=(0,0,0)):
    current_pixel = 0
    decrement = 1.0 / float(fade)
    level = [0.0 for x in range(8)]
    count = 0
    while count < iterations:
        if current_pixel == 0:
            step = 1
            count += 1
        if current_pixel == 7:
            step = -1
            count += 1
        level = [max(x - decrement, 0) for x in level]
        level[current_pixel] = 1.0
        for pixel in range(8):
           set_pixel(pixel, *colour, brightness=level[pixel])
        show()
        print("{0:1.2f} {1:1.2f} {2:1.2f} {3:1.2f} {4:1.2f} {5:1.2f} {6:1.2f} {7:1.2f}".format(*level))
        current_pixel += step
        sleep(delay)
    
red = ([x*2.125 for x in range(120)] +
       [255 - (x*2.125) for x in range(120)] +
       [0 for x in range(120)])
green = rotate(red, 120)
blue = rotate(green, 120)

red_pixel=(255, 0, 0)
grn_pixel=(0, 255, 0)
blu_pixel=(0, 0, 255)
ppl_pixel=(95, 0, 160)
blk_pixel=(0, 0, 0)

degrees = zip(red, green, blue)

colour_swatch = []
for pixel in range(8):
    loc = pixel * 45
    colour_swatch.append(degrees[loc])

state = cycle(360, degrees, .1, 20)

sleep(5)
turn_off()

state = chase(colour_swatch, 60, 0.1)
state = chase(colour_swatch, 60, 0.1, 2)
state = chase(colour_swatch, 60, 0.1, 3)
sleep(2)

state = set_two_tone(red_pixel)
state = chase(state, 63, 0.1, 3)
state = set_two_tone(grn_pixel)
state = chase(state, 63, 0.1, 3)
state = set_two_tone(blu_pixel, red_pixel)
state = chase(state, 63, 0.1, 3)
for build in range(2,8):
    state = set_two_tone(ppl_pixel, split=build)
    state = chase(state, (8-build)*4, 0.1, 3, 8-build)
for decline in range(2,8):
    state = set_two_tone(blk_pixel, ppl_pixel, split=decline)
    state = chase(state, (8-decline)*8, 0.1, 3, 8-decline)

sleep(3)
state = turn_off()
