import whisper

import time

import sys

import io

import pyaudio

import numpy as np

from scipy.io.wavfile import write

import wave

from pydub import AudioSegment

from gtts import gTTS

import os

model = whisper.load_model("base")

DURATION = 25

CHUNK = 1024

FORMAT = pyaudio.paInt32

CHANNELS = 1 if sys.platform == "darwin" else 2

RATE = 44100

audio_buffer = io.BytesIO()

frames = []

def callback(in_data,frame_count,time_info,status):

    # audio_chunk = AudioSegment(

    #     data = in_data,

    #     sample_width = p.get_sample_size(FORMAT),

    #     frame_rate = RATE,

    #     channels = CHANNELS

    #     )

    # mp3buffer = io.BytesIO()

    # audio_chunk.export(mp3buffer,format="mp3")

    # mp3buffer.seek(0)

    # audio_segment = AudioSegment.from_mp3(mp3buffer)

    # samples = np.array(audio_segment.get_array_of_samples())

    # samples = samples.astype(np.float32) / 32768.0

    # transcription = model.transcribe(samples)

    # print(transcription["text"])

    global audio_buffer

    audio_buffer.write(in_data)

    frames.append(in_data)

    return (in_data,pyaudio.paContinue)

p = pyaudio.PyAudio()

stream = p.open(

    format=FORMAT,

    channels=CHANNELS,

    rate=RATE,

    input=True,

    output=True,

    frames_per_buffer=CHUNK,

    stream_callback=callback

    )

start = time.time()

while stream.is_active() and (time.time() - start)<DURATION :

    time.sleep(0.1)

stream.close()

p.terminate()


wf = wave.open("test_output.wav", 'wb')

wf.setnchannels(CHANNELS)

wf.setsampwidth(p.get_sample_size(FORMAT))

wf.setframerate(RATE)

wf.writeframes(b''.join(frames))

wf.close()

audio_chunk = AudioSegment.from_wav("test_output.wav")

audio_chunk.export("test_output.mp3", format="mp3")

print("Audio has been written to test_output.wav and test_output.mp3")

# Load MP3 data for transcription

mp3_buffer = io.BytesIO()

audio_chunk.export(mp3_buffer, format="mp3")

mp3_buffer.seek(0)

audio_segment = AudioSegment.from_mp3(mp3_buffer)

samples = np.array(audio_segment.get_array_of_samples())

# Convert samples to floating point values

samples = samples.astype(np.float32) / 32768.0  # Convert to float32 and normalize

# Transcribe the numpy array

transcription = model.transcribe("test_output.mp3")

print(transcription['text'])

language = "en"

myobj = gTTS(text=transcription["text"], lang=language, slow=False)

# Saving the converted audio in a mp3 file named

# welcome 

myobj.save("welcome.mp3")

# Playing the converted file

os.system("start welcome.mp3")

# audio_buffer.seek(0)

# audio_chunk = AudioSegment(

#     data=audio_buffer.read(),

#     sample_width=p.get_sample_size(FORMAT),

#     frame_rate=RATE,

#     channels=CHANNELS

# )

# audio_chunk.export("test_output1.mp3", format="mp3")