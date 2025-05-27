import sys
import numpy as np
import schroeder_reverb as sch
import math


def usage(msg=None):
    if msg is not None:
        print("Error: " + msg)

    sys.exit(1)


# Runs file through a Moorer Reverberator with given variables from GUI
def moorer_reverb(samples, delay, coefficient, ratio, taps, spacing, cutoff, sr):
    # Runs samples through TDL to create better early impulse response
    new_samples = tap_delay(samples, taps, sr * (spacing / 1000) / taps)
    np.add(samples, new_samples)

    # Then runs samples through a Schroeder Reverberator
    sch.schroeder_reverb(samples, delay, coefficient, ratio, sr)

    samples = lowpass(samples, cutoff)

    return samples


# TDL for better early reflections
def tap_delay(samples, taps, tap_spacing):
    zeros = [0.0] * len(samples)
    output = np.array(zeros)

    for i in range(len(samples)):
        delay_line = 0.0
        for tap in range(taps):
            try:
                delay_line += (1 / taps) * samples[i - int(tap * tap_spacing)]
            except IndexError:
                delay_line += 0.0

        output[i] = delay_line

    return output


def lowpass(samples, cutoff):
    alpha = 1 - math.pow(np.e, (-1 * cutoff * len(samples)))
    feedback = 0
    lowpass_samples = [0.0] * len(samples)

    for i in range(len(samples)):
        lowpass_samples[i] = alpha * samples[i] + (1 - alpha) * feedback
        feedback = lowpass_samples[i]

    return lowpass_samples