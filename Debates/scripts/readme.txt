1. All the scd_[x].py files perform speaker change detection for the respective audio directories inside their copied directories.
It will produce a {file_name}_speech.pkl and a {file_name}_part.pkl for each audio file within these directories (refer to the
files to see which directories they modify). These are both Pyannote timeline objects, and the _part will be the one that 
you will need to apply rules to to refine speaker segments. No arguments.
2. clean.py produces concatenated text files for each of the separated transcripts for a transcript directory. Can be run by
"python /proj/afosr/corpora/debates/e_transcripts" for example. Removes all the [laughter] and [inaudible xx:xx:xx] tags as well.
3. compute_map.py takes two arguments: audio directory and transcript directory. Performs alignment using Aeneas. Does not consider
speaker segments, so will be continuous, which is why diarization is needed.
4. example_pyannote.ipynb is a sample notebook that provides an example of how to use pyannote with given files.
