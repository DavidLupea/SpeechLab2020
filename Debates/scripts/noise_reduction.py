import librosa
from pysndfx import AudioEffectsChain
import numpy as np
import math
import python_speech_features
import scipy as sp
from scipy import signal
from os import listdir
from os.path import isfile, join
import argparse
from tqdm import tqdm
import soundfile


def read_file(file_name):
    # sample_file = file_name
    # sample_directory = '00_samples/'
    # sample_path = sample_directory + sample_file

    # generating audio time series and a sampling rate (int)
    y, sr = librosa.load(file_name)

    return y, sr


def reduce_noise_power(y, sr):

    cent = librosa.feature.spectral_centroid(y=y, sr=sr)

    threshold_h = round(np.median(cent))*1.5
    threshold_l = round(np.median(cent))*0.1

    less_noise = AudioEffectsChain().lowshelf(gain=-30.0, frequency=threshold_l, slope=0.8).highshelf(gain=-12.0, frequency=threshold_h, slope=0.5)#.limiter(gain=6.0)
    y_clean = less_noise(y)

    return y_clean

def reduce_noise_centroid_s(y, sr):

    cent = librosa.feature.spectral_centroid(y=y, sr=sr)

    threshold_h = np.max(cent)
    threshold_l = np.min(cent)

    less_noise = AudioEffectsChain().lowshelf(gain=-12.0, frequency=threshold_l, slope=0.5).highshelf(gain=-12.0, frequency=threshold_h, slope=0.5).limiter(gain=6.0)

    y_cleaned = less_noise(y)

    return y_cleaned

def reduce_noise_centroid_mb(y, sr):

    cent = librosa.feature.spectral_centroid(y=y, sr=sr)

    threshold_h = np.max(cent)
    threshold_l = np.min(cent)

    less_noise = AudioEffectsChain().lowshelf(gain=-30.0, frequency=threshold_l, slope=0.5).highshelf(gain=-30.0, frequency=threshold_h, slope=0.5).limiter(gain=10.0)
    # less_noise = AudioEffectsChain().lowpass(frequency=threshold_h).highpass(frequency=threshold_l)
    y_cleaned = less_noise(y)


    cent_cleaned = librosa.feature.spectral_centroid(y=y_cleaned, sr=sr)
    columns, rows = cent_cleaned.shape
    boost_h = math.floor(rows/3*2)
    boost_l = math.floor(rows/6)
    boost = math.floor(rows/3)

    # boost_bass = AudioEffectsChain().lowshelf(gain=20.0, frequency=boost, slope=0.8)
    boost_bass = AudioEffectsChain().lowshelf(gain=16.0, frequency=boost_h, slope=0.5)#.lowshelf(gain=-20.0, frequency=boost_l, slope=0.8)
    y_clean_boosted = boost_bass(y_cleaned)

    return y_clean_boosted

def reduce_noise_mfcc_down(y, sr):

    hop_length = 512

    ## librosa
    # mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
    # librosa.mel_to_hz(mfcc)

    ## mfcc
    mfcc = python_speech_features.base.mfcc(y)
    mfcc = python_speech_features.base.logfbank(y)
    mfcc = python_speech_features.base.lifter(mfcc)

    sum_of_squares = []
    index = -1
    for r in mfcc:
        sum_of_squares.append(0)
        index = index + 1
        for n in r:
            sum_of_squares[index] = sum_of_squares[index] + n**2

    strongest_frame = sum_of_squares.index(max(sum_of_squares))
    hz = python_speech_features.base.mel2hz(mfcc[strongest_frame])

    max_hz = max(hz)
    min_hz = min(hz)

    speech_booster = AudioEffectsChain().highshelf(frequency=min_hz*(-1)*1.2, gain=-12.0, slope=0.6).limiter(gain=8.0)
    y_speach_boosted = speech_booster(y)

    return (y_speach_boosted)

def reduce_noise_mfcc_up(y, sr):

    hop_length = 512

    ## librosa
    # mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
    # librosa.mel_to_hz(mfcc)

    ## mfcc
    mfcc = python_speech_features.base.mfcc(y)
    mfcc = python_speech_features.base.logfbank(y)
    mfcc = python_speech_features.base.lifter(mfcc)

    sum_of_squares = []
    index = -1
    for r in mfcc:
        sum_of_squares.append(0)
        index = index + 1
        for n in r:
            sum_of_squares[index] = sum_of_squares[index] + n**2

    strongest_frame = sum_of_squares.index(max(sum_of_squares))
    hz = python_speech_features.base.mel2hz(mfcc[strongest_frame])

    max_hz = max(hz)
    min_hz = min(hz)

    speech_booster = AudioEffectsChain().lowshelf(frequency=min_hz*(-1), gain=12.0, slope=0.5)#.highshelf(frequency=min_hz*(-1)*1.2, gain=-12.0, slope=0.5)#.limiter(gain=8.0)
    y_speach_boosted = speech_booster(y)

    return (y_speach_boosted)

def reduce_noise_median(y, sr):
    y = sp.signal.medfilt(y,3)
    return (y)


def trim_silence(y):
    y_trimmed, index = librosa.effects.trim(y, top_db=20, frame_length=2, hop_length=500)
    trimmed_length = librosa.get_duration(y) - librosa.get_duration(y_trimmed)

    return y_trimmed, trimmed_length


def enhance(y):
    apply_audio_effects = AudioEffectsChain().lowshelf(gain=10.0, frequency=260, slope=0.1).reverb(reverberance=25, hf_damping=5, room_scale=5, stereo_depth=50, pre_delay=20, wet_gain=0, wet_only=False)#.normalize()
    y_enhanced = apply_audio_effects(y)

    return y_enhanced

def output_file(destination ,filename, y, sr, ext=""):
    destination = destination + filename.split("/")[-1][:-4] + ext + '.wav'
    # librosa.output.write_wav(destination, y, sr)
    soundfile.write(destination, y, sr, subtype='PCM_16')


if __name__ == "__main__":
    samples = ['01_counting.m4a','02_wind_and_cars.m4a','03_truck.m4a','04_voices.m4a','05_ambeint.m4a','06_office.m4a']
    ap = argparse.ArgumentParser()
    ap.add_argument("-b", "--audio_path",
                    default="../audio_clips",
                    help="downsample or upsample")
    args = vars(ap.parse_args())
    samples = [join(args["audio_path"], f) for f in listdir(args["audio_path"]) if isfile(join(args["audio_path"], f)) and f.endswith(".mp3")]
    for s in tqdm(samples):
        # reading a file
        filename = s
        y, sr = read_file(filename)

        # reducing noise using db power
        y_reduced_power = reduce_noise_power(y, sr)
        y_reduced_centroid_s = reduce_noise_centroid_s(y, sr)
        y_reduced_centroid_mb = reduce_noise_centroid_mb(y, sr)
        y_reduced_mfcc_up = reduce_noise_mfcc_up(y, sr)
        y_reduced_mfcc_down = reduce_noise_mfcc_down(y, sr)
        y_reduced_median = reduce_noise_median(y, sr)

        # trimming silences
        y_reduced_power, time_trimmed = trim_silence(y_reduced_power)
        # print (time_trimmed)

        y_reduced_centroid_s, time_trimmed = trim_silence(y_reduced_centroid_s)
        # print (time_trimmed)

        y_reduced_power, time_trimmed = trim_silence(y_reduced_power)
        # print (time_trimmed)

        y_reduced_centroid_mb, time_trimmed = trim_silence(y_reduced_centroid_mb)
        # print (time_trimmed)

        y_reduced_mfcc_up, time_trimmed = trim_silence(y_reduced_mfcc_up)
        # print (time_trimmed)

        y_reduced_mfcc_down, time_trimmed = trim_silence(y_reduced_mfcc_down)
        # print (time_trimmed)

        y_reduced_median, time_trimmed = trim_silence(y_reduced_median)

        # generating output file [1]

        output_file('../pwr/' ,filename, y_reduced_power, sr, '_pwr')
        output_file('../ctr_s/' ,filename, y_reduced_centroid_s, sr, '_ctr_s')
        output_file('../ctr_mb/' ,filename, y_reduced_centroid_mb, sr, '_ctr_mb')
        output_file('../mfcc_up/' ,filename, y_reduced_mfcc_up, sr, '_mfcc_up')
        output_file('../mfcc_down/' ,filename, y_reduced_mfcc_down, sr, '_mfcc_down')
        output_file('../median/' ,filename, y_reduced_median, sr, '_median')
        output_file('../org/' ,filename, y, sr, '_org')
