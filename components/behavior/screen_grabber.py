import logging
import time

log = logging.getLogger(__name__)
SHOT_DELAY = 1

try:
    import ImageChops
    import ImageGrab
    import ImageDraw
    HAVE_PIL = True
except:
    try:
        from PIL import ImageChops
        from PIL import ImageGrab
        from PIL import ImageDraw
        HAVE_PIL = True
    except:
        HAVE_PIL = False

def grabber():
        img_counter = 0
        while img_counter < 10:
            time.sleep(SHOT_DELAY)
            try:
                img_current = ImageGrab.grab()
            except IOError as e:
                log.error("Cannot take screenshot: %s", e)
                continue
            img_counter += 1
            # workaround as PIL can't write to the socket file object :(
            # tmpio = StringIO.StringIO()
            new_image_name = "puckoo_screen" + `img_counter` + ".jpg"
            img_current.save(new_image_name)

