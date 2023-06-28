import pywsidicom
from pywsidicom import ffi, dicom_lib, _to_string, _to_bytes

class Sequence:
    def __init__(self, pointer, steal=False):
        # record the pointer we were given to manage
        # if steal is set, destroy on GC
        if steal:
            self.pointer = ffi.gc(pointer, dicom_lib.dcm_sequence_destroy)
        else:
            self.pointer = pointer

        return 

    def __repr__(self):
        return f"<Sequence of {self.count()} items>"

    def count(self):
        return dicom_lib.dcm_sequence_count(self.pointer)

    def get(self, index):
        error = pywsidicom.Error()
        pointer = dicom_lib.dcm_sequence_get(error.pointer, self.pointer, index)
        if pointer == ffi.NULL:
            raise error.exception()

        return pywsidicom.DataSet(pointer)






