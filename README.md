# pywsidicom

This is a tiny, experimental binding for
[libdicom](https://github.com/jcupitt/libdicom). This is a DICOM read
library focused on Whole Slide Imaging (WSI). It should be fast, and only
needs a little memory.

This binding was made to validate the libdicom API. It is not supposed to
be ready for production! There are plenty of obvious missing features and
useful enhancements.

Having said that, it does work, performs well, has no known memory leaks,
and supports the whole libdicom file read API.

# Thanks

Development of this library was supported by [NCI Imaging Data
Commons](https://imaging.datacommons.cancer.gov/), and has been funded in
whole or in part with Federal funds from the National Cancer Institute,
National Institutes of Health, under Task Order No. HHSN26110071 under
Contract No. HHSN261201500003l.

# Read frames

See `read-frames.py`:

```python
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
```

Prints:

```
$ ./read-frames.py sm_image.dcm 
opening libdicom ...
init for libdicom ...
libdicom version: 1.0.0
frame 1 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 2 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 3 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 4 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 5 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 6 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 7 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 8 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 9 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 10 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 11 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 12 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 13 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 14 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 15 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 16 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 17 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 18 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 19 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 20 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 21 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 22 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 23 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 24 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
frame 25 -> <10x10 pixels, 8 bits, 3 bands, RGB> 300 bytes
```

# Print metadata

See `print-metadata.py`:

```python
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
```

Prints:

```
$ ./print-metadata.py sm_image.dcm 
opening libdicom ...
init for libdicom ...
libdicom version: 1.0.0
===File Meta Information===
(0002,0001) FileMetaInformationVersion | OB | 2 | 1 | 00 01 
(0002,0002) MediaStorageSOPClassUID | UI | 30 | 1 | 1.2.840.10008.5.1.4.1.1.77.1.6
(0002,0003) MediaStorageSOPInstanceUID | UI | 64 | 1 | 1.2.826.0.1.3680043.9.7433.3.12857516184849951143044513877282227
(0002,0010) TransferSyntaxUID | UI | 20 | 1 | 1.2.840.10008.1.2.1
(0002,0012) ImplementationClassUID | UI | 28 | 1 | 1.2.826.0.1.3680043.9.7433.1
(0002,0013) ImplementationVersionName | SH | 14 | 1 | wsiget v0.0.1
===Dataset===
(0008,0008) ImageType | CS | 28 | 4 | [ORIGINAL, PRIMARY, VOLUME, NONE]
(0008,0016) SOPClassUID | UI | 30 | 1 | 1.2.840.10008.5.1.4.1.1.77.1.6
(0008,0018) SOPInstanceUID | UI | 64 | 1 | 1.2.826.0.1.3680043.9.7433.3.12857516184849951143044513877282227
(0008,0020) StudyDate | DA | 8 | 1 | 20190604
(0008,0023) ContentDate | DA | 8 | 1 | 20190822
(0008,002a) AcquisitionDateTime | DT | 14 | 1 | 20091229095915
(0008,0030) StudyTime | TM | 6 | 1 | 101000
(0008,0033) ContentTime | TM | 6 | 1 | 113618
(0008,0050) AccessionNumber | SH | 12 | 1 | S19-1_A_1_1
(0008,0051) IssuerOfAccessionNumberSequence | SQ | 34 | 1 | <sequence>
  -- Item #0 --
    (0040,0032) UniversalEntityID | UT | 30 | 1 | http://test.org/specimens/2019
    (0040,0033) UniversalEntityIDType | CS | 4 | 1 | URI
(0008,0060) Modality | CS | 2 | 1 | SM
(0008,0070) Manufacturer | LO | 18 | 1 | Test Manufacturer
(0008,0090) ReferringPhysicianName | PN | 14 | 1 | Test^Physician
(0008,1090) ManufacturerModelName | LO | 10 | 1 | Test Model
(0008,9206) VolumetricProperties | CS | 6 | 1 | VOLUME
...
```


