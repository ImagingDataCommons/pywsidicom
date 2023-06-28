#!/usr/bin/env python

import sys
import pywsidicom

file = pywsidicom.Filehandle.create_from_file(sys.argv[1])
metadata = file.get_metadata()
num_frames_tag = pywsidicom.Tag.create_from_keyword("NumberOfFrames")
num_frames = int(metadata.get(num_frames_tag).get_value()[0])
for frame_number in range(1, num_frames + 1):
    frame = file.read_frame(frame_number)
    value = frame.get_value()
    print(f"frame {frame_number} -> {frame} {len(value)} bytes")
