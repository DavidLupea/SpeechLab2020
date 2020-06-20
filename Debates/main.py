import re

import pickle

# obj = pickle.load(open("demos/E17SF01_part.pkl", 'rb'))  Unsupported pickle type 3
obj = pickle.load(open("demos/E17SF01_speech.pkl", 'rb'))
print(obj)

# First 1:11 of video only speaker 1
#ffmpeg -ss 00:00:00 -t 00:01:11 -i demos/E17SF01.mp3 output.mp3
# python3 -m aeneas.tools.execute_task demos/E17SF01.mp3 outputs/cleaned_transcript.txt "task_language=eng|os_task_file_format=json|is_text_type=plain" map.json

def formatfile(fname):
    # "outputs/speaker1_first.txt"
    f = open(fname)
    text = f.read()

    portions = re.split(",.", text)

    f2 = open(fname, "w")
    f2.write("1\n")
    for a in portions:
        f2.write(a + "\n")

def reformat_transcript(fname):
    f_in = open(fname)
    seg = f_in.read()
    seg = re.sub(r'\[[A-Za-z]*\]', '', seg)
    seg = re.sub(r"^\[INAUDIBLE\s\d{2}:\d{2}:\d{2}\]$", "aa", seg)
    seg = re.sub(r"^\[laughter\]$", "", seg)
    seg = re.sub(r"Audience\d+: ", "", seg)
    seg = re.sub(r"Speaker\d+: ", "", seg)
    seg = re.sub(r"Announcement: ", "", seg)
    seg = re.sub(r"\n", "", seg)

    portions = re.split(",.", seg)

    f_out = open("outputs/cleaned_transcript.txt", "w")
    f_out.write("1\n")

    for a in portions:
        f_out.write(a + "\n")
    f_out.write(seg)

# reformat_transcript("demos/E17SF01.txt")
