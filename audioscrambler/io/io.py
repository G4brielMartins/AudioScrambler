from pathlib import Path

import numpy as np
from pydub import AudioSegment

from .resample import resample_signal

def audio_to_np(audio_path: Path|str) -> tuple[int, np.ndarray]:
    """
    Import an audio file (WAV, MP3, etc.) and return its sample rate and normalized audio data.

    Args:
        audio_path (Path | str): Path to the audio file.

    Returns:
        tuple[int, np.ndarray]: A tuple containing the sample rate (int) and the normalized audio data (np.ndarray).
    """
    # Load audio file using pydub                                                                                            
    audio = AudioSegment.from_file(audio_path)

    # Convert to mono if stereo                                                                                              
    if audio.channels == 2:
        audio = audio.set_channels(1)

    # Get raw audio data and convert to NumPy array                                                                          
    samples = np.array(audio.get_array_of_samples())

    # Convert to float32                                                                                                     
    samples = samples.astype(np.float32)

    # Normalise float32 array so that values are between -1.0 and +1.0                                                      
    samples_normalised = samples / np.iinfo(np.int16).max

    return audio.frame_rate, samples_normalised

def import_audio(audio_path: Path|str, sample_rate: int) -> tuple[int, np.ndarray]:
    """
    Import an audio file (WAV, MP3, etc.) and return its sample rate and normalized audio data.
    If the audio file's sample rate differs from the specified sample_rate, it will be resampled.

    Args:
        audio_path (Path | str): Path to the audio file.
        sample_rate (int): Desired sample rate for the output audio data.

    Returns:
        tuple[int, np.ndarray]: A tuple containing the sample rate (int) and the normalized audio data (np.ndarray).
    """
    # Load audio file
    original_sample_rate, audio_data = audio_to_np(audio_path)

    # Resample if necessary
    if original_sample_rate != sample_rate:
        sample_rate, audio_data = resample_signal(audio_data, original_sample_rate, sample_rate)
    return sample_rate, audio_data

def export_audio(audio_path: Path|str, sample_rate: int, audio_data: np.ndarray) -> None:
    """
    Export audio data to a audio file (WAV, MP3, etc.).

    Args:
        audio_path (Path | str): Path to save the audio file.
        sample_rate (int): Sample rate of the audio data.
        audio_data (np.ndarray): The audio data to be saved.
    """
    # Convert float32 array to int16                                                                                         
    audio_data_int16 = (audio_data * np.iinfo(np.int16).max).astype(np.int16)

    # Create an AudioSegment from the NumPy array                                                                            
    audio_segment = AudioSegment(
        audio_data_int16.tobytes(),
        frame_rate=sample_rate,
        sample_width=audio_data_int16.dtype.itemsize,
        channels=1
    )

    # Export the audio segment to the specified file                                                                         
    audio_segment.export(audio_path, format=Path(audio_path).suffix[1:])  # Use file extension as format