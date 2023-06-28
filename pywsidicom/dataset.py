import pywsidicom
from pywsidicom import ffi, dicom_lib, _to_string, _to_bytes

class DataSet:
    def __init__(self, pointer, steal=False):
        # record the pointer we were given to manage
        # if steal is set, destroy on GC
        if steal:
            self.pointer = ffi.gc(pointer, dicom_lib.dcm_dataset_destroy)
        else:
            self.pointer = pointer

        return 

    def __repr__(self):
        return f"<DataSet of {self.count()} items>"

    def count(self):
        return dicom_lib.dcm_dataset_count(self.pointer)

    def tags(self):
        n = self.count()
        int_tags = ffi.new(f"uint32_t[{n}]")
        dicom_lib.dcm_dataset_copy_tags(self.pointer, int_tags, n)

        return [pywsidicom.Tag(tag) for tag in int_tags]

    def _contains(self, tag):
        if isinstance(tag, pywsidicom.Tag):
            tag = tag.value

        return dicom_lib.dcm_dataset_contains(self.pointer, tag)

    def contains(self, tag):
        pointer = self._contains(tag)
        return pointer != ffi.NULL

    def get(self, tag):
        pointer = self._contains(tag)
        if pointer == ffi.NULL:
            raise Exception(f"dataset does not contain tag {tag}")

        return pywsidicom.Element(pointer)






