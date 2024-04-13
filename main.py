# import time

# import RPi.GPIO as GPIO

# from modules.video import capture_lane_video



# # Set GPIO mode and configure pins

# GPIO.setmode(GPIO.BCM)
# # 3
# # 5
# # 7
# # 11
# # 13
# # 15
# # 19
# # 21
# # 23
# # 29
# # 31
# # 33
# # 35
# # 37


# vehicle_count_x1 = 0
# vehicle_count_x2 = 0
# vehicle_count_y1 = 0
# vehicle_count_y2 = 0


# vehicle_counts: dict[str, int] = {
#     "vehicle_count_x1": vehicle_count_x1,
    
#     "vehicle_count_x2": vehicle_count_x2,
    

#     "vehicle_count_y1": vehicle_count_y1,
#     "vehicle_count_y2": vehicle_count_y2,
# }


# s = [vehicle_count_x1,  vehicle_count_y1, vehicle_count_x2, vehicle_count_y2] # lane_1, lane_2, lane_3, lane_4

# video_names = ['lane_1.mp4', 'lane_2.mp4', 'lane_3.mp4', 'lane_4.mp4']




# # the led light indicators
# ledRedX, ledYellowX, ledGreenX = 17, 27, 22
# ledRedY, ledYellowY, ledGreenY = 5, 6, 13 

# # the motor controller pins 
# IN1, IN2, IN3, IN4 = 23, 24, 25,8


# #  responsible to show the count down timer 
# SegmentPinAX, SegmentPinBX, SegmentPinCX, SegmentPinDX = 4, 14, 15, 18
# SegmentPinAY, SegmentPinBY, SegmentPinCY, SegmentPinDY = 12, 16, 20, 21



# #  responsible to show the count down timer
# multiplex1, multiplex2, multiplex3 = 2, 3, 4


# # def get_vehicles_count():
# #     global vehicle_count_x1, vehicle_count_x2, vehicle_count_y1, vehicle_count_y2
# #     for i in range(4):
# #        count = callLight(source=video_names[i])



# # Set GPIO mode and configure pins
# GPIO.setmode(GPIO.BCM)

# # set up leds
# for i in [ledRedX, ledYellowX, ledGreenX, ledRedY, ledYellowY, ledGreenY]:
#     GPIO.setup(i, GPIO.OUT)
# # setup stepper motor    
# GPIO.setup(IN1, GPIO.OUT)
# GPIO.setup(IN2, GPIO.OUT)
# GPIO.setup(IN3, GPIO.OUT)
# GPIO.setup(IN4, GPIO.OUT)

# # setup 7 segment display
# for i in [SegmentPinAX, SegmentPinBX, SegmentPinCX, SegmentPinDX, SegmentPinAY, SegmentPinBY, SegmentPinCY, SegmentPinDY]:
#     GPIO.setup(i, GPIO.OUT)


# # set up multiplexers
# for i in [multiplex1, multiplex2, multiplex3]:
#     GPIO.setup(i, GPIO.OUT)


# # lets set up the timer for the lightgett

# # Define constants
# DEG_PER_STEP = 1.8
# STEPS_PER_REVOLUTION = int(360 / DEG_PER_STEP)

# # Define sequence for 28BYJ-48 stepper motor
# seq = [
#     [1, 0, 0, 1],
#     [1, 0, 0, 0],
#     [1, 1, 0, 0],
#     [0, 1, 0, 0],
#     [0, 1, 1, 0],
#     [0, 0, 1, 0],
#     [0, 0, 1, 1],
#     [0, 0, 0, 1]
# ]

# # Function to rotate the stepper motor one step
# def step(delay, step_sequence):
#     for i in range(4):
#         GPIO.output(IN1, step_sequence[i][0])
#         GPIO.output(IN2, step_sequence[i][1])
#         GPIO.output(IN3, step_sequence[i][2])
#         GPIO.output(IN4, step_sequence[i][3])
#         time.sleep(delay)

# # Function to move the stepper motor one step forward and captures image as it progresses
# def step_forward(delay, steps):
#     for _ in range(steps):
#         capture_lane_video("1")
#         step(delay, seq[0])
#         capture_lane_video("2")
        
#         step(delay, seq[1])
#         capture_lane_video("3")
#         step(delay, seq[2])
#         capture_lane_video("4")
#         step(delay, seq[3])
        

# # Function to move the stepper motor one step backward
# def step_backward(delay, steps):
#     for _ in range(steps):
#         step(delay, seq[3])
#         step(delay, seq[2])
#         step(delay, seq[1])
#         step(delay, seq[0])

# try:
#     # Set the delay between steps
#     delay = 0.005

#     while True:
#         # Rotate one revolution forward (clockwise)
#         step_forward(delay, STEPS_PER_REVOLUTION)

#         # Pause for 2 seconds
#         time.sleep(2)

#         # Rotate one revolution backward (anticlockwise)
#         step_backward(delay, STEPS_PER_REVOLUTION)

#         # Pause for 2 seconds
#         time.sleep(2)

# except KeyboardInterrupt:
#     print("\nExiting the script.")

# finally:
#     # Clean up GPIO settings
#     GPIO.cleanup()




import time

from gpiozero import LED, Button, LEDBoard, Motor
from gpiozero.tools import zip_values

# from signal import pause
from modules.api_call import send_videos_to_api
from modules.video import capture_lane_video

# Define constants
DEG_PER_STEP = 1.8
STEPS_PER_REVOLUTION = int(360 / DEG_PER_STEP)

# # Define GPIO pins
# ledRedX, ledYellowX, ledGreenX = LED(17), LED(27), LED(22)
# ledRedY, ledYellowY, ledGreenY = LED(5), LED(6), LED(13)
# IN1, IN2, IN3, IN4 = Motor(23, 24), Motor(25, 8), None, None
# segmentDisplayX = LEDBoard(4, 14, 15, 18, 16, 20, 21, 12)
# segmentDisplayY = LEDBoard(12, 16, 20, 21, 4, 14, 15, 18)
# multiplex1, multiplex2, multiplex3 = LED(2), LED(3), LED(4)
# startButton = Button(26)

# # Define sequence for 28BYJ-48 stepper motor
# seq = [
#     (1, 0, 0, 1),
#     (1, 0, 0, 0),
#     (1, 1, 0, 0),
#     (0, 1, 0, 0),
#     (0, 1, 1, 0),
#     (0, 0, 1, 0),
#     (0, 0, 1, 1),
#     (0, 0, 0, 1)
# ]

# Function to rotate the stepper motor one step
def step(delay, step_sequence):
    for i in range(4):
        # IN1.value, IN2.value, IN3.value, IN4.value = step_sequence[i]
        time.sleep(delay)

# Function to move the stepper motor one step forward and captures image as it progresses
def step_forward(delay, steps):
    for _ in range(steps):
        capture_lane_video("1")
        # step(delay, seq[0])
        capture_lane_video("2")
        # step(delay, seq[1])
        capture_lane_video("3")
        # step(delay, seq[2])
        capture_lane_video("4")
        # step(delay, seq[3])



capture_lane_video("1")
capture_lane_video("2")
capture_lane_video("3")
capture_lane_video("4")
print("done saving")

video_files = {
  "x1": "lane_1.mp4",
  "x2": "lane_2.mp4",
  "y1": "lane_3.mp4",
  "y2": "lane_4.mp4"
}
print(send_videos_to_api(video_files))
# Function to move the stepper motor one step backward
def step_backward(delay, steps):
    for _ in range(steps):
        pass
        # step(delay, seq[3])
        # step(delay, seq[2])
        # step(delay, seq[1])
        # step(delay, seq[0])

try:
    # Set up LEDs
    # ledsX = [ledRedX, ledYellowX, ledGreenX]
    # ledsY = [ledRedY, ledYellowY, ledGreenY]

    # Set up multiplexers
    # multiplexers = [multiplex1, multiplex2, multiplex3]

    # Set up motors
    # motors = [IN1, IN2]

    # Set the delay between steps
    delay = 0.005

    # Create a function to handle button press event
    def start_button_pressed():
        # Rotate one revolution forward (clockwise)
        step_forward(delay, STEPS_PER_REVOLUTION)

        # Pause for 2 seconds
        time.sleep(2)

        # Rotate one revolution backward (anticlockwise)
        step_backward(delay, STEPS_PER_REVOLUTION)

        # Pause for 2 seconds
        time.sleep(2)

    # Assign the button press event handler
    # startButton.when_pressed = start_button_pressed

    # Keep the program running
    # pause()

except KeyboardInterrupt:
    print("\nExiting the script.")

finally:
    pass
    # Clean up GPIO settings
    # for led in ledsX + ledsY:
    #     led.close()
    # for mux in multiplexers:
    #     mux.close()
    # for motor in motors:
    #     motor.close()
    # startButton.close()
