from SimpleCV import Image
from features import Feature
from screenshot import screenshot
import time
from settings import PARAMS, REGION
def test(t,m,p):
    time.sleep(t)
    i=0
    bug = 0
    while i < m or m is None:
        path = 'test/'+str(bug)+'.png'
        screenshot(path, region=REGION)
        im = Image(path)
        f = Feature(im, **PARAMS)
        blobs = f.extract_blobs()
        if not blobs[0]:
            break
        if not blobs[1]:
            bug += 1

        blobs = [blob for blob in blobs if blob]

        f.show_blobs_on_image(blobs)
        time.sleep(p)
        i+=1

if __name__ == '__main__':
    test(0,None,0)
    print 'bird has died'
