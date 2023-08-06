# This file is part of audioread.
import audioread
import sys
import os
import wave
import contextlib


def decodeaudio(filename):
    #try:
    with audioread.audio_open(filename) as f:
        with contextlib.closing(wave.open(filename.split('.')[0] + '.wav', 'w')) as of:
            of.setnchannels(f.channels)
            of.setframerate(f.samplerate)
            of.setsampwidth(2)

            for buf in f:
                of.writeframes(buf)
