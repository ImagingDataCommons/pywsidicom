#!/usr/bin/env python

import sys
import pywsidicom

def print_sequence(seq, indent=0):
    for index in range(0, seq.count()):
        print(f"{' '*indent}-- Item #{index} --")
        print_dataset(seq.get(index), indent + 2)

def print_dataset(dataset, indent=0):
    for tag in dataset.tags():
        element = dataset.get(tag)
        print(f"{' '*indent}{element}")
        if element.vr_class() == pywsidicom.VRClass.SEQUENCE:
            seq = element.get_value()
            print_sequence(seq, indent + 2)

file = pywsidicom.Filehandle.create_from_file(sys.argv[1])
file_meta = file.get_file_meta()
print(f"===File Meta Information===")
print_dataset(file_meta)

metadata = file.get_metadata()
print(f"===Dataset===")
print_dataset(metadata)

