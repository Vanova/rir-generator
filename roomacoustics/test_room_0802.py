"""
Simulation of room IR with 4 omnidirectional microphones
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import soundfile
import pyroomacoustics as pra
import utils.geometry as geo
import config as cfg


def generate_room_impulse(azimuth, radius, rir_out_dir):
    for phi in azimuth:
        for r in radius:
            # set max_order to a low value for a quick (but less accurate) RIR
            room = pra.Room.from_corners(cfg.corners, fs=cfg.fs, max_order=12, absorption=0.2)
            # room = pra.ShoeBox()
            room.extrude(cfg.room_dim[2])

            # add 4-microphone array
            room.add_microphone_array(pra.MicrophoneArray(cfg.mic_location, room.fs))
            # place source to the coordinate
            x_source, y_source = geo.polar_to_cartesian(r, phi)
            room.add_source([cfg.room_dim[0] / 2. + x_source,
                             cfg.room_dim[1] / 2. + y_source,
                             cfg.human_height], signal=cfg.mls_signal)

            # compute image sources
            room.image_source_model(use_libroom=True)

            # visualize 3D polyhedron room and image sources
            fig, ax = room.plot(img_order=3)
            fig.set_size_inches(18.5, 10.5)
            ax.set_xlim([-1, cfg.room_dim[0] + 1])
            ax.set_ylim([-1, cfg.room_dim[1] + 1])
            ax.set_zlim([0, cfg.room_dim[2] + 1])
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            plt.show()

            # plot RIR impulse functions
            room.plot_rir()
            fig = plt.gcf()
            fig.set_size_inches(20, 10)
            plt.show()

            room.simulate()
            all_rir = []
            max_sz = 10000
            for rir_id in range(cfg.mic_n):
                all_rir.append(room.rir[rir_id][0][:max_sz])
            fname = os.path.join(rir_out_dir, 'ir_dist%.2f_degree%d.wav')
            soundfile.write(fname % (r, phi), np.array(all_rir).T, cfg.fs)

            print('(x, y): %.4f, %.4f' % (x_source, y_source))
            print('(r, phi): %.4f, %.4f' % (r, phi))
            del room
            del all_rir


def convolve(signal, ir):
    n, ch = ir.shape
    all_conv = np.array([])
    for c in range(ch):
        sig_conv = np.convolve(signal, ir[:, c], mode='full')
        all_conv = np.vstack([all_conv, sig_conv]) if all_conv.size else sig_conv
    return all_conv.T


rir_out = 'data/ir/pyroom/'
generate_room_impulse(cfg.azimuth, cfg.radius, rir_out)

fname = os.path.join(rir_out, 'ir_dist%.2f_degree%d.wav')
ir, fs = soundfile.read(fname % (0.50, 60))
assert fs == cfg.test_fs

conv_aud = convolve(cfg.test_signal, ir)
soundfile.write('test_ir.wav', conv_aud, cfg.test_fs)