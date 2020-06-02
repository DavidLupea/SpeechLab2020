import re

# First 1:11 of video only speaker 1

#ffmpeg -ss 00:00:00 -t 00:01:11 -i demos/E17SF01.mp3 output.mp3

# python3 -m aeneas.tools.execute_task output.mp3 demos/speaker1_first.txt "task_language=eng|os_task_file_format=json|is_text_type=plain" map.json

f = open("demos/speaker1_first.txt")
text = f.read()

portions = re.split(",.", text)

f2 = open("demos/speaker1_first.txt", "w")
f2.write("1\n")
for a in portions:
    f2.write(a + "\n")
