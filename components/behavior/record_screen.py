import math

import logging
import StringIO
import threading
import time

# import puckoo.components.behavior.record_screen
# import behavior.record_screen
#import record_screen
#__import__(record_screen.Screenshot)

log = logging.getLogger(__name__)


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

class Screenshot:
    """Get screenshots."""

    def _draw_rectangle(self, img, xy):
        """Draw a black rectangle.
        @param img: PIL Image object
        @param xy: Coordinates as refined in PIL rectangle() doc
        @return: Image with black rectangle
        """
        dr = ImageDraw.Draw(img)
        dr.rectangle(xy, fill="black", outline="black")
        return img

    def have_pil(self):
        """Is Python Image Library installed?
        @return: installed status.
        """
        return HAVE_PIL

    def equal(self, img1, img2, skip_area=None):
        """Compares two screenshots using Root-Mean-Square Difference (RMS).
        @param img1: screenshot to compare.
        @param img2: screenshot to compare.
        @return: equal status.
        """
        if not HAVE_PIL:
            return None

        # Trick to avoid getting a lot of screen shots only because the time in the windows
        # clock is changed.
        # We draw a black rectangle on the coordinates where the clock is locates, and then
        # run the comparison.
        # NOTE: the coordinates are changing with VM screen resolution.
        if skip_area:
            # Copying objects to draw in another object.
            img1 = img1.copy()
            img2 = img2.copy()
            # Draw a rectangle to cover windows clock.
            for img in (img1, img2):
                self._draw_rectangle(img, skip_area)

        # To get a measure of how similar two images are, we use
        # root-mean-square (RMS). If the images are exactly identical,
        # this value is zero.
        diff = ImageChops.difference(img1, img2)
        h = diff.histogram()
        sq = (value * ((idx % 256)**2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares/float(img1.size[0] * img1.size[1]))

        # Might need to tweak the threshold.
        return rms < 8

    def take(self):
        """Take a screenshot.
        @return: screenshot or None.
        """
        if not HAVE_PIL:
            return None

        return ImageGrab.grab()


# Copyright (C) 2012-2013 Claudio Guarnieri.
# Copyright (C) 2014-2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

SHOT_DELAY = 1

# Skip the following area when comparing screen shots.
# Example for 800x600 screen resolution.
# SKIP_AREA = ((735, 575), (790, 595))
SKIP_AREA = None

class Screenshots(threading.Thread):
    """Take screenshots."""

    def __init__(self, options={}, analyzer=None):
        threading.Thread.__init__(self)
        # Auxiliary.__init__(self, options, analyzer)
        self.do_run = True

    def stop(self):
        """Stop screenshotting."""
        self.do_run = False

    def run(self):
        """Run screenshotting.
        @return: operation status.
        """
        if "screenshots" in self.options:
            self.do_run = int(self.options["screenshots"])

        scr = Screenshot()

        # TODO We should also send the action "pillow" so that the Web
        # Interface can adequately inform the user about this missing library.
        if not scr.have_pil():
            log.info(
                "Python Image Library (either PIL or Pillow) is not "
                "installed, screenshots are disabled."
            )
            return False

        img_counter = 0
        img_last = None

        while self.do_run:
            time.sleep(SHOT_DELAY)

            try:
                img_current = scr.take()
            except IOError as e:
                log.error("Cannot take screenshot: %s", e)
                continue

            if img_last and scr.equal(img_last, img_current, SKIP_AREA):
                continue

            img_counter += 1

            # workaround as PIL can't write to the socket file object :(
            tmpio = StringIO.StringIO()
            img_current.save(tmpio, format="JPEG")
            tmpio.seek(0)

            # # now upload to host from the StringIO
            # nf = NetlogFile()
            # nf.init("shots/%04d.jpg" % img_counter)
            #
            # for chunk in tmpio:
            #     nf.sock.sendall(chunk)
            #
            # nf.close()

            img_last = img_current

        return True
