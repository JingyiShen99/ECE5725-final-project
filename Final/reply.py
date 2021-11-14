import telebot
import RPi.GPIO as GPIO
import time 

bot = telebot.TeleBot("2022892271:AAFua__pKYcbUQIhlOuwMKUZs-bWewbwDrY", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN


#----------------------------gpio part
GPIO.setup(26, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
led_pin = GPIO.PWM(26, 1)
led_pin.start(50)


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

bot.infinity_polling()
