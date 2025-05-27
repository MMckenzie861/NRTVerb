import sys
import numpy as np
import soundfile as sf
from scipy import signal


def usage(msg=None):
    if msg is not None:
        print("Error: " + msg)

    sys.exit(1)


# Convolves file with RIR from GUI, slow but as this isn't real-time not a huge issue
def convolutional_reverb(samples, convolution_file, ratio):
    try:
        RIR, RSR = sf.read("sounds/RIR/" + convolution_file)
    except FileNotFoundError:
        usage(f"file {convolution_file} does not exist")

    reverb = signal.fftconvolve(samples, RIR)

    for i in range(len(samples)):
        samples[i] += ratio * reverb[i]

    return samples