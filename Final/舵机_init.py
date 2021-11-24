#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import signal
import atexit

if __name__ == '__main__':
    atexit.register(GPIO.cleanup)
    servopin = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servopin, GPIO.OUT, initial=False)

    # 创建 PWM 实例
    # channel: servopin, frequency: 50HZ
    p = GPIO.PWM(servopin, 50)  

    # 更改频率，freq 为设置的新频率，单位为 Hz
    # p.ChangeFrequency(freq)   

    # 启用 PWM
    p.start(0)      
    # time.sleep(2)

    for i in range(0, 181, 10):
        # 更改占空比
        p.ChangeDutyCycle(2.5 + 10 * i / 180)  # 设置转动角度
        time.sleep(0.02)  # 等该20ms周期结束
        p.ChangeDutyCycle(0)  # 归零信号
            # time.sleep(2)

    print ("Opening door")

    time.sleep(1)

    for i in range(181, 0, -10):
        p.ChangeDutyCycle(2.5 + 10 * i / 180)
        time.sleep(0.02)
        p.ChangeDutyCycle(0)
           # time.sleep(0.2)
