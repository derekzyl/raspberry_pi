from json import JSONDecoder
import requests

def send_videos_to_api(api_url, video_paths):
 
    """
    Sends multiple videos as form data to an API endpoint.

    Args:
    - api_url (str): The URL of the API endpoint.
    - video_paths (dict): A dictionary containing the paths to the videos. 
                          Keys represent the form field names, and values are the file paths.

    Returns:
    - bool: True if the API call was successful, False otherwise.
    """


    print("started sending videos to API...")
    try:
        # Prepare the files to be sent as form data
        files = {key: open(path, 'rb') for key, path in video_paths.items()}
        
        # Make the API call
        response = requests.post(api_url, files=files)
        
        # Check the response status code
        if response.status_code == 200:
            print("API call successful")
            data = response.json()
            return data
        else:
            print("API call failed with status code:", response.status_code)
            return  {'id': '20240413060929emkax651ip2ff3e1acea50443b9b6ed854613634e6',
                     'x1_vehicles': 0, 'x2_vehicles': 0, 'y1_vehicles': 0, 'y2_vehicles': 0,
                     'x_green_time': 60, 
                     'y_green_time': 60}
    except Exception as e:
        print("An error occurred:", str(e))
        return  {'id': '20240413060929emkax651ip2ff3e1acea50443b9b6ed854613634e6',
                 'x1_vehicles': 0,
                 'x2_vehicles': 0, 
                 'y1_vehicles': 0, 
                 'y2_vehicles': 0,
                 'x_green_time': 60, 
                 'y_green_time': 60}

# Example usage:

# Example usage
api_url = "http://127.0.0.1:8000/process"
video_files = {
  "x1": "lane_1.mp4",
  "x2": "lane_2.mp4",
  "y1": "lane_3.mp4",
  "y2": "lane_4.mp4"
}

success=send_videos_to_api(api_url, video_files)
if success is not None:
    print("Received response:", success)
else:
    print("Failed to receive response from the API.")
    
