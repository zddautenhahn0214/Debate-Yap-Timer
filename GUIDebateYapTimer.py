import PySimpleGUI as sg
import random
from DebateYapTimer import yapTimer, edgeDetect, manual_bounding_boxes, discord_yap_track
from selectScreen import open_select_screen_window, bring_window_to_front, capture_window


# Function to handle button presses with logging
def handle_button_press(button_name, window):
    # # This is the normal print that comes with simple GUI
    # sg.Print('Re-routing the stdout', do_not_reroute_stdout=False)

    # # this is clobbering the print command, and replacing it with sg's Print()
    # print = sg.Print

    # # this will now output to the sg display.
    # print('This is a normal print that has been re-routed.')

    if button_name == 'Run':
        # window['-OUTPUT-']('')
        update_log("Running Yap Timer", window)
        update_log("Press 'q' to close windows that will open in fullscreen", window)
        open_select_screen_window(window)
        bounding_boxes = edgeDetect()
        # Confirm with user if the auto detected boxes work
        if sg.popup_yes_no('Do those borders work?') == 'No':
            #manually set user tlaking boxes, make sure to include discord's green highlight
            bounding_boxes = manual_bounding_boxes()
        
        # Confirm with user to start tracking
        if sg.popup_yes_no('Start Yap Tracking?') == 'Yes':
            userTimes = discord_yap_track(bounding_boxes)
            for user in userTimes:
                update_log(f"{user['name']} spoke for {round(user['talkingTime'], 2)} seconds", window)
            sg.popup('Yap Tracking Completed!', keep_on_top=True)
        else:
            update_log("Yap Tracking cancelled", window)
            
        update_log("", window)

# Function to update the log output
def update_log(log_text, window):
    window['-OUTPUT-'].update(log_text + '\n', append=True)

# List of themes to cycle through
themes = sg.theme_list()  # Get all available themes 
current_theme_index = 8  # 8 is DarkAmber

# Function to open theme selection window
def open_theme_selector(main_window):
    # Initial layout for theme selector window
    layout = [
        [sg.Text('Search Theme:'), sg.InputText('', key='-SEARCH-', enable_events=True)],
        [sg.Listbox(values=themes, size=(30, 20), key='-THEME_LIST-', enable_events=True)],
        [sg.Button('Preview Theme', key='-PREVIEW-', tooltip="Preview the selected theme"), sg.Button('Pick Random Theme', key='-PICK_RANDOM_THEME-', tooltip="Pick a random GUI theme")],
        [sg.Button('Apply Theme', key='-APPLY-', tooltip="Apply the selected theme"), sg.Button('Cancel', key='-CANCEL-', tooltip="Cancel theme selection")]
    ]

    window = sg.Window('Theme Selector', layout, modal=True)

    filtered_themes = themes.copy()  # Start with full list of themes

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == '-CANCEL-':
            break

        # Filter the theme list based on the search input
        if event == '-SEARCH-':
            search_term = values['-SEARCH-'].lower()
            filtered_themes = [theme for theme in themes if search_term in theme.lower()]
            window['-THEME_LIST-'].update(filtered_themes)

        # Preview the selected theme
        if event == '-PREVIEW-':
            selected_theme = values['-THEME_LIST-'][0] if values['-THEME_LIST-'] else None
            if selected_theme:
                sg.theme(selected_theme)
                preview_layout = [
                    [sg.Text(f'Preview of Theme: {selected_theme}', justification='center')],
                    [sg.Text('This is a sample preview text.', size=(40, 1))],
                    [sg.Button('Close Preview', key='-CLOSE_PREVIEW-')]
                ]
                preview_window = sg.Window(f'Preview: {selected_theme}', preview_layout, modal=True, finalize=True)
                preview_window.read(close=True)
                
        # Change to a random theme
        if event == '-PICK_RANDOM_THEME-':
            selected_theme = random.randint(0, len(themes) - 1)
            window['-THEME_LIST-'].update(set_to_index=[selected_theme], scroll_to_index=selected_theme)


        # Apply the selected theme
        if event == '-APPLY-':
            selected_theme = values['-THEME_LIST-'][0] if values['-THEME_LIST-'] else None
            if selected_theme:
                sg.theme(selected_theme)
                main_window.close()  # Close main window to apply new theme
                window.close()  # Close the theme selector window
                return selected_theme  # Return the selected theme

    window.close()
    return None


def main_menu():
    global current_theme_index

    # Set initial theme
    sg.theme(themes[current_theme_index])

    # Layout of the GUI
    scale = 2
    layout = [
        [sg.Text(f'Debate Yap Tracker', size=(30*scale, 1*scale)), sg.Push()],
        [sg.Button('Select Theme', key='-SELECT_PREVIEW_THEME-', size=(12, 1), font=("", 8, ""), tooltip="Open the theme selection window"), sg.Push()],  
        [sg.Button('Select File', key='-SELECT_FILE-', button_color=('white', 'blue'), tooltip="Select a file from your system"),
         sg.Button('Select Screen', key='-SELECT_SCREEN-', button_color=('white', 'green'), tooltip="Select Screen/App to take screenshot from")],  
        [sg.Multiline(size=(60*scale, 10*scale), key='-OUTPUT-')], 
        [sg.Button('Exit', tooltip="Exit the application"), sg.Button('Run', size=(10, 1), tooltip="Run Code")]
    ]

    # Create the window with dynamic resizing enabled
    window = sg.Window('Debate Yap Tracker', layout, resizable=True)

    # Main event loop
    log_visible = True
    while True:
        event, values = window.read()
        
        # If user closes window or clicks Exit button
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
        # Handle button presses with logging
        if event in ('Run', 'Button 2', 'Button 3'):
            handle_button_press(event, window)
        
        # Handle file selection
        if event == '-SELECT_FILE-':
            file_path = sg.popup_get_file('Select a file', keep_on_top=True)
            if file_path:
                update_log(f"File selected: {file_path}", window)
        
        # Allow the user to select the screen or applciation to take the screenshots from
        elif event == "-SELECT_SCREEN-":
            open_select_screen_window(window)
            

        # Manually select a theme from the menu
        if event in themes:
            current_theme_index = themes.index(event)
            sg.theme(themes[current_theme_index])
            window.close()  # Close current window
            return main_menu()  # Re-run the main function to apply the new theme
        
        # Open the theme selector window
        if event == '-SELECT_PREVIEW_THEME-':
            selected_theme = open_theme_selector(window)
            if selected_theme:
                current_theme_index = themes.index(selected_theme)
                return main_menu()  # Re-run the main function to apply the new theme

    # Close the window
    window.close()

if __name__ == '__main__':
    main_menu()
