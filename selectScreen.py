import PySimpleGUI as sg
from PIL import Image, ImageGrab, ImageDraw, ImageFont
import pygetwindow as gw
import io

# Function to capture a thumbnail of an active window
def capture_window(window_title):
    window = gw.getWindowsWithTitle(window_title)[0]
    
    if not window.isActive:  # Ensure the window is active
        window.activate()
    
    # Ensure the window is active before capturing
    if window.isActive:
        window.activate()
        bbox = window.left, window.top, window.right, window.bottom
        # screenshot = ImageGrab.grab(bbox)
        screenshot = ImageGrab.grab(bbox, include_layered_windows=False, all_screens=True)
        # screenshot.show()
        # input("Press Enter after closing the image to take the next screenshot or Ctrl+C to stop...")

        
        # Resize the screenshot to a thumbnail size
        thumbnail = screenshot.resize((200, 150))
        
        return thumbnail
    return None

# Function to bring a specific window to the front
def bring_window_to_front(window_title):
    window = gw.getWindowsWithTitle(window_title)[0]
    window.activate()

# Function to create a placeholder image with the text "No thumbnail was captured"
def create_placeholder_thumbnail():
    thumbnail = Image.new('RGB', (200, 150), color=(169, 169, 169))  # Gray background
    draw = ImageDraw.Draw(thumbnail)
    
    # Load a font and draw text on the placeholder image
    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()
    
    text = "No thumbnail captured"
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]  # Get the width and height of the text
    position = ((thumbnail.width - text_width) // 2, (thumbnail.height - text_height) // 2)
    draw.text(position, text, fill="black", font=font)
    
    return thumbnail

    
    
# Function to open the "Select Screen" window
def open_select_screen_window(main_window):
    window_list = gw.getAllTitles()  # Get all window titles
    layout = []
    
    for title in window_list:
        if title.strip() == '':
            continue  # Skip windows with no title
        
        thumbnail = capture_window(title)
        if not thumbnail:
            thumbnail = create_placeholder_thumbnail()  # Create a placeholder thumbnail
        
        # Convert the thumbnail to a format that PySimpleGUI can display
        bio = io.BytesIO()
        thumbnail.save(bio, format="PNG")
        thumbnail_data = bio.getvalue()
        
        # Create a button with the window title and thumbnail or placeholder
        layout.append([sg.Image(data=thumbnail_data), sg.Button(title, key=title)])
    
    if not layout:
        layout = [[sg.Text("No active windows found.")]]
    
    screen_window_layout = [
        [sg.Text("Select Screen To Track")],
        [sg.Column(layout, scrollable=True, size=(400, 400))],
        [sg.Button("Close")]
    ]
    
    screen_window = sg.Window("Select Screen", screen_window_layout, modal=True, size=(450, 500))
    
    while True:
        event, values = screen_window.read()
        if event in (sg.WIN_CLOSED, "Close"):
            break
        elif event in window_list:
            bring_window_to_front(event)  # Bring the clicked window to the front
            screen_window.close()
            return

    screen_window.close()
    
    # Bring the main window back to the front and activate it
    main_window.bring_to_front()  # Bring the main window to the front
    main_window.force_focus()  # Ensure the main window is activated and focused


# test code with layout
# # Main window layout
# layout = [
    # [sg.Button("Select File", size=(10, 1), button_color=('white', 'blue')),
     # sg.Button("Select Screen", size=(12, 1), button_color=('white', 'green'))],
    # [sg.Multiline(size=(60, 20), key='-OUTPUT-')],
    # [sg.Button("Exit", size=(8, 1)), sg.Button("Run", size=(8, 1))]
# ]

# # Create the main window
# window = sg.Window("Main Window", layout, size=(500, 450))

# # Main event loop
# while True:
    # event, values = window.read()
    
    # if event in (sg.WIN_CLOSED, "Exit"):
        # break
    # elif event == "Select Screen":
        # open_select_screen_window()

# window.close()
