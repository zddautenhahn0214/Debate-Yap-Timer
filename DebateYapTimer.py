# Importing Image and ImageGrab module from PIL package  
from PIL import Image, ImageGrab 
import numpy as np
import time
import cv2


# takes a screen shot and crops to speicifed coordiantes
# If the green discord border color to indicate that person is talking appears in a suffiecnt amount
# then the time for that person starts. Once its got it turns off. Totals how long they speak for
#requires name, x, y, width, and height 
def discord_yap_track(coord_data):
    """
    returns a list of users and their data:
    users = [user = {
        "name": data['name'],
        "xStart": data['x'],
        "yStart": data['y'],
        "xEnd": data['x'] + data['width'],
        "yEnd": data['y'] + data['height'],
        "isTalking": False,
        "talkingTime": 0.0,
        "img": ""
    },]
    """
    print(coord_data)
    discord_talking_color = np.array([35, 165, 89])  # RGB color to detect if a user is talking
    # threshold for acceptable color varience
    threshold = 30
    # min req pixels to count them as talking 
    # increase this if that color is present and you can't draw around it
    minPixels = 0
    
    # max time the tracker will run for(seconds).
    # Set to -1 or lower if you want it to run forever
    maxTime = 10

    users = []  # List to hold user data dynamically
    
    for data in coord_data:
        user = {
            "name": data['name'],
            "xStart": data['x'],
            "yStart": data['y'],
            "xEnd": data['x'] + data['width'],
            "yEnd": data['y'] + data['height'],
            "isTalking": False,
            "talkingTime": 0.0,
            "img": ""
        }
        users.append(user)


    width = 795
    height = 447
    # track how long code takes
    codet0 = time.time()

    active_users = {}
    totalCodeTime = 0
    while totalCodeTime < maxTime:
        # get screen shots of each person in call/user list
        # Capture the entire screen
        full_screen = ImageGrab.grab()
        # img.show() 

        for user in users:
            # Define the bounding box for each user (xStart, yStart, xEnd, yEnd)
            bbox = (user["xStart"], user["yStart"], user["xEnd"], user["yEnd"])
            
            # Crop the specific section from the full-screen image
            user["img"] = full_screen.crop(bbox)
            
            # Calculate the difference between each pixel and the target color
            diff = np.linalg.norm(user["img"] - discord_talking_color, axis=-1)
            num_pixels = np.sum(diff <= threshold)
            # print(user['name'], num_pixels)
            # print()

            # Consider the user speaking if green pixels are above a certain minimum
            if num_pixels > 0:
                isTalking = True
            else:
                isTalking = False
         
            if isTalking:
                if user["name"] not in active_users:
                    active_users[user["name"]] = time.time()
            else:
                if user["name"] in active_users:
                    speaking_duration = time.time() - active_users.pop(user["name"])
                    user["talkingTime"] += speaking_duration
                    print(f'{user["name"]} spoke for:\t{speaking_duration}')


        # code_block
        codet1 = time.time()
        totalCodeTime = codet1-codet0

    print()
    # get last talk time if ended while talking for each user
    for user in users:
        if user["name"] in active_users:
            speaking_duration = time.time() - active_users.pop(user["name"])
            user["talkingTime"] += speaking_duration
        print(f'{user["name"]} spoke for a total of:\t{round(user["talkingTime"], 2)} seconds')
            
    print("totalCodeTime: ", totalCodeTime)
    
    return users



def edgeDetect():
    """
    Returns List of JSONs:
    [{
        "name": user_name,
        "x": x,
        "y": y,
        "width": w,
        "height": h
    }]
    """
    #inform user how to close screen
    print("Press 'q' to close window")
    
    # Capture the screen
    screen = np.array(ImageGrab.grab())

    # Convert to grayscale
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Find contours which should correspond to user frames
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Set thresholds for filtering contours
    min_width, min_height = 100, 100  # Minimum size for a user frame
    max_width, max_height = screen.shape[1] * 0.9, screen.shape[0] * 0.9  # Exclude near full-screen contours
    aspect_ratio_target = 16 / 9  # Target aspect ratio for video feeds

    bounding_boxes = []
    user_count = 1  # Start the user count at 1

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # Calculate the aspect ratio of the contour
        aspect_ratio = w / float(h)

        # Filter contours that are rectangular (allowing for typical camera feed shapes)
        if min_width < w < max_width and min_height < h < max_height and (aspect_ratio_target-0.5 < aspect_ratio < aspect_ratio_target+0.5):
            # Assign a user name
            user_name = f"User{user_count}"
            user_count += 1  # Increment the user count
            
            # Append bounding box coordinates and the name to the list
            bounding_boxes.append({
                "name": user_name,
                "x": x,
                "y": y,
                "width": w,
                "height": h
            })

            # Draw bounding box around the detected user frame
            cv2.rectangle(screen, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Put the user name inside the bounding box
            cv2.putText(screen, user_name, (x + 5, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Optional: Display the result for visual verification
    # Create a named window before displaying it
    cv2.namedWindow('Detected User Frames', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Detected User Frames', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Detected User Frames', screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return bounding_boxes


# Initialize global variables to store the bounding box coordinates and the current mouse position
bounding_boxes = []
start_point = None
drawing = False
last_update_time = 0  # To limit update frequency

def draw_rectangle(event, x, y, flags, param):
    global start_point, drawing, bounding_boxes, last_update_time
    screenName = 'Manual Bounding Box'
    update_interval = 0.016  # Update every 16 ms (~60 fps)

    # When the left mouse button is pressed down, record the starting point and start drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        drawing = True

    # If the right mouse button is pressed, cancel the current drawing
    elif event == cv2.EVENT_RBUTTONDOWN:
        if drawing:
            drawing = False
            # Optionally, redraw the original image without the rectangle
            cv2.imshow(screenName, param)

    # When the mouse is moved and drawing is in progress, update the rectangle
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            current_time = time.time()
            if current_time - last_update_time >= update_interval:  # Throttle updates to ~60 FPS
                last_update_time = current_time
                temp_image = param.copy()
                cv2.rectangle(temp_image, start_point, (x, y), (0, 255, 0), 2)
                cv2.imshow(screenName, temp_image)

    # When the left mouse button is released, stop drawing and save the rectangle coordinates
    elif event == cv2.EVENT_LBUTTONUP:
        if drawing:
            drawing = False
            end_point = (x, y)
            user_name = f"User{len(bounding_boxes) + 1}"

            # Determine the top-left and bottom-right corners of the rectangle
            top_left = (min(start_point[0], end_point[0]), min(start_point[1], end_point[1]))
            bottom_right = (max(start_point[0], end_point[0]), max(start_point[1], end_point[1]))

            bounding_boxes.append({
                "name": user_name,
                "x": top_left[0],
                "y": top_left[1],
                "width": bottom_right[0] - top_left[0],
                "height": bottom_right[1] - top_left[1]
            })

            # Draw the final rectangle
            cv2.rectangle(param, top_left, bottom_right, (0, 255, 0), 2)
            
            # Position the text in the top-left corner of the rectangle
            text_position = (top_left[0] + 5, top_left[1] + 25)
            
            # Draw the user name inside the rectangle
            cv2.putText(param, user_name, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display the updated image
            cv2.imshow(screenName, param)

def manual_bounding_boxes():
    """
    Returns List of JSONs:
    [{
        "name": user_name,
        "x": x,
        "y": y,
        "width": w,
        "height": h
    }]
    """
    print("Press 'q' when done drawing borders")
    print("Right click to cancel current box")
    #rest the boxes each time this method is called
    global bounding_boxes
    bounding_boxes = []
    
    screenName = 'Manual Bounding Box'
    # Capture the screen
    screen = np.array(ImageGrab.grab())

    # Create a named window before displaying it
    cv2.namedWindow(screenName, cv2.WINDOW_NORMAL)
    #make window full screen
    cv2.setWindowProperty(screenName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    # Display the screen capture for drawing bounding boxes
    cv2.imshow(screenName, screen)
    
    # Set the mouse callback function to draw rectangles
    cv2.setMouseCallback(screenName, draw_rectangle, screen)

    # Wait until the user presses the 'q' key to finish drawing and close the window
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

    return bounding_boxes


# this should be replaced by the UI, this same logic should happen when the 'run' button is pushed
def yapTimer():
    # edgeDetect()
    #auto detect the edges, works sometimes. Will show the generated boxes, if bad use manual mode
    bounding_boxes = edgeDetect()
    goodBorder = ""
    while goodBorder != 'y' and goodBorder != 'n':
        goodBorder = input("Were those borders good?(y/n)")
    if goodBorder == 'n':
        #manually set user tlaking boxes, make sure to include discord's green highlight
        bounding_boxes = manual_bounding_boxes()
    print(bounding_boxes)
    for bbox in bounding_boxes:
        print(f"{bbox['name']} | x: {bbox['x']}, y: {bbox['y']}, width: {bbox['width']}, height: {bbox['height']}")

    discord_yap_track(bounding_boxes)

    

if __name__ == '__main__':
    yapTimer()
