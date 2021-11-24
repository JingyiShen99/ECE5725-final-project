#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2019/8/6 16:19
# @FileName : entrance_guard.py
# @Author   : jiaye

import os

import RPi.GPIO as GPIO
import SimpleMFRC522

def opendoor():
    os.system("python /root/work_repository/RC522/open_door.py")

if __name__ == '__main__':
    reader = SimpleMFRC522.SimpleMFRC522()
    while(True):
        try:
            print ("Ready to read card")
            id, text = reader.read()
            print("Card id: ", id)

            if (id == 357306137218):
                # Open the door
                # opendoor()
                opendoor()
                print ("Door is opened")
            print(text)
        finally:
            GPIO.cleanup()
