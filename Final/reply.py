import telebot
import RPi.GPIO as GPIO
import time 
from PIL import Image


bot = telebot.TeleBot("2022892271:AAFua__pKYcbUQIhlOuwMKUZs-bWewbwDrY", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

result_list = [][4]
carrier_list = ["Fedex", "DHL", "Food"]

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
		while(1):
			usr_in = 1
			usr_in = 100
			led_pin.ChangeFrequency(int(usr_in))
			time.sleep(0.5)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

@bot.message_handler(commands=['delivery'])
def get_delivery_status(message):
	log_request(message)


bot.infinity_polling()

#-----load delivery handlers--------------------------------
#/home/pi/Downloads/3.jpeg: Predicted in 0.970428 seconds.
# 2
# Box 0, 0.686100, 0.433947, 0.482435 ,0.397016
# Box 1, 0.705939, 0.436732, 0.403356 ,0.375360
# ups: 89%
def log_request(message):
	f = open("file.txt", "r")
	searchlines = f.readlines()
	f.close() 
	for i, line in enumerate(searchlines):
		if "searchphrase" in line: 
			for l in searchlines[i:i+3]:
				result_list[l][0] = searchlines[i]
				if searchlines[i + 1] is carrier_list[0]:
					result_list[l][1] = 1
				elif searchlines[i + 1] is carrier_list[1]:
					result_list[l][2] =	1
				elif searchlines[i + 1] is carrier_list[2]:
					#TODO: check bounding boxes
					pass

def check_bounding_boxes(box_list):
	#TODO: check bounding boxes functions
	pass

def emergency_alarm():
	#TODO: triggered
	pass

def retrieve_images(time_list):

