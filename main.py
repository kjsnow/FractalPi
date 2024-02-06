from mandelbrot import Mandelbrot
from PIL import Image as im
import asyncio
import numpy as np
import glob
import sys
import time

# Set to the name of your e-ink device (https://github.com/robweber/omni-epd#displays-implemented)
DISPLAY_TYPE = "waveshare_epd.epd7in5_V2"

# Disable when running the waveshare panel
DEBUG = True

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


async def display_renders(epd, debug=False, sleep=10):
    for file in sorted(glob.glob("renders/*.jpg")):
        with im.open(file) as image:
            display_image(epd, image, debug)
            await asyncio.sleep(sleep)


# @asyncio.coroutine
async def render_images(epd, debug=False, save_render=False):
    render_iteration = 0
    while True:
        print('I am a strange loop')
        await asyncio.sleep(3)
    # for render_iteration in range(0, 10):
    #     print(f"Starting render {render_iteration}...")
    #     mandelbrot.render(WIDTH, HEIGHT)
    #     print("Done!")
    #     arr = mandelbrot.get_render()
    #     arr = (np.asarray(arr)*255).astype(np.uint8)
    #     image = im.fromarray(arr)
    #     # Save the image as BMP
    #     image = image.convert("1")
    #
    #     if save_render:
    #         # Save to results
    #         image.save(f"./renders/render_{render_iteration}.jpg")
    #
    #     display_image(epd, image, debug)
    #
    #     mandelbrot.zoom_on_interesting_area()
    #     render_iteration += 1




async def main():
    # 1 - THIS WORKS
    render = asyncio.create_task(render_images(epd, True, False))
    display = asyncio.create_task(display_renders(epd, debug=True, sleep=5))
    await render
    await display

    # 2
    # await asyncio.gather(render_images(epd, True, False), display_renders(epd, debug=True, sleep=5))


if __name__ == "__main__":
    epd = prepare_display(width=WIDTH, height=HEIGHT, debug=DEBUG)

    # render_images(epd, debug=DEBUG, save_render=False)
    # display_renders(epd, DEBUG, 10)

    asyncio.run(main())
