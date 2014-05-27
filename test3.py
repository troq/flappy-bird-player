from SimpleCV import Image, DrawingLayer, Color
from features import Features
from screenshot import screenshot
from settings import PARAMS, REGION
def test():
    f = Features(**PARAMS)
    minx,maxx = 0,0
    miny,maxy = 0,0
    while True:
        path = 'test/tmp.png'
        screenshot(path, region=REGION)
        im = Image(path)
        f.set_image(im)
        blobs = f.extract_blobs()
        if not blobs[0]:
            break
        dl = f.small.dl()
        bottom_right_corner = blobs[0].bottomRightCorner()
        dl.circle(bottom_right_corner, 5, Color.RED)
        if blobs[1]:
            top_right = blobs[1].topRightCorner()
            x = bottom_right_corner[0] - top_right[0]
            y = bottom_right_corner[1] - top_right[1]
            if x < minx:
                minx = x
            elif x > maxx:
                maxx = x
            if y < miny:
                miny = y
            elif y > maxy:
                maxy = y
            dl.circle(top_right, 5, Color.RED)
        f.small.show()
    print 'minx, maxx', minx, maxx
    print 'miny, maxy', miny, maxy

if __name__ == '__main__':
    test()
    print 'bird has died'
