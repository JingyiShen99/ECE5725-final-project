# Wed Lab2
from pygame.locals import *
import RPi.GPIO as GPIO
import pygame
import os
# Global Flag
CODERUN = True
START_GAME = False
# Environment Seting
os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') #
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
# Init Pygame
pygame.init()
pygame.mouse.set_visible(False)
size = (width, height) = (320, 240)
screen = pygame.display.set_mode(size)
WHITE = 255,255,255
BLACK = 0,0,0
screen.fill(BLACK)
button_font = pygame.font.Font(None, 30)
touch_info_font = pygame.font.Font(None, 30)
# GPIO Setting
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN,pull_up_down = GPIO.PUD_UP)
def GPIO17_callback(channel):
    global CODERUN
    print("Quit by Bail-out button!!!")
    CODERUN = False
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)

pressed_positions_list = []

#game info
speed_big = [1,1] 
ball_big = pygame.image.load("/home/pi/Downloads/wc06.png")
ballrect_big = ball_big.get_rect()
ballrect_big.center = (198,100)
ball_big_radius = 64

# Small Ball
speed_small = [-2,-2] 
ball_small = pygame.image.load("/home/pi/Downloads/ball.png")
ballrect_small = ball_small.get_rect()
ballrect_small.center = (100,100)
ball_small_radius = 24

def check_quit_button_press(position):
    x,y = position
    # Check if the position is in the button area
    if y < 230 and y > 170:
        if x < 280 and x > 200:
            global CODERUN
            print("Quit!!!")
            CODERUN = False

def refresh_touch_info(position):
    pressed_positions_list.append(position)
    x, y = position
    touch_position_info = "touch at " + str(x) + ", " + str(y)
    touch_info = touch_info_font.render(touch_position_info, True, WHITE)
    touch_info_rect = text_surface.get_rect(center=(150,100))
    screen.blit(touch_info, touch_rect)

def check_start_button_press(position):
    global START_GAME
    x,y = position
    if x < 90 and y > 70:
        if x > 30 and y < 130:
            START_GAME = True


def check_colliderect():
    dx = abs(ballrect_big.centerx - ballrect_small.centerx)
    dy = abs(ballrect_big.centery - ballrect_small.centery)
    if( dx < (ball_big_radius + ball_small_radius - 30) and dy < (ball_big_radius + ball_small_radius - 25)):
        return True
    else:
        return False

def game_start():
    if (START_GAME):
        global ballrect_big, ballrect_small
        ballrect_big = ballrect_big.move(speed_big)    
        if ballrect_big.left < 0 or ballrect_big.right > width:        
            speed_big[0] = -speed_big[0]    
        if ballrect_big.top < 0 or ballrect_big.bottom > 200:        
            speed_big[1] = -speed_big[1]

        ballrect_small= ballrect_small.move(speed_small)    
        if ballrect_small.left < 0 or ballrect_small.right > width:        
            speed_small[0] = -speed_small[0]    
        if ballrect_small.top < 0 or ballrect_small.bottom > 200:        
            speed_small[1] = -speed_small[1]

        if check_colliderect():
            speed_big[0] = - speed_big[0]
            speed_big[1] = - speed_big[1]
            speed_small[0] = - speed_small[0]
            speed_small[1] = - speed_small[1]

def refresh_game(touch_position):
    #render buttons
    text_surface = button_font.render('Quit', True, WHITE)
    rect = text_surface.get_rect(center=(240, 200))
    screen.blit(text_surface, rect)
    #start button
    text_surface_start = button_font.render('Start', True, WHITE)
    rect_start = text_surface.get_rect(center=(60, 200))
    screen.blit(text_surface, rect_start)

    touch_info = touch_info_font.render('Touch at', True, WHITE)
    touch_rect = text_surface.get_rect(center= (150, 100))
    screen.blit(touch_info, touch_rect)   







if __name__ == "__main__":
    text_surface = button_font.render('Quit', True, WHITE)
    # Get Width and Height
    # print(text_surface.get_width())  # 63
    # print(text_surface.get_height()) # 38
    rect = text_surface.get_rect(center=(240, 200))
    screen.blit(text_surface, rect)
    #start button
    text_surface_start = button_font.render('Start', True, WHITE)
    rect_start = text_surface.get_rect(center=(60, 200))
    screen.blit(text_surface, rect_start)

    touch_info = touch_info_font.render('Touch at', True, WHITE)
    touch_rect = text_surface.get_rect(center= (150, 100))
    screen.blit(touch_info, touch_rect)
    pygame.display.flip()
    pos_String = "No Touch"

    screen.blit(ball_big, ballrect_big)
    screen.blit(ball_small, ballrect_small) 
    pygame.display.flip()

    #while quit button not pressed
    while CODERUN:
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                # touch_position = pygame.mouse.get_pos()
                # print(touch_position)
                pass
            #on mouse press
            elif(event.type is MOUSEBUTTONUP):
                touch_position = pygame.mouse.get_pos()
                print(touch_position)
                pressed_positions_list.append(touch_position)
                check_quit_button_press(touch_position)
                check_start_button_press(touch_position)
                # screen.fill(BLACK)
                # refresh_touch_info(touch_position)
                # screen.blit(text_surface, rect)
                # pygame.display.flip()
        game_start()

