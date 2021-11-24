#!/usr/bin/python

import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

try:
    # 使用 raw_input 读入一个输入并存入 text 中
    text = raw_input('New data:')

    # 放置卡片
    print("Now place your tag to write")
    reader.write(text)
    print("Written")
finally:
    GPIO.cleanup()
