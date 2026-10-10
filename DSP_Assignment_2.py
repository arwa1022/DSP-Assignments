import numpy as np

def checkAliasing(normal_F, sampling_F):
    return sampling_F < (2 * normal_F)

def analogSignal(wave, A, normal_F, phase_shift):
    # High-density points to display a smooth continuous curve over 1 second
    t = np.linspace(0, 1, 1000)
    
    if wave == "sin":
        analog_signal = A * np.sin(2 * np.pi * normal_F * t + phase_shift)
    else:
        analog_signal = A * np.cos(2 * np.pi * normal_F * t + phase_shift)
        
    return t, analog_signal

def discreteSignal(wave, A, sampling_F, normal_F, phase_shift):
    # Integer sample indices over 1 second: 0, 1, ..., int(sampling_F) - 1
    total_samples = int(sampling_F)
    n = np.arange(total_samples)
    
    # x[n] = A * wave(2 * pi * (F / Fs) * n + theta)
    omega_d = 2 * np.pi * (normal_F / sampling_F)
    
    if wave == "sin":
        discrete_signal = A * np.sin(omega_d * n + phase_shift)
    else:
        discrete_signal = A * np.cos(omega_d * n + phase_shift)
        
    return n, discrete_signal