import sys
import numpy as np
import random
import math


def usage(msg=None):
    if msg is not None:
        print("Error: " + msg)

    sys.exit(1)


# Runs file through a Schroeder Reverberator with given variables from GUI, would like to add functionality to change
# number of delay comb filters but didn't want to give user too many choices without enough context
def schroeder_reverb(samples, delay, coefficient, ratio, sr):
    # Creates 3 additional delays with random amounts between the initial delay and 1.5x the initial delay
    delays = [delay / 1000]
    for i in range(3):
        delays.append((delay + random.randint(1, delay // 2)) / 1000)

    delayed_samples = []
    for i in delays:
        delay_samples = int(sr * i)

        delayed_samples.append(schroeder_delay(samples, delay_samples, coefficient))

    # Sums all comb filter delays
    full_delayed_samples = delayed_samples[0]
    for i in range(1, 4):
        np.add(full_delayed_samples, delayed_samples[i])

    # Runs delayed samples through an allpass filter, 1 allpass seems to work better than 2 for this, unsure why
    allpass_samples = allpass(full_delayed_samples, coefficient, sr)

    # Adds reverb samples back to original at desired ratio
    for i in range(len(allpass_samples)):
        samples[i] += ratio * allpass_samples[i]

    return samples


# Delays samples according to equation y[n] = x[n - d] + gy[n-d]
def schroeder_delay(samples, delay_samples, coefficient):
    y_delayed = 0
    zeros = [0.0] * len(samples)
    output = np.array(zeros)

    for i in range(delay_samples, len(samples)):
        output[i] = samples[i - delay_samples] + coefficient * y_delayed
        y_delayed = output[i - delay_samples]

    return output


# Adds higher density reverberations to the late impulse response according to equation y[n] = -gx[n]+x[n-d]+gy[n-d]
def allpass(samples, coefficient, sr):
    output_1_delayed = 0
    output_2_delayed = 0
    zeros = [0.0] * len(samples)
    output_1 = np.array(zeros)
    output_2 = np.array(zeros)
    d_1 = int(5 / 1000 * sr)
    d_2 = int(1.7 / 1000 * sr)

    for i in range(len(samples)):
        output_1[i] = -1 * coefficient * samples[i] + samples[i - d_1] + coefficient * output_1_delayed
        output_1_delayed = output_1[i - d_1]

    for i in range(len(output_1)):
        output_2[i] = -1 * coefficient * output_1[i] + output_1[i - d_2] + coefficient * output_2_delayed
        output_2_delayed = output_2[i - d_2]

    return output_2