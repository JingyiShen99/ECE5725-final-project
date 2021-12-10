import telebot
import RPi.GPIO as GPIO
import time 
from PIL import Image
import os
from collections import defaultdict
from pygame import mixer
import threading

bot = telebot.TeleBot("2022892271:AAFua__pKYcbUQIhlOuwMKUZs-bWewbwDrY", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

result_list = [][4]
local_result_list = []
carrier_list = ["Fedex", "DHL", "Food"]
list_pointer = 0

mixer.init()
play_flag = False

#-----paths--------------------------------
result_storage_path = ""
image_name = label_stamp + ".jpg"
output_path = "" +label_stamp

#----------------------------gpio part
GPIO.setup(26, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
led_pin = GPIO.PWM(26, 1)
led_pin.start(50)

#TODO: setup pass code
def get_date_taken(path):
    return Image.open(path)._getexif()[36867]

#---------------------------gpio init operation
GPIO.setup(26, GPIO.OUT)
led_pin = GPIO.PWM(26, 1)
led_pin.start(50)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Welcome to the ultimate control panel.")

@bot.message_handler(commands=['苟利国家生死以', '膜蛤'])
def send_welcome(message):
	bot.reply_to(message, "岂因祸福避趋之")


@bot.message_handler(commands=['alarm'])
def send_welcome(message):
        bot.reply_to(message, "alarm will be triggered")
        threading.Thread(target = emergency_alarm).start
        while(play_flag):
            usr_in = 1
            usr_in = 100
            led_pin.ChangeFrequency(int(usr_in))
            time.sleep(0.5)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

@bot.message_handler(commands=['latest delivery'])
def get_delivery_status(message):
	log_request(message, 0)

@bot.message_handler(commands=['history'])
def get_history(message):
	log_request(message, 1)


threading.Thread(target = bot.infinity_polling()).start()


#-----load delivery handlers--------------------------------
def log_request(path, complete_flag):
    global list_pointer


    box = []
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r') as f:  # open in readonly mode
            i = 0
            j = 0
            local_result_list = []
            searchlines = f.readlines()
            image_path = searchlines[0].split(':')[0]
            predictions_num = int(searchlines[1]) - 1
            for i in range(predictions_num):
                box = searchlines[1 + 1 + i].split(',')
                i += 1
            for j in range(predictions_num):
                print(searchlines[2 + i + 1 + j])
                print(2 + i + 1 + j)
                local_result_list.append(str(searchlines[2 + i + 1 + j].split(':')[0]))
                if complete_flag:
                    if local_result_list[j] == 'fedex':
                        result_list[image_path].append("fedex")
                    elif local_result_list[j] == 'dhl':
                        result_list[image_path].append("dhl")
                    elif local_result_list[j] == 'ups':
                        result_list[image_path].append("ups")
                    elif local_result_list[j] == 'food delivery':
                        result_list[image_path].append("food")
                    list_pointer += 1
                else:

                    print(box)
                j += 1
        list_pointer += 1
        print(image_path)
        print(result_list)
            
    f.close()
	
# /home/pi/Downloads/3.jpeg: Predicted in 0.970428 seconds.
# 2
# Box 0, 0.686100, 0.433947, 0.482435 ,0.397016
# Box 1, 0.705939, 0.436732, 0.403356 ,0.375360
# ups: 89%

def check_bounding_boxes(box_list):
	#TODO: check bounding boxes functions
	pass

def emergency_alarm():
	# Remember the current and previous button states
	current_state = True
	prev_state = True
	global play_flag
	# Load the sounds
	sound = mixer.Sound('applause-1.wav')

	# If button is pushed, light up LED
	while play_flag:
		if (current_state == False) and (prev_state == True):
			sound.play()
		time.sleep(10)
		play_flag = False

def retrieve_images(time_list):
	#TODO: send back lastest image
	pass

def detection(result_storage_path, image_name, output_path):
    #TODO: trigger sensor and detections
    os.system('cd /darknet-nnpack/ && ./darknet detector test cfg/yolov3-tiny.cfg yolov3-tiny.weights {0}/{1} > {2}'.format(result_storage_path, image_name, output_path)) 

