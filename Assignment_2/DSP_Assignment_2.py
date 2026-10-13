import numpy as np

def checkAliasing(normal_F, sampling_F):
    return sampling_F < (2 * normal_F)

def analogSignal(wave, A, normal_F, phase_shift):
    # high-density points to display a smooth continuous curve over 1 second
    t = np.linspace(0, 1, 1000)
    
    if wave == "sin":
        analog_signal = A * np.sin(2 * np.pi * normal_F * t + phase_shift)
    else:
        analog_signal = A * np.cos(2 * np.pi * normal_F * t + phase_shift)
        
    return t, analog_signal

def discreteSignal(wave, A, sampling_F, normal_F, phase_shift):
    # integer sample indices over 1 second: 0, 1, ..., int(sampling_F) - 1
    total_samples = int(sampling_F)
    n = np.arange(total_samples)
    
    # ω = 2 * π * (normal_F / sampling_F)
    ω = 2 * np.pi * (normal_F / sampling_F)

    # x[n] = A * wave(ω * n + theta)
    if wave == "sin":
        discrete_signal = A * np.sin(ω * n + phase_shift)
    else:
        discrete_signal = A * np.cos(ω * n + phase_shift)
        
    return n, discrete_signal