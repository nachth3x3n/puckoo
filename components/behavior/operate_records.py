

import logging
import StringIO
import threading
import time

# import puckoo.components.behavior.record_screen
# import behavior.record_screen
import record_screen
__import__(record_screen.Screenshot)

log = logging.getLogger(__name__)

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