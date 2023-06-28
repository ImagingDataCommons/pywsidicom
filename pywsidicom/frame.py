import pywsidicom
from pywsidicom import ffi, dicom_lib, _to_string, _to_bytes, reference_dict

class Frame:
    def __init__(self, pointer, steal=False):
        # record the pointer we were given to manage
        # if steal is set, destroy on GC
        if steal:
            self.pointer = ffi.gc(pointer, dicom_lib.dcm_frame_destroy)
        else:
            self.pointer = pointer

        return 

    def __repr__(self):
        return f"<{self.columns()}x{self.rows()} pixels, " + \
               f"{self.bits_stored()} bits, " + \
               f"{self.samples_per_pixel()} bands, " + \
               f"{self.photometric_interpretation()}>"

    def number(self):
        return dicom_lib.dcm_frame_get_number(self.pointer)

    def length(self):
        return dicom_lib.dcm_frame_get_length(self.pointer)

    def rows(self):
        return dicom_lib.dcm_frame_get_rows(self.pointer)

    def columns(self):
        return dicom_lib.dcm_frame_get_columns(self.pointer)

    def samples_per_pixel(self):
        return dicom_lib.dcm_frame_get_samples_per_pixel(self.pointer)

    def bits_allocated(self):
        return dicom_lib.dcm_frame_get_bits_allocated(self.pointer)

    def bits_stored(self):
        return dicom_lib.dcm_frame_get_bits_stored(self.pointer)

    def high_bit(self):
        return dicom_lib.dcm_frame_get_high_bit(self.pointer)

    def pixel_representation(self):
        return dicom_lib.dcm_frame_get_pixel_representation(self.pointer)

    def planar_configuration(self):
        return dicom_lib.dcm_frame_get_planar_configuration(self.pointer)

    def photometric_interpretation(self):
        cstr = dicom_lib.dcm_frame_get_photometric_interpretation(self.pointer)
        return _to_string(cstr)

    def transfer_syntax_uid(self):
        cstr = dicom_lib.dcm_frame_get_transfer_syntax_uid(self.pointer)
        return _to_string(cstr)

    def get_value(self):
        pointer = dicom_lib.dcm_frame_get_value(self.pointer)
        length = self.length()
        return ffi.buffer(pointer, length)



