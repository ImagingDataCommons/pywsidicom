import pywsidicom
from pywsidicom import ffi, dicom_lib, _to_string, _to_bytes

class VR:
    def __init__(self, value):
        self.value = value

    @staticmethod
    def create_from_name(name):
        value = dicom_lib.dcm_dict_vr_from_str(_to_bytes(name))
        if value == -1:
            raise Exception(f"Unknown VR '{name}'")
        return VR(value)

    def name(self):
        return _to_string(dicom_lib.dcm_dict_str_from_vr(self.value))

    def __repr__(self):
        return self.name()

