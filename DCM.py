import PySimpleGUI as sg
import json
from pathlib import Path
from PIL import Image, ImageTk
from time import sleep
import numpy as np


def login():
    filename = "DCM.jpeg"

    # Resize image file
    size = (450, 600)
    img = Image.open(filename)
    img = img.resize(size, resample=Image.BICUBIC)

    sg.theme('DefaultNoMoreNagging')

    left_side = [
        [sg.Image(key='-IMAGE-')],
    ]

    login_button = [
        [sg.Button("Login", size=(25, 1), pad=(5, 5), button_color='Grey20', bind_return_key=True)]
    ]

    register_button = [
        [sg.Text("New user?", enable_events=True, key="REGISTER", text_color='Blue')],
    ]

    right_side = [
        [sg.Text("Username:")],
        [sg.InputText(key="user", size=(30, 40), do_not_clear=False, pad=(10, 10))],
        [sg.Text("Password:")],
        [sg.InputText(key="password", password_char="*", size=(30, 40), do_not_clear=False, pad=(10, 10))],
        [sg.Column(login_button, element_justification='center', expand_x=True)],
        [sg.Column(register_button, element_justification='center', expand_x=True)],
    ]

    layout = [
        [sg.Column(left_side),
         # sg.VSeperator(pad=(0, 100)),
         sg.Column(right_side, pad=(20, 20)),
         ]
    ]

    window = sg.Window('Pacemaker DCM Login', layout, margins=(0, 0), finalize=True, resizable=False)

    # Convert im to ImageTk.PhotoImage after window finalized
    image = ImageTk.PhotoImage(image=img)

    # update image in sg.Image
    window['-IMAGE-'].update(data=image)

    # Create an event loop
    while True:
        event, values = window.read()

        # opening json to use in event loop
        f = open("users.json", "r+")
        info = json.load(f)

        if event == "Login" or event == sg.WIN_CLOSED:
            # check if text fields are empty
            if values['user'] and values['password']:
                # create flag variable
                flag = False
                # Check login in data in json
                for i in info['user_list']:
                    if values['user'] == i['User']:
                        flag = True
                        if values['password'] == i['Pass']:
                            sg.popup_quick_message("Welcome!", text_color="Green")
                            sleep(1)
                            window.close()
                            AOO()
                        else:
                            sg.popup_ok("Incorrect Password", text_color="Red")
                            break
                if not flag:
                    sg.popup_ok("Not an active user", text_color="Red")

        if event == "HELP" or event == sg.WIN_CLOSED:
            break

        if event == "REGISTER" or event == sg.WIN_CLOSED:
            window.close()
            # sg.popup(register(f, info))
            register(f, info)

        # close json file
        f.close()
    window.close()


def register(f, info):
    filename = "DCM.jpeg"

    # Resize PNG file to size (300, 300)
    size = (450, 600)
    img = Image.open(filename)
    img = img.resize(size, resample=Image.BICUBIC)

    sg.theme('DefaultNoMoreNagging')

    left_side = [
        [sg.Image(key='-IMAGE-')],
    ]

    register_button = [
        [sg.Button("Register", size=(25, 1), pad=(5, 5), button_color='Grey20', bind_return_key=True)]
    ]

    back_button = [
        [sg.Text("Back", enable_events=True, key="Back", text_color='Blue')],
    ]

    right_side = [
        [sg.Text("Username:")],
        [sg.InputText(key="USER", size=(30, 40), do_not_clear=False, pad=(10, 10))],
        [sg.Text("Password:")],
        [sg.InputText(key="PASSWORD", password_char="*", size=(30, 40), do_not_clear=False, pad=(10, 10))],
        [sg.Text("Reenter Password:")],
        [sg.InputText(key="REENTER", password_char="*", size=(30, 40), do_not_clear=False, pad=(10, 10))],
        [sg.Column(register_button, element_justification='center', expand_x=True)],
        [sg.Column(back_button, element_justification='center', expand_x=True)]
    ]

    layout = [
        [sg.Column(left_side),
         sg.Column(right_side, pad=(20, 20)),
         ]
    ]

    window = sg.Window('Pacemaker DCM Registration', layout, margins=(0, 0), finalize=True, resizable=False)

    # Convert im to ImageTk.PhotoImage after window finalized
    image = ImageTk.PhotoImage(image=img)

    # update image in sg.Image
    window['-IMAGE-'].update(data=image)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Back":
            window.close()
            login()
        if event == 'Register':
            # check if text fields are empty
            if values['USER'] and values['PASSWORD']:
                if values['PASSWORD'] == values['REENTER']:
                    # create flag variable
                    flag = False

                    # check existing users
                    for i in info['user_list']:
                        if values['USER'] == i['User']:
                            flag = True
                            sg.popup_ok("Already an active user. Please try a new username.")
                            break

                    # create new user if username did not already exist
                    if not flag:
                        # create variable to determine how many users currently exist
                        ID = len(info['user_list'])
                        # check to see if max num users is exceeded
                        if ID + 1 <= 10:
                            new_user = {"User": f"{values['USER']}", "Pass": f"{values['PASSWORD']}", "ID": f"{ID + 1}"}
                            info['user_list'].append(new_user)
                            f.seek(0)
                            json.dump(info, f, indent=4)
                            f.close()
                            sg.popup_quick_message("Welcome!", text_color="Green")
                            sleep(1)
                            window.close()
                            AOO()
                        else:
                            sg.popup_ok("Max. number of users has been reached.\nPlease contact service provider.")
                else:
                    sg.popup_ok("Passwords do not match.", text_color="Red")
                    # sg.popup_error("Passwords do not match.")


def connection_page():
    sg.theme('DefaultNoMoreNagging')

    layout = [
        [sg.Text("Connection:", size=(11, 2), font=("Helvetica", 20)),
         sg.Text("Not-Connected", size=(11, 2), font=("Helvetica", 20), key='connect'), sg.Button('Sign Out')],
        [sg.Text("Device:", size=(11, 2), font=("Helvetica", 20)),
         sg.Text("", size=(11, 2), font=("Helvetica", 20), key='device')],
        [sg.Button('Connect')]
    ]

    window = sg.Window('Pacemaker DCM', layout, margins=(250, 250), element_justification='c')

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Sign Out":
            window.close()
            login()
        if event == "Connect":
            values['connect'] = 'Connected'
            values['device'] = 'Pacemaker123'


def mode():
    sg.theme('DefaultNoMoreNagging')
    layout = [
        [sg.Button('AOO'), sg.HSeparator(pad=(5, 5)), sg.Button('VOO'), sg.HSeparator(pad=(5, 5)), sg.Button('AAI'),
         sg.HSeparator(pad=(5, 5)), sg.Button('VVI')]
    ]

    window = sg.Window('Modes', layout, margins=(20, 20), element_justification='c')

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Sign Out":
            window.close()
            login()
        if event == "AOO":
            AOO()
        if event == "VOO":
            VOO()


def AOO():
    filename = "heart.png"

    # Resize image file
    size = (300, 100)
    img = Image.open(filename)
    img = img.resize(size, resample=Image.BICUBIC)

    lower_rate_limit = list(range(30, 175))
    upper_rate_limit = list(range(50, 175))
    atrial_amplitude = np.arange(0.5, 3.2, 0.1)
    atrial_pulse_width = np.arange(0.1, 1.9, 0.1)

    sg.theme('Reddit')

    top_left = [
        [sg.Text("Status: "), sg.Text("Connected", text_color="Green")],
        [sg.Text("Device: "), sg.Text("Pacemaker123", text_color="Blue")],
    ]

    top_right = [
        [sg.Button('Sign Out')]
    ]

    middle = [
        [sg.Image(key='-IMAGE-')],
        [sg.Text("Pacing Mode: AOO")],
        [sg.Text("Change mode", enable_events=True, key="CHANGE", text_color='Blue')]
    ]

    left_parameters = [
        [sg.Text("Lower Rate Limit (ppm):")],
        [sg.Text("Upper Rate Limit (ppm):")],
    ]

    left_inputs = [
        [sg.Combo(lower_rate_limit, key="LRL", size=(10, 10), pad=(10, 10))],
        [sg.Combo(upper_rate_limit, key="LRL", size=(10, 10), pad=(10, 10))],
    ]

    right_parameters = [
        [sg.Text("Atrial Amplitude (V):")],
        [sg.Text("Atrial Pulse Width (ms):")],
    ]

    right_inputs = [
        [sg.Combo(atrial_amplitude, key="LRL", size=(10, 10), pad=(10, 10))],
        [sg.Combo(atrial_pulse_width, key="LRL", size=(10, 10), pad=(10, 10))],
    ]

    confirm = [
        [sg.Button('Send Inputs', button_color="Green")]
    ]

    layout = [
        [sg.Column(top_left),
         sg.Text("                                                                            "),
         sg.Column(top_right, element_justification="right")],
        [sg.Column(middle, element_justification='center', expand_x=True)],
        [
            sg.Column(left_parameters),
            sg.Column(left_inputs),
            sg.Column(right_parameters),
            sg.Column(right_inputs)
        ],
        [sg.Column(confirm, element_justification='center', expand_x=True)]
    ]

    window = sg.Window('Pacemaker DCM Login', layout, margins=(10, 10), finalize=True, resizable=False)

    # Convert im to ImageTk.PhotoImage after window finalized
    image = ImageTk.PhotoImage(image=img)

    # update image in sg.Image
    window['-IMAGE-'].update(data=image)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Sign Out":
            window.close()
            login()
        if event == "CHANGE":
            sg.popup(mode())


def VOO():
    filename = "heart.png"

    # Resize image file
    size = (300, 100)
    img = Image.open(filename)
    img = img.resize(size, resample=Image.BICUBIC)

    lower_rate_limit = ['1', '2']
    upper_rate_limit = ['1', '2']
    atrial_amplitude = ['1', '2']
    atrial_pulse_width = ['1', '2']

    sg.theme('Default')

    top_left = [
        [sg.Text("Status: "), sg.Text("Connected", text_color="Green")],
        [sg.Text("Device: "), sg.Text("Pacemaker123", text_color="Blue")],
    ]

    top_right = [
        [sg.Button('Sign Out')]
    ]

    middle = [
        [sg.Image(key='-IMAGE-')],
        [sg.Text("Pacing Mode: VOO")],
        [sg.Text("Change mode", enable_events=True, key="CHANGE", text_color='Blue')]
    ]

    left_inputs = [
        [sg.Text("Lower Rate Limit:"), sg.Combo(lower_rate_limit, key="LRL", size=(10, 10), pad=(10, 10))],
        [sg.Text("Upper Rate Limit:"), sg.Combo(upper_rate_limit, key="LRL", size=(10, 10), pad=(10, 10))],
    ]
    right_inputs = [
        [sg.Text("Ventricular Amplitude:"), sg.Combo(atrial_amplitude, key="LRL", size=(10, 10), pad=(10, 10))],
        [sg.Text("Ventricular Pulse Width:"), sg.Combo(atrial_pulse_width, key="LRL", size=(10, 10), pad=(10, 10))],
    ]

    layout = [
        [sg.Column(top_left),
         sg.Text("                                                                            "),
         sg.Column(top_right, element_justification="right")],
        [sg.Column(middle, element_justification='center', expand_x=True)],
        [sg.Column(left_inputs),
         sg.Column(right_inputs, pad=(20, 20)),
         ]
    ]

    window = sg.Window('Pacemaker DCM Login', layout, margins=(10, 10), finalize=True, resizable=False)

    # Convert im to ImageTk.PhotoImage after window finalized
    image = ImageTk.PhotoImage(image=img)

    # update image in sg.Image
    window['-IMAGE-'].update(data=image)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Sign Out":
            window.close()
            login()
        if event == "CHANGE":
            sg.popup(mode())


if __name__ == "__main__":
    SETTINGS_PATH = Path.cwd()
    # create the settings object and use ini format
    settings = sg.UserSettings(
        path=SETTINGS_PATH, filename="config.ini", use_config_file=True, convert_bools_and_none=True
    )
    theme = settings["GUI"]["theme"]
    font_family = settings["GUI"]["font_family"]
    font_size = int(settings["GUI"]["font_size"])
    sg.theme(theme)
    sg.set_options(font=(font_family, font_size))
    login()
