import glob, os
import argparse
import re
from pathlib import Path
import nltk
from nltk import tokenize

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="directory to clean and concatenate")
args = parser.parse_args()
dir = args.dir
os.chdir(dir)

Path("conc").mkdir(parents=True, exist_ok=True)

cur_transcript = ""
cur_out = ""
file_set = set()
for file in glob.glob("*.txt"):
    transcript = file.split("_")[0]
    print(transcript)
    if transcript not in file_set:
        if cur_transcript != "":
            out_file = open("/root/SpeechLab2020/Debates/" + cur_transcript + ".txt", "w")
            for s in tokenize.sent_tokenize(cur_out):
                out_file.write("%s\n" % s)
        cur_transcript = transcript
        cur_out = ""
    file_set.add(transcript)
    with open(file, "r") as file:
        seg = file.read()
        seg = re.sub(r"^\[INAUDIBLE\s\d{2}:\d{2}:\d{2}\]$", "aa", seg)
        seg = re.sub(r"^\[laughter\]$", "", seg)
        seg = re.sub("Etc.", "", seg)
        cur_out += seg + "\n"
