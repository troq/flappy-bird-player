"""For extracting features from flappy bird game images"""

from SimpleCV import Image, DrawingLayer

class Feature(object):

    def __init__(self, image, resize_h, pipe_thresh_bin, min_pipe_size, pipe_thresh_x, 
                 bird_color, bird_thresh_bin, num_bird_dilate, min_bird_size, max_bird_size):
        """Used to handle features (bird x&y displacement from significan pipe) 
        of snappy bird game, after extraction, features stored as x_disp, y_disp
        THERE'S TOO MUCH FUNCTIONALITY IN THIS CLASS, WATEVER THO

        :image: simplecv image of flappy bird game
        :resize_h: height to resize image to, None if don't resize
        :pipe_thresh_bin: threshold used to binarize/separate pipes 
        :min_pipe_size: min blob area that matches pipes
        :pipe_thresh_x: x coord threshold to filter out too far left pipes
        :bird_color: color of flappy bird used to locate bird in image
        :bird_thresh_bin: threshold used to binarize/separate flappy bird 
        :min_bird_size: min blob area that matches bird
        :max_bird_size: max blob area that matches bird

        """
        if resize_h is not None:
            self.small = image.resize(h=resize_h)
        else:
            self.small = image
        self.color_channel   = self.small.colorDistance(bird_color)
        self.pipe_thresh_bin = pipe_thresh_bin
        self.min_pipe_size   = min_pipe_size
        self.pipe_thresh_x   = pipe_thresh_x
        self.bird_thresh_bin = bird_thresh_bin
        self.num_bird_dilate = num_bird_dilate
        self.max_bird_size   = max_bird_size
        self.min_bird_size   = min_bird_size

    def extract(self):
        """extracts bird x&y displacement from significant pipe from small image

        :returns: True if extraction successful (and sets x_disp, y_disp, bird_y), False if bird is dead

        """
        bird, pipe = self.extract_blobs()

        if bird is None:
            return False

        self.x_disp = bird.x-pipe.x
        self.y_disp = bird.y-pipe.y

        return True

    def extract_blobs(self):
        """extracts the bird blob and the significant pipe blob from small image

        :returns: bird blob (or None if dead), pipe blob

        """

        #extract bird needs to be first bc extract pipes needs self.bird_only
        return self.extract_bird(), self.extract_significant_pipe()

    def extract_bird(self):
        """extracts the bird blob

        :returns: bird blob or None if bird is dead

        """
        #makes the bird color stand out (as black) and binarizes it to make the bird white
        self.bird_only = self.color_channel.binarize(self.bird_thresh_bin).dilate(self.num_bird_dilate)

        blobs = self.bird_only.findBlobs()

        if not blobs: #if no bird is found (bird is dead)
            return None

        #the smallest blob is the bird (safeguard for if another blob was found somehow)
        return blobs[-1]
        

    def extract_significant_pipe(self):
        """returns significant pipe blob (the bottom left valid pipe)
        :returns: significant pipe blob or None if there is none
        """
        pipes = self.extract_pipes()
        if not pipes:
            return None
        pipes = pipes.filter(pipes.x() > self.pipe_thresh_x) #filters out pipes that are too far left
        pipes = pipes.sortX()
        pipes = pipes[:2] #there are 4 pipes, this gets the 2 leftmost pipes
        return max(pipes, key=lambda pipe: pipe.y) #gets the lowest pipe blob, resulting in the bottom-left pipe blob


    def extract_pipes(self):
        """extracts the pipe blobs from the image (determined by blob size)
        :returns: simplecv FeatureSet of pipe blobs or None if there are no pipes
        """
        pipes_only = (self.color_channel+self.bird_only).binarize(self.pipe_thresh_bin).dilate()

        pipes = pipes_only.findBlobs(minsize=self.min_pipe_size)
        return pipes[-4:] if pipes else None #the largest 4 are the pipes, None if no pipes

    def show_features(self):
        """shows bird/pipe blobs on image

        :returns: nothing

        """
        blobs = [blob for blob in self.extract_blobs() if blob]
        self.show_blobs_on_image(blobs)

    def show_blobs_on_image(self, blobs):
        """draws blobs onto the game image and shows it

        :blobs: list of blobs to draw on and show
        :returns: nothing

        """

        layer = DrawingLayer(self.small.size())

        for blob in blobs:
            blob.draw(layer=layer)

        self.small.addDrawingLayer(layer)

        self.small.show()
        self.small.clearLayers()
        

if __name__ == '__main__':
    params = {
        'resize_h'      : None,
        'min_pipe_size' : 400,
        'max_pipe_size' : 525,
        'pipe_thresh_x' : 75,
        'bird_color'    : (228,129,22),
        'min_bird_size' : 300,
        'max_bird_size' : 400,
    }
    for x in range(0,35):
        image = Image('flap/test'+str(x)+'.png')
        f = Feature(image, **params)
        f.show_features()
        raw_input()
