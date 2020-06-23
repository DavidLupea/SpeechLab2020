import re
import os
import pickle

def reformat_transcript(fname):
    f_in = open("demos/" + fname)
    seg = f_in.read()
    seg = re.sub(r'\[[A-Za-z]*\]', '', seg)
    seg = re.sub(r"^\[INAUDIBLE\s\d{2}:\d{2}:\d{2}\]$", "aa", seg)
    seg = re.sub(r"^\[laughter\]$", "", seg)
    seg = re.sub(r"Audience\d+: ", "", seg)
    seg = re.sub(r"Speaker\d+: ", "", seg)
    seg = re.sub(r"Announcement: ", "", seg)
    seg = re.sub(r"\n", "", seg)

    portions = re.split(",.", seg)

    f_out = open("outputs/" + fname.split(".")[0] + "_cleaned.txt", "w")
    f_out.write("1\n")

    for a in portions:
        f_out.write(a + "\n")
    f_out.write(seg)

def reformat_batch(dir, debate_name):
    files = os.listdir(dir)
    speaker_transcripts = re.findall(debate_name + "_S" + r'\d_\D.txt', str(files))
    for x in speaker_transcripts:
        print("Reformatting: " + x)
        reformat_transcript(x)

def batch_align(dir, debate_name):
    files = os.listdir(dir)

    for i in range(1, 9):
        cur_txt_file = re.findall(debate_name + "_S" + str(i) + r'_\D_cleaned.txt', str(files))[0]
        cur_audio_file = debate_name + "_" + str(i - 1) + ".mp3"
        print("DEBATE: " + debate_name + "; SPEAKER: " + str(i))

        os.system('python3 -m aeneas.tools.execute_task ' + dir + cur_audio_file + ' ' + dir + cur_txt_file + ' "task_language=eng|os_task_file_format=json|is_text_type=plain" ' + dir +  debate_name + "_S" + str(i) +'_map.json')

# reformat_batch("demos/", "E17SF01")
batch_align("outputs/", "E17SF01")
