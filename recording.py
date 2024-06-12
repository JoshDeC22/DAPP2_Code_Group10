import pyaudio
import numpy as np

p = pyaudio.PyAudio()

def record_audio():
    stream = p.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = 16000,
        input = True,
        frames_per_buffer = 3200,
        input_device_index = 1
    )

    frames = []
    seconds = 1
    for i in range(0, int(5)):
        data = stream.read(3200)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    return np.frombuffer(b''.join(frames), dtype = np.int16)

def terminate():
    p.terminate()
