#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pyaudio
import wave
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()],
    format='%(levelname)s:%(asctime)s:%(message)s'
)

class VoicePlayer:

    def __init__(self) -> None:
        self.chunk = 1024

    def play(self, filename):
        logging.debug("[VoicePlayer.play] - load file %s" % filename)
        chunk = 1024
        wf = wave.open('voice.wav', 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)
        data = wf.readframes(chunk)

        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)
            if data == b'':
                break

        stream.close()
        p.terminate()
        logging.debug("[VoicePlayer.play] - Voice Play Finish")