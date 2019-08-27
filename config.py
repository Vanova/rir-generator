import numpy as np
import soundfile
from scipy.signal import max_len_seq

# room parameters: 10m x 20m x 3m
room_dim = (20, 10, 3) # x y z
human_height = 1.6
corners = np.array([[0, 0],
                    [0, room_dim[1]],
                    [room_dim[0], room_dim[1]],
                    [room_dim[0], 0]]).T  # [x,y]
absorption = 0.4

# specify signal source
test_signal, test_fs = soundfile.read('data/guitar_16k.wav')
# Maximum length sequence (MLS)
nbits_mls = 12
mls_signal = max_len_seq(nbits_mls)[0] * 2 - 1
fs = 16000
soundfile.write('mls.wav', mls_signal.astype('float32'), fs)

# locate IR36 source
resolution = 10
azimuth = np.array(range(0, 360, resolution))
radius = np.array([1.5]) #np.array([[0.5, 1.5, 3.]])

# mics parameters (meters)
mic_n = 8
# mics position on the device [[x], [y]]
mic_position = np.array([[0., -0.03813, -0.02898, 0.01197, 0.03591, 0.03281, 0.005, -0.02657],
                         [0., 0.00358, 0.03204, 0.03638, 0.01332, -0.01977, -0.03797, -0.02758]])
# move mics to the center of the room
xy_center = np.array(room_dim[:2]) / 2.
mic_location = mic_position + xy_center[:, np.newaxis]  # [[x], [y], [z]]
mic_location = np.vstack([mic_location,
                          np.repeat(room_dim[2], mic_n)])

