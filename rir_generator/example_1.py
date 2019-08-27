# export LD_LIBRARY_PATH="`pwd`:$LD_LIBRARY_PATH";
import os
import matplotlib.pyplot as plt
import pyrirgen
import soundfile
import numpy as np
print(os.environ.get('LD_LIBRARY_PATH'))

# TODO model IR36

c = 340  # Sound velocity (m/s)
fs = 16000  # Sample frequency (samples/s)
r = [2, 1.5, 2]  # Receiver position [x y z] (m)
s = [2, 3.5, 2]  # Source position [x y z] (m)
L = [10, 20, 3]  # Room dimensions [x y z] (m)
rt = 3.  # Reverberation time (s)
n = 2*2048  # Number of samples

h = pyrirgen.generateRir(L, s, r, soundVelocity=c, fs=fs, reverbTime=rt, nSamples=n)
print(len(h))
soundfile.write('ir.wav', h, fs)

# plt.figure()
# plt.plot(h)
# plt.show()


def convolve(signal, response):
    """Convolves two waves.
    Note: this operation ignores the timestamps; the result
    has the timestamps of self.
    other: Wave or NumPy array

    returns: Wave
    """
    # assert framerate == framerate
    #     window = other.ys
    # else:
    #     window = other
    res_sig = np.convolve(signal, response, mode='full')
    # ts = np.arange(len(ys)) / self.framerate
    return res_sig


audio, fs = soundfile.read('test.wav')
conv_aud = convolve(audio, h)
soundfile.write('test_ir.wav', conv_aud, fs)