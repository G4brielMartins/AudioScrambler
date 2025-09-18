from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sig

from .io import import_audio, export_audio, resample_signal

# Configurações de gráficos
#---------------------------------
plt.rcParams.update({
    'font.size': 16,
    'axes.titlesize': 18,
    'axes.labelsize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14,
    'figure.titlesize': 20
}) 
#---------------------------------

class Scrambler:
    def __init__(self, audio_path: str, desired_rate: int = 96_000, out_path: str = None) -> None:
        self.rate, self.audio = import_audio(audio_path, desired_rate)
        self.scramble()
        self.descramble()
        self.out_path = Path(out_path)

    @property
    def signals(self):
        signals = {
            'original': self.audio,
            'scrambled': self.scrambled_audio,
            'descrambled': self.descrambled_audio,
        }
        return signals
    
    @staticmethod
    def modulate(audio_rate: int, input_signal: np.ndarray) -> np.ndarray:
        # Define time vector
        t = np.arange(len(input_signal)) / audio_rate

        # Define signals
        m_t = input_signal
        cos_20k_hz = np.cos(2 * np.pi * 20_000 * t)
        cos_25k_hz = np.cos(2 * np.pi * 25_000 * t)

        # Design filters
        nyquist_freq = audio_rate / 2
        fpa_20k_hz = sig.butter(150, 20_000 / nyquist_freq, btype='highpass', output='sos')
        fpb_20k_hz = sig.butter(150, 20_000 / nyquist_freq, btype='lowpass', output='sos')

        # Modulate
        x1_t = m_t * 2 * cos_20k_hz
        x2_t = sig.sosfiltfilt(fpa_20k_hz, x1_t)
        x3_t = x2_t * 2 * cos_25k_hz
        y_t = sig.sosfiltfilt(fpb_20k_hz, x3_t)

        return y_t

    def scramble(self) -> np.ndarray:
        m_t = self.audio
        
        # Modulate
        y_t = self.modulate(self.rate, m_t)

        self.scrambled_audio = y_t
        return y_t
    
    def descramble(self) -> np.ndarray:
        if self.scrambled_audio is None:
            self.scramble()
        
        # Demodulate
        y_t = self.scrambled_audio
        m_rec_t = self.modulate(self.rate, y_t) # Self-invertible system

        self.descrambled_audio = m_rec_t
        return m_rec_t

    def export_audio(self, output_dir: str|None = None, signals: list[str] = ['all']) -> None:
        output_dir = self.out_path if output_dir is None else Path(output_dir)

        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
        
        if 'all' in signals:
            signals = ['original', 'scrambled', 'descrambled']

        for signal in signals:
            if signal not in self.signals:
                raise ValueError("Signal must be 'original', 'scrambled', 'descrambled', or 'all'.")
            export_audio(output_dir / f"{signal}.mp3", self.rate, self.signals[signal])
    
    def plot_signals(self, signals: list[str] = ['all'], sample_rate: int = 44_100) -> None:
        if 'all' in signals:
            signals = ['original', 'scrambled', 'descrambled']

        plt.figure(figsize=(15, 10))
        for i, signal_name in enumerate(signals):
            if signal_name not in self.signals:
                raise ValueError("Signal must be 'original', 'scrambled', 'descrambled', or 'all'.")
            
            rate, signal = resample_signal(self.signals[signal_name], self.rate, sample_rate)
            
            plt.subplot(len(signals), 1, i + 1)
            plt.plot(signal)
            plt.ylim(-1, 1)
            plt.title(f"{signal_name.capitalize()} Audio Signal")
            plt.xlabel("Time [sec]")
            plt.ylabel("Amplitude [normalized]")

        plt.tight_layout()
        if self.out_path is None:
            plt.show()
        else:
            plt.savefig(self.out_path / "time_plot")


    def plot_spectrograms(self, signals: list[str] = ['all'], sample_rate: int = 44_100) -> None:
        if 'all' in signals:
            signals = ['original', 'scrambled', 'descrambled']
        
        plt.figure(figsize=(15, 10))
        for i, signal_name in enumerate(signals):
            if signal_name not in self.signals:
                raise ValueError("Signal must be 'original', 'scrambled', 'descrambled', or 'all'.")

            rate, signal = resample_signal(self.signals[signal_name], self.rate, sample_rate)

            unnormalized = signal * np.iinfo(np.int16).max
            
            plt.subplot(len(signals), 1, i + 1)
            plt.specgram(unnormalized, Fs=rate, scale='dB', vmin=-40, vmax=40,)
            plt.ylim(0, rate / 2)
            plt.colorbar(label='Intensity [dB]')
            plt.ylabel('Frequency [Hz]')
            plt.xlabel('Time [sec]')
            plt.title(f'Spectrogram of {signal_name.capitalize()} Audio Signal')

        plt.tight_layout()
        if self.out_path is None:
            plt.show()
        else:
            plt.savefig(self.out_path / "spectograms")
