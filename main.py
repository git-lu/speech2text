#!/usr/bin/python

from getTranscript import GetTranscript
import sys
import os

# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)

# Arguments passed
print("\nName of Python script:", sys.argv[0])

video_filepath = sys.argv[1]
video_filename = os.path.basename(video_filepath)

dest_filepath = 'transcriptions/' + video_filename + '.txt'

print(f"\nClip url: {video_filepath}")
print(f"\nTranscript destination file: {dest_filepath}")

transcriptor = GetTranscript()
transcriptor.process(video_filepath, dest_filepath)
