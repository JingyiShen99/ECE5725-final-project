#write data 
#!/usr/bin/python

import RPi.GPIO as GPIO
import SimpleMFRC522    # 使用封装好的 RC522 功能

# 调用 SimpleMFRC522 的创建函数，然后将其作为对象存储到我们的 reader 变量中，以便稍后与之交互
reader = SimpleMFRC522.SimpleMFRC522()    

# try捕获运行中发生的异常
try:
    # 调用读卡器对象，告诉电路开始读取放置在 RC522 读卡器顶部的任何 RFID 卡片
    id, text = reader.read() 

    # 打印读取到的信息，包含卡片的 ID 和 存储在卡上的文本
    print(id)
    print(text)

# finally总在 try 语句后触发，即时抛出异常
finally:
    # 清除 GPIO 占用，防止其它程序不能正常使用引脚
    GPIO.cleanup()
