import glob, os
import argparse
import re
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="directory to clean and concatenate")
parser.add_argument("tdir", help="transcript dir")
args = parser.parse_args()
dir = args.dir

Path("../" + dir + "_maps").mkdir(parents=True, exist_ok=True)

os.chdir(dir)

for file in glob.glob("*.mp3"):
    f = file.split(".")[0]

    transcript = "../"+args.tdir+f+"zz.txt"
    command = 'python3 -m aeneas.tools.execute_task ' + "'" + file + "'" + " " + transcript + \
        ' "task_language=eng|os_task_file_format=json|is_text_type=plain" ' + f + 'map.json'
    print(command)
    os.system(command)
