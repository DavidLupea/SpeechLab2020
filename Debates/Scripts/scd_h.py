import torch
import glob, os
import pickle

sad = torch.hub.load('pyannote/pyannote-audio', 'sad_ami')
scd = torch.hub.load('pyannote/pyannote-audio', 'scd_ami')

os.chdir("/proj/afosr/corpora/debates/h_audio_copy/H audio")
for file in glob.glob("*.wav"):
    print(file)
    test_file = {'uri': 'filename', 'audio': file}
    sad_scores = sad(test_file)
    from pyannote.audio.utils.signal import Binarize
    binarize = Binarize(offset=0.52, onset=0.52, log_scale=True,
                    min_duration_off=0.1, min_duration_on=0.1)
    speech = binarize.apply(sad_scores, dimension=1)
    f_out_speech = file.split('.')[0] + "_speech.pkl"
    pickle.dump(speech, open(f_out_speech, "wb"))

    scd_scores = scd(test_file)
    from pyannote.audio.utils.signal import Peak
    peak = Peak(alpha=0.10, min_duration=0.10, log_scale=True)
    partition = peak.apply(scd_scores, dimension=1)
    f_out_partition = file.split('.')[0] + "_part.pkl"
    pickle.dump(partition, open(f_out_partition, "wb"))

