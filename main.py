from mandelbrot import Mandelbrot
from PIL import Image as im
import numpy as np
import glob
import sys
import time

# Set to the name of your e-ink device (https://github.com/robweber/omni-epd#displays-implemented)
DISPLAY_TYPE = "waveshare_epd.epd7in5_V2"

# Disable when running the waveshare panel
DEBUG = False

if not DEBUG:
    from omni_epd import displayfactory, EPDNotFoundError

mandelbrot = Mandelbrot()

# default height and width - need to hardcode for debug mode
WIDTH = 800
HEIGHT = 480


def prepare_display(width=800, height=480, debug=False):
    if not debug:
        try:
            epd = displayfactory.load_display_driver(DISPLAY_TYPE)
        except EPDNotFoundError:
            print(f"Couldn't find {DISPLAY_TYPE}")
            sys.exit()

        width = epd.width
        height = epd.height

        epd.prepare()
        epd.clear()
        epd.sleep()
        return epd


def display_image(epd, image, debug=False):
    if debug:
        image.show()
    else:
        epd.prepare()
        epd.clear()
        epd.display(image)
        epd.sleep()


def display_renders(epd, debug=False, sleep=10):
    for file in sorted(glob.glob("renders/*.jpg")):
        with im.open(file) as image:
            display_image(epd, image, debug)
            time.sleep(sleep)


def render_images():
    for render_iteration in range(0,9):
        print(f"Starting render {render_iteration}...")
        mandelbrot.render(WIDTH,HEIGHT)
        print("Done!")
        arr = mandelbrot.get_render()
        arr = (np.asarray(arr)*255).astype(np.uint8)
        image = im.fromarray(arr)
        # Save the image as BMP
        image = image.convert("1")

        # Save to results
        image.save(f"./renders/render_{render_iteration}.jpg")

        if DEBUG:
            image.show()
        else:
            epd.prepare()
            epd.clear()
            epd.display(image)
            epd.sleep()

        mandelbrot.zoom_on_interesting_area()
        render_iteration += 1


if __name__ == "__main__":
    epd = prepare_display(width=WIDTH, height=HEIGHT, debug=DEBUG)

    # render_iteration = 0
    while True:
        display_renders(epd, DEBUG, 10)
