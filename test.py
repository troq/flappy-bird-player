from SimpleCV import Image
from features import Features
from screenshot import screenshot
import time
from settings import PARAMS, REGION
def test():
    while True:
        path = 'test/tmp.png'
        screenshot(path, region=REGION)
        im = Image(path)
        f = Features(im, **PARAMS)
        blobs = f.extract_blobs()
        if not blobs[0]:
            break

        blobs = [blob for blob in blobs if blob]

        f.show_blobs_on_image(blobs)

if __name__ == '__main__':
    test()
    print 'bird has died'
