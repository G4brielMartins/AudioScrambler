import numpy as np
from scipy import signal

def lowpass_filter(input_signal: np.ndarray, cutoff_freq: int, nyquist_freq: int) -> np.ndarray:
    """
    Apply an interpolating low-pass filter to the input signal.

    Parameters:
    - input_signal: np.ndarray
        The input audio signal.
    - cutoff_freq: int
        The cutoff frequency of the low-pass filter.
    - nyquist_rate: int
        The Nyquist rate (half the sampling rate) of the output signal.

    Returns:
    - np.ndarray
        The filtered audio signal.
    """
    # Design a low-pass Butterworth filter
    normalized_cutoff = cutoff_freq / nyquist_freq
    butter = signal.butter(5, normalized_cutoff, btype='lowpass', output='sos')
    
    # Apply the filter to the input signal
    filtered_signal = signal.sosfiltfilt(butter, input_signal)
    return filtered_signal

def upsample_signal(input_signal: np.ndarray, input_rate: int, output_rate: int) -> tuple[int, np.ndarray]:
    """
    Oversample the input audio signal from input_rate to output_rate.

    Parameters:
    - input_signal: np.ndarray
        The input audio signal.
    - input_rate: int
        The original sampling rate of the input signal.
    - output_rate: int
        The desired sampling rate after resampling. (Must be greater than input_rate.)

    Returns:
    - np.ndarray
        The resampled audio signal.
    """
    if output_rate < input_rate:
        raise ValueError("output_rate must be greater than input_rate for oversampling.")

    # Calculate the closest output_rate with integer ratio
    output_rate = input_rate * (output_rate // input_rate)
    ratio = int(output_rate / input_rate)

    # Adding zeros to the input signal
    zero_padded_signal = np.zeros(len(input_signal) * ratio)
    zero_padded_signal[::ratio] = input_signal
    
    # Apply the interpolating filter to the zero-padded signal
    nyquist_freq = output_rate / 2.0
    cutoff_freq = input_rate / 2.0  # Nyquist frequency of the original signal
    filtered_signal = lowpass_filter(zero_padded_signal, cutoff_freq, nyquist_freq)

    return output_rate, filtered_signal

def downsample_signal(input_signal: np.ndarray, input_rate: int, output_rate: int) -> tuple[int, np.ndarray]:
    """
    Downsample the input audio signal from input_rate to output_rate.

    Parameters:
    - input_signal: np.ndarray
        The input audio signal.
    - input_rate: int
        The original sampling rate of the input signal.
    - output_rate: int
        The desired sampling rate after resampling. (Must be less than input_rate.)

    Returns:
    - np.ndarray
        The resampled audio signal.
    """
    if output_rate > input_rate:
        raise ValueError("output_rate must be less than input_rate for downsampling.")

    # Calculate the closest output_rate with integer ratio
    output_rate = input_rate / (input_rate // output_rate)
    ratio = int(input_rate / output_rate)

    # Apply the filter to the input signal
    nyquist_freq = input_rate / 2.0
    cutoff_freq = output_rate / 2.0  # Nyquist frequency of the downsampled signal
    filtered_signal = lowpass_filter(input_signal, cutoff_freq, nyquist_freq)

    # Downsample by taking every 'ratio'-th sample
    downsampled_signal = filtered_signal[::ratio]

    return output_rate, downsampled_signal

def resample_signal(input_signal: np.ndarray, input_rate: int, output_rate: int) -> tuple[int, np.ndarray]:
    """
    Resample the input audio signal from input_rate to output_rate.

    Parameters:
    - input_signal: np.ndarray
        The input audio signal.
    - input_rate: int
        The original sampling rate of the input signal.
    - output_rate: int
        The desired sampling rate after resampling.

    Returns:
    - np.ndarray
        The resampled audio signal.
    """
    if output_rate == input_rate:
        return input_rate, input_signal
    elif output_rate > input_rate:
        return upsample_signal(input_signal, input_rate, output_rate)
    else:
        return downsample_signal(input_signal, input_rate, output_rate)