import sys
import os
import soundfile as sf
import numpy as np
import gui
import schroeder_reverb as schr
import moorer_reverb as moor
import convolutional_reverb as conv
import subprocess


# For error handling
def usage(msg=None):
    if msg is not None:
        print("Error: " + msg)

    sys.exit(1)


def NRTVerb():
    # Gets Variables for filename, reverb type, and reverb variables from GUI
    all_variables = gui.create_gui()

    # Separates the results from the GUI
    variables = all_variables.pop()
    reverb_type = all_variables.pop()
    fp = all_variables.pop()

    try:
        samples, sr = sf.read("sounds/" + fp)
    except FileNotFoundError:
        usage(f"file {fp} does not exist")

    if samples.ndim == 2:
        zeros = [0.0] * len(samples)
        average_samples = np.array(zeros)

        for i in range(len(samples)):
            average_samples[i] = np.average(samples[i])

        samples = average_samples

    # Sets variables and creates file of requested reverb type
    if reverb_type == "schroeder":
        schroeder_coefficient = variables.pop()
        delay = variables.pop()
        ratio = variables.pop()

        new_samples = schr.schroeder_reverb(samples, delay, schroeder_coefficient, ratio, sr)
    elif reverb_type == "moorer":
        cutoff = variables.pop()
        schroeder_coefficient = variables.pop()
        delay = variables.pop()
        ratio = variables.pop()
        spacing = variables.pop()
        taps = variables.pop()

        new_samples = moor.moorer_reverb(samples, delay, schroeder_coefficient, ratio, taps, spacing, cutoff, sr)
    elif reverb_type == "convolution":
        ratio = variables.pop()
        convolution_file = variables.pop()

        new_samples = conv.convolutional_reverb(samples, convolution_file, ratio)

        fp = convolution_file + "_" + fp
    else:
        usage(f"{reverb_type} is not an available reverb")

    new_file = reverb_type + "_reverb_" + fp
    new_fp = "sounds/results/" + new_file

    sf.write(new_fp, new_samples, sr)

    full_path = fr"{os.getcwd()}/sounds/results".replace("\\", "/")

    if sys.platform == "win32":
        os.startfile(full_path)
    else:
        if sys.platform == "darwin":
            opener = "open"
        else:
            opener = "xdg-open"

        subprocess.call([opener, full_path])

    return 0


if __name__ == "__main__":
    NRTVerb()