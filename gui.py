import PySimpleGUI as sg
import os


# Creates initial GUI
def create_gui():
    types = ["schroeder", "moorer", "convolution"]

    layout = [[sg.Text("Choose an audio file")], [sg.FileBrowse(key="file", initial_folder="sounds")],
              [sg.Text("Choose reverb type")], [sg.Combo(types, readonly=True, key="type")],
              [sg.Button("Confirm")]]

    window = sg.Window("NRTVerb", layout, size=(500, 500), element_justification='c')

    while True:
        event, values = window.read()

        file = os.path.basename(values["file"])
        reverb_type = values["type"]

        if event == sg.WIN_CLOSED:
            window.close()

        if event == "Confirm":
            if not file:
                popup_error("no file selected")
            elif not reverb_type:
                popup_error("no reverb type selected")
            else:
                break

    if reverb_type == "schroeder":
        variables = schroeder_gui()
    elif reverb_type == "moorer":
        variables = moorer_gui()
    elif reverb_type == "convolution":
        variables = convolution_gui()

    window.close()

    return [file, reverb_type, variables]


# Creates GUI for Schroeder Reverberator with default initial values
def schroeder_gui():
    layout = [[sg.Text("ratio")], [sg.InputText("0.1", key="ratio")],
              [sg.Text("delay (ms)")], [sg.InputText("30", key="delay")],
              [sg.Text("allpass gain coefficient")], [sg.InputText("0.7", key="coefficient")],
              [sg.Button("Confirm")]]

    window_2 = sg.Window("Schroeder Reverb", layout, size=(500, 500), element_justification='c')

    while True:
        event, values = window_2.read()

        if event == sg.WIN_CLOSED:
            return None

        if event == "Confirm":
            break

    ratio = float(values["ratio"])
    delay = float(values["delay"])
    coefficient = float(values["coefficient"])

    window_2.close()

    return [ratio, delay, coefficient]


# Creates GUI for Moorer Reverberator with default initial values
def moorer_gui():
    layout = [[sg.Text("ratio")], [sg.InputText("0.1", key="ratio")],
              [sg.Text("delay taps")], [sg.InputText("20", key="taps")],
              [sg.Text("tap spacing (ms)")], [sg.InputText("10", key="spacing")],
              [sg.Text("delay (ms)")], [sg.InputText("30", key="delay")],
              [sg.Text("allpass gain coefficient")], [sg.InputText("0.7", key="coefficient")],
              [sg.Text("lowpass cutoff frequency")], [sg.InputText("2000", key="cutoff")],
              [sg.Button("Confirm")]]

    window_2 = sg.Window("Moorer Reverb", layout, size=(500, 500), element_justification='c')

    while True:
        event, values = window_2.read()

        if event == sg.WIN_CLOSED:
            return None

        if event == "Confirm":
            break

    taps = int(values["taps"])
    spacing = float(values["spacing"])
    ratio = float(values["ratio"])
    delay = float(values["delay"])
    coefficient = float(values["coefficient"])
    cutoff = float(values["cutoff"])

    window_2.close()

    return [taps, spacing, ratio, delay, coefficient, cutoff]


# Creates GUI for Convolution Reverb with default initial values
def convolution_gui():
    layout = [[sg.Text("File to convolve with")],
              [sg.FileBrowse(key="convolution_file", initial_folder="sounds/RIR")],
              [sg.Text("ratio")], [sg.InputText("0.15", key="ratio")],
              [sg.Button("Confirm")]]

    window_2 = sg.Window("Convolution Reverb", layout, size=(500, 500), element_justification='c')

    while True:
        event, values = window_2.read()

        convolution_file = os.path.basename(values["convolution_file"])

        if event == sg.WIN_CLOSED:
            return None

        if event == "Confirm":
            if not convolution_file:
                popup_error("no file selected")
            else:
                break

    ratio = float(values["ratio"])

    window_2.close()

    return [convolution_file, ratio]


def popup_error(msg="select file"):
    layout = [[sg.Text(msg)],
              [sg.Button("OK")]]

    error_window = sg.Window("error", layout, element_justification='c')

    while True:
        event, values = error_window.read()

        if event == sg.WIN_CLOSED:
            return None

        if event == "OK":
            break

    error_window.close()