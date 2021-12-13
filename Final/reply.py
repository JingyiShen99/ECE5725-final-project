import telebot
import RPi.GPIO as GPIO
import time 
from PIL import Image
import os
from collections import defaultdict
from pygame import mixer
import threading
from picamera import PiCamera
from pad4pi import rpi_gpio


bot = telebot.TeleBot("2022892271:AAFua__pKYcbUQIhlOuwMKUZs-bWewbwDrY", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

result_list = defaultdict(list)
carrier_list = ["Fedex", "DHL", "Food"]
list_pointer = 0

mixer.init()
play_flag = True

#-----------------------------lablel init
label_stamp = 100

#-----paths--------------------------------
result_storage_path = "/home/pi/PiImage/"
image_name = str(label_stamp) + ".jpg"
output_path = "/home/pi/PiImage/OutTxt/"
output_directory = "/home/pi/PiImage/OutTxt/"

#----------------------------gpio part

#----------------------------movement sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

#----------------------------hall
GPIO.setwarnings(False)
GPIO.setup( 20, GPIO.IN)

#----------------------------camera init
camera = PiCamera()
camera.resolution = (3280, 2464)

#---------------------------pygame initialization
mixer.init()
mixer.music.load("/home/pi/good_alarm.mp3")

#TODO: setup pass code
def get_date_taken(path):
    return Image.open(path)._getexif()[36867]

#---------------------------gpio init operation
GPIO.setup(26, GPIO.OUT)
led_pin = GPIO.PWM(26, 1)
led_pin.start(50)


#------------------------pin pad setup
# Setup Keypad
KEYPAD =[["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["0","F","E","D"]]
password = "5725"
res = 1
# same as calling: factory.create_4_by_4_keypad, still we put here fyi:
ROW_PINS = [22,27,17,21] # BCM numbering; Board numbering is: 7,8,10,11 (see pinout.xyz/)
COL_PINS = [26,19,6,5] # BCM numbering; Board numbering is: 12,13,15,16 (see pinout.xyz/)

factory = rpi_gpio.KeypadFactory()

# Try keypad = factory.create_4_by_3_keypad() or 
# Try keypad = factory.create_4_by_4_keypad() #for reasonable defaults
# or define your own:
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

class KeyStore:
    def __init__(self, message):
        #list to store them
        self.pressed_keys =''
        self.message = message

    #function to clear string
    def clear_keys(self):
        self.pressed_keys = self.pressed_keys.replace(self.pressed_keys,'')

    def store_key(self,key):
        global res
        global password
        if key=='D':
            #printing the sequence of keys.
            if self.pressed_keys == password:
              print("right password, the door is opened, please enter!")
              bot.reply_to(self.message, "The mechanics have entered")
              return 100
            else:
              if res>=3:
                bot.reply_to(self.message, "Potential risk of unknown personel trying to enter")
                print("wrong password for 3 times, please contact the administrator")
                password = "sdsg"
                return 101
              else:
                print("wrong password, please try again! (it is the "+ str(res)+" try)")
              res += 1
            self.clear_keys()
        else:
            self.pressed_keys += key


def pin_pad_input():
    pass


#-----load delivery handlers--------------------------------
def log_request(path, complete_flag):
    global list_pointer
    result_list.clear()
    box = []
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r') as f:  # open in readonly mode
            i = 0
            j = 0
            local_result_list = []
            # if os.path.join(path, filename).getsize == 0:
            #     break
            searchlines = f.readlines()
            if len(searchlines) is 0:
                continue 
            last_line = searchlines[-1]
            image_path = searchlines[0].split(':')[0]
            print(image_path)

            if searchlines[1] != 0:
                predictions_num = int(searchlines[1]) - 1
                for i in range(predictions_num):
                    box = searchlines[1 + 1 + i].split(',')
                    i += 1
                for j in range(predictions_num):
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
                        return local_result_list
                    if searchlines[2 + i + 1 + j] is last_line:
                        break
                    j += 1

        list_pointer += 1
        print(result_list)

    if complete_flag:
        return result_list
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
	current_state = False
	prev_state = True
	global play_flag
	# Load the sounds

	# If button is pushed, light up LED
	while play_flag:
            if (current_state == False) and (prev_state == True):
                mixer.music.play()
                current_state = True


		# time.sleep(10)
		# play_flag = False

def open_door(message):
    #key oeprations
    keys = KeyStore(message)

    # store_key will be called each time a keypad button is pressed
    status_code = keypad.registerKeyPressHandler(keys.store_key)

def retrieve_images(time_list):
	#TODO: send back lastest image
	pass

def detection():
    global label_stamp
    global output_path
    global image_name
    #TODO: trigger sensor and detections
    while True:
        if GPIO.input(4):
            image_name = str(label_stamp) + ".jpg"
            camera.capture(result_storage_path + image_name)
            output_path_full = output_path + str(label_stamp) + ".txt"
            os.system('cd /home/pi/darknet-nnpack/ && ./darknet detector test weight/t.data cfg/yolov3tiny_custom_trained.cfg weight/t.weights {0}{1} > {2}'.format(result_storage_path, image_name, output_path_full))
            label_stamp += 1
            time.sleep(5)



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Welcome to the ultimate control panel.")

@bot.message_handler(commands=['苟利国家生死以', '膜蛤'])
def send_welcome(message):
	bot.reply_to(message, "岂因祸福避趋之")

@bot.message_handler(commands=['alarm'])
def send_welcome(message):
        bot.reply_to(message, "door open process will be triggered")
        status_code = open_door(message)

        # while(play_flag):
        #     usr_in = 1
        #     usr_in = 100
        #     led_pin.ChangeFrequency(int(usr_in))
        #     time.sleep(0.5)


@bot.message_handler(commands=['latest'])
def get_delivery_status(message):
        result_list_reply = log_request(output_directory, 0)
        if result_list_reply is None:
            bot.reply_to(message, "There are no logs currently")
            return 0
        bot.reply_to(message, result_list_reply)

@bot.message_handler(commands=['history'])
def get_history(message):
        empty_message = 0
        result_list_reply = (log_request(output_directory, 1))
        if result_list_reply is None:
            empty_message = 1
            bot.reply_to(message, "There are no logs currently")
            return 0
        reply_list = ''.join(str(e) for e in str(list(result_list_reply.values())))
        print(result_list)
        bot.reply_to(message, reply_list)

@bot.message_handler(commands=['door'])
def get_door(message):
        door_staus = sensorCallback(sensor_channel)
        if door_staus:
            bot.reply_to(message, 'The  door is closed!!!')
        else:
            bot.reply_to(message, 'The door is open!!!')

@bot.message_handler(commands=['food'])
def get_food(message):
        if(GPIO.input(20) == False):
            bot.reply_to(message, "There are food delivery on shelf")
        else:
            bot.reply_to(message, "Food Lot is Empty")
            

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

class DetectionThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            detection()

class ReplyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        bot.infinity_polling()

thread1 = DetectionThread()
thread2 = ReplyThread()

thread1.start()
thread2.start()