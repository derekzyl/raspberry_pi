import os

import cv2

# from picamera import PiCamera


def capture_lane_video(lane_name, duration=2, fps=10, fourcc='mp4v'):
  """
  Captures a video stream from the webcam for a specified duration and lane name,
  replacing the existing video for that lane if it exists.

  Args:
      lane_name (str): Name of the lane being captured.
      duration (int, optional): Duration of video capture in seconds. Defaults to 2.
      fps (int, optional): Frame rate of the video. Defaults to 20.
      fourcc (str, optional): Video codec (e.g., 'XVID', 'MJPG'). Defaults to 'XVID'.

  Returns:
      None
  """

  # Define video capture object
  cap = cv2.VideoCapture(0)
  # cap = PiCamera()  
  # cap.resolution = (640, 480) 


  # # Set frame width and height (optional, adjust if needed)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

  # Generate filename based on lane_name
  filename = f"lane_{lane_name}.mp4"

  # Check if video file already exists
  if os.path.exists(filename):
    print(f"Replacing existing video: {filename}")
    os.remove(filename)  # Remove existing video before capture

  # Define video writer settings
  out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*fourcc), fps, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

  # Start time for frame capture
  start_time = cv2.getTickCount()

  # Capture frames and write to video
  while True:
    ret, frame = cap.read()

    # Write frame to video
    if ret:
      out.write(frame)

    # Calculate elapsed time in seconds
    elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
    if elapsed_time >= duration:
      break

  # Release video capture and writer objects
  cap.release()
  out.release()

  print(f"Video saved successfully: {filename}")


# Example usage for four lanes (replace lane names as needed)
# lane_names = ["1", "2", "3", "4"]
# for lane_name in lane_names:
#   capture_lane_video(lane_name)


# import os
# from picamera import PiCamera
# from time import sleep

# def capture_lane_video(lane_name, duration=2, fps=10, format='h264'):
#     """
#     Captures a video stream from the Pi Camera for a specified duration and lane name,
#     replacing the existing video for that lane if it exists.

#     Args:
#         lane_name (str): Name of the lane being captured.
#         duration (int, optional): Duration of video capture in seconds. Defaults to 2.
#         fps (int, optional): Frame rate of the video. Defaults to 10.
#         format (str, optional): Video format (e.g., 'h264', 'mp4'). Defaults to 'h264'.

#     Returns:
#         None
#     """

#     # Initialize PiCamera
#     camera = PiCamera()
#     camera.resolution = (640, 480)  # Adjust resolution as needed
#     camera.framerate = fps

#     # Generate filename based on lane_name
#     filename = f"lane_{lane_name}.{format}"

#     # Check if video file already exists
#     if os.path.exists(filename):
#         print(f"Replacing existing video: {filename}")
#         os.remove(filename)  # Remove existing video before capture

#     # Start recording
#     camera.start_recording(filename)

#     # Record for specified duration
#     camera.wait_recording(duration)

#     # Stop recording
#     camera.stop_recording()

#     # Release PiCamera resources
#     camera.close()

#     print(f"Video saved successfully: {filename}")
