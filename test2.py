from SimpleCV import Image
from features import Features
from settings import PARAMS
def test():
    f = Features(**PARAMS)
    for i in range(300,400):
        path = 'test/'+str(i)+'.png'
        im = Image(path)
        f.set_image(im)
        f.extract_blobs()

if __name__ == '__main__':
    test()
