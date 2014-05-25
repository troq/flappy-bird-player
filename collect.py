from features import Features
import numpy as np
#screenshot
import gtk.gdk as g
import Image
import time
#log 
from evdev import InputDevice, ecodes
from select import select

#in vm, top left is (58,140), bottom right is (378, 516), so w = 320, h=376

def f(t,width,height):
    time.sleep(t)
    w = g.get_default_root_window()
    sz = (width,height)
    pb = g.Pixbuf(g.COLORSPACE_RGB, False, 8,*sz)
    cm = w.get_colormap()
    pb = pb.get_from_drawable(w,cm,58,141,0,0,*sz)
    im = Image(pb.get_pixels_array()) #creates simplecv image from pixbuf
    return im
im.show()
data = []

#log 
device = InputDevice('/dev/input/event5')

skip = 0

m = 10
i = 0

X = np.zeros([m,2], dtype='int16')
y = np.zeros(m, dtype='bool')

for event in device.read_loop():
    if i == m:
        break
    if event.type == ecodes.BTN_MOUSE && event.value == 1 && skip <= 0: #mousedown
        pb = pb.get_from_drawable(w,cm,58,140,0,0,*sz)
        im = Image(pb.get_pixels_array()) #creates simplecv image from pixbuf
        click = True
        f = Features(im, click)
        extracted = f.extract()
        if not extracted:
            skip = 4
        else:
            X[i] = [f.x_disp, f.y_disp]
            y[i] = f.click
            i += 1
        skip -= 1
