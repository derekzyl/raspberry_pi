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
from threading import Thread

from gpiozero import LED, Motor, OutputDevice

from modules.api_call import send_videos_to_api
from modules.video import capture_lane_video

# Define constants
DEG_PER_STEP = 1.8
STEPS_PER_REVOLUTION = int(360 / DEG_PER_STEP)

# Define GPIO pins for the O
motor = Motor(forward=14, backward=15)

IN1, IN2, IN3, IN4 = OutputDevice(23),  OutputDevice(24), OutputDevice(25),  OutputDevice(8)

# Define GPIO pins for the LEDs
ledRedX, ledYellowX, ledGreenX = LED(17), LED(27), LED(22)
ledRedY, ledYellowY, ledGreenY = LED(5), LED(6), LED(13)

# # Define sequence for 28BYJ-48 stepper motor
seq = [
    (1, 0, 0, 1),
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 0, 0, 1)
]
delay =6
# Function to rotate the stepper motor one step
def step(delay, step_sequence:tuple):


        

# Function to move the stepper motor one step backward
    IN1.value = step_sequence[0]
    IN2.value = step_sequence[1]
    IN3.value = step_sequence[2]
    IN4.value = step_sequence[3]

                
  

        
        # GPIO.output(IN1, step_sequence[i][0])
        # GPIO.output(IN2, step_sequence[i][1])
        # GPIO.output(IN3, step_sequence[i][2])
        # GPIO.output(IN4, step_sequence[i][3])
        
       
    time.sleep(delay)

# Function to move the stepper motor one step forward
def step_forward(delay, steps):
    for _ in range(steps):
        capture_lane_video("1")
        step(delay, seq[0])
        capture_lane_video("2")
        step(delay, seq[1])
        capture_lane_video("3")
        step(delay, seq[2])
        capture_lane_video("4")
        step(delay, seq[3])

# Function to move the stepper motor one step backward
def step_backward(delay, steps):
    for _ in range(steps):
        capture_lane_video("1")
        step(delay, seq[3])
        capture_lane_video("2")
        step(delay, seq[2])
        capture_lane_video("3")
        step(delay, seq[1])
        capture_lane_video("4")
        step(delay, seq[0])

# Function to capture and send videos to the server for updated timing information
# def capture_and_send_videos():
#     while True:
#         # Capture videos
#         step_backward(delay, STEPS_PER_REVOLUTION)
#         video_files = {
#             "x1": "lane_1.mp4",
#             "x2": "lane_2.mp4",
#             "y1": "lane_3.mp4",
#             "y2": "lane_4.mp4"
#         }
#         # Send videos to the server
#         data = send_videos_to_api(video_files)
#         # Adjust timing parameters based on received information
#         x_green_time = data["x_green_time"]
#         y_green_time = data["y_green_time"]
#         y_red_time = x_green_time - 5
#         x_red_time = y_green_time - 5

# Create a thread to capture and send videos
# capture_thread = Thread(target=capture_and_send_videos)
# capture_thread.daemon = True
# capture_thread.start()

try:
    while True:
        # Step 1: Capture videos from all lanes sequentially
        step_forward(delay, STEPS_PER_REVOLUTION)

        # Step 2: Send the captured videos to the server for processing
        video_files = {
            "x1": "lane_1.mp4",
            "x2": "lane_2.mp4",
            "y1": "lane_3.mp4",
            "y2": "lane_4.mp4"
        }
        data = send_videos_to_api(video_files)

        # Step 3: Adjust timing parameters based on received information
        x_green_time = data["x_green_time"]
        y_green_time = data["y_green_time"]
        y_red_time = x_green_time - 5
        x_red_time = y_green_time - 5

        # Step 4: Turn on LEDs according to the timing information
        ledGreenX.on()
        ledRedY.on()
        time.sleep(x_green_time - 20)  # Wait for x_green_time - 20 seconds
        ledGreenX.off()
        ledYellowX.on()
        time.sleep(5)  # Wait for 5 seconds
        ledYellowX.off()
        ledRedX.on()
        time.sleep(85)  # Wait for 85 seconds
        ledRedX.off()
        ledYellowY.on()
        time.sleep(5)  # Wait for 5 seconds
        ledYellowY.off()
        ledGreenY.on()
        time.sleep(y_green_time - 15)  # Wait for y_green_time - 15 seconds
        ledGreenY.off()

except KeyboardInterrupt:
    print("\nExiting the script.")
