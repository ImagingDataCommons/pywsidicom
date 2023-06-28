import pywsidicom
from pywsidicom import ffi, dicom_lib, _to_string, _to_bytes

"""
usage:
        error = pywsidicom.Error()
        pointer = dicom_lib.dcm_filehandle_create_from_file(error.pointer,
                                                            _to_bytes(filename))
        if pointer == ffi.NULL:
            raise Error(error)
"""


def error_free(pointer):
    if pointer[0] != ffi.NULL:
        dicom_lib.dcm_error_clear(pointer)

class Error():
    """This class manages a single pointer which can be passed to functions
    taking a DcmError**.

    On creation, we init the pointer to NULL. On destruction, we free any
    error object held by the pointer. Methods get the error message and code.

    """

    def __init__(self):
        # allocate space for a single DcmError* pointer and set it to NULL
        pointer = ffi.new("DcmError**")
        self.pointer = ffi.gc(pointer, error_free)

    @staticmethod
    def str_from_error_code(code):
        return _to_string(dicom_lib.dcm_error_code_str(code))

    @staticmethod
    def name_from_error_code(code):
        return _to_string(dicom_lib.dcm_error_code_name(code))

    def summary(self):
        if self.pointer[0] == ffi.NULL:
            return ""

        return _to_string(dicom_lib.dcm_error_get_summary(self.pointer[0]))

    def message(self):
        if self.pointer[0] == ffi.NULL:
            return ""

        return _to_string(dicom_lib.dcm_error_get_message(self.pointer[0]))

    def code(self):
        if self.pointer[0] == ffi.NULL:
            return 0

        return dicom_lib.dcm_error_get_code(self.pointer[0])

    def exception(self):
        code = Error.str_from_error_code(self.code())
        message = f"{code}: {self.summary()} - {self.message()}"
        return Exception(message)

