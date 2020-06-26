import pickle
import pyannote.core
import os

obj = pickle.load(open("demos/E17SF01_speech.pkl", 'rb'))

def generate_formatted_list(obj):
    # Takes pickle object and creates a formatted list of most likely speech intervals.
    times = [0]
    for a in obj:
        if a.duration < 6:
            if times[-1] != 0:
                times.append(0)
        else:
            times.append(a.start)
            times.append(a.end)
    return times

def get_interval_list(formatted):
    speaker_intervals = []
    zeroes = []
    counter = 0
    while True:
        try:
            zeroes.append([i for i, n in enumerate(formatted) if n == 0][counter])
            counter += 1
        except:
            break
    # print(zeroes)
    for i in range(0, len(zeroes) - 1):
        if formatted[zeroes[i + 1] - 1] - formatted[zeroes[i] + 1] > 60:
        #Ensures it's not long clapping
            speaker_intervals.append([formatted[zeroes[i] + 1], formatted[zeroes[i + 1] - 1]])
    return speaker_intervals

def spliceaudio(fname, intervals):
    for i in range(len(intervals)):
        print(fname + " splicing speaker #" + str(i))
        print(intervals[i])
        os.system("ffmpeg -ss " + str(intervals[i][0]) + " -t " + str(intervals[i][1] - intervals[i][0]) + " -i " + os.getcwd() + "/demos/" + fname + ".mp3 " + os.getcwd() + "/outputs/" + fname + "_" + str(i) + ".mp3")
formatted = generate_formatted_list(obj)
intervals = get_interval_list(formatted)
spliceaudio("E17SF01", intervals)
# ffmpeg -ss 00:00:00 -t 00:01:11 -i demos/E17SF01.mp3 output.mp3
