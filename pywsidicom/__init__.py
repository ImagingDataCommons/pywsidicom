import weakref
from cffi import FFI
from .version import __version__

ffi = FFI()

print(f"opening libdicom ...")
dicom_lib = ffi.dlopen("libdicom.so")

ffi.cdef('''
void dcm_init(void);
const char *dcm_get_version(void);

typedef struct _DcmError DcmError;
typedef struct _DcmFilehandle DcmFilehandle;
typedef struct _DcmDataSet DcmDataSet;
typedef struct _DcmSequence DcmSequence;
typedef struct _DcmElement DcmElement;
typedef struct _DcmFrame DcmFrame;

const char *dcm_error_code_str(int code);
const char *dcm_error_code_name(int code);
void dcm_error_clear(DcmError **error);
const char *dcm_error_get_summary(DcmError *error);
const char *dcm_error_get_message(DcmError *error);
int dcm_error_get_code(DcmError *error);

void *dcm_calloc(DcmError **error, uint64_t n, uint64_t size);
void dcm_free(void *pointer);

DcmFilehandle *dcm_filehandle_create_from_file(DcmError **error,
                                               const char *filepath);
void dcm_filehandle_destroy(DcmFilehandle *filehandle);

DcmDataSet *dcm_filehandle_get_file_meta(DcmError **error,
                                         DcmFilehandle *filehandle);
DcmDataSet *dcm_filehandle_get_metadata(DcmError **error,
                                        DcmFilehandle *filehandle);
bool dcm_filehandle_read_pixeldata(DcmError **error, DcmFilehandle *filehandle);
DcmFrame *dcm_filehandle_read_frame(DcmError **error,
                                    DcmFilehandle *filehandle,
                                    uint32_t frame_number);
DcmFrame *dcm_filehandle_read_frame_position(DcmError **error,
                                             DcmFilehandle *filehandle,
                                             uint32_t column,
                                             uint32_t row);

const char *dcm_dict_keyword_from_tag(uint32_t tag);
uint32_t dcm_dict_tag_from_keyword(const char *keyword);
int dcm_dict_vr_from_str(const char *vr);
const char *dcm_dict_str_from_vr(int vr);

int dcm_dataset_count(DcmDataSet *dataset);
void dcm_dataset_copy_tags(const DcmDataSet *dataset, uint32_t *tags, uint32_t n);
DcmElement *dcm_dataset_contains(const DcmDataSet *dataset, uint32_t tag);
void dcm_dataset_destroy(DcmDataSet *dataset);

uint32_t dcm_element_get_tag(const DcmElement *element);
int dcm_element_get_vr(const DcmElement *element);
int dcm_dict_vr_class(int vr);
uint32_t dcm_element_get_vm(const DcmElement *element);
uint32_t dcm_element_get_length(const DcmElement *element);
char *dcm_element_value_to_string(const DcmElement *element);
bool dcm_element_get_value_integer(DcmError **error,
                                   const DcmElement *element,
                                   uint32_t index,
                                   int64_t *value);
bool dcm_element_get_value_decimal(DcmError **error,
                                   const DcmElement *element,
                                   uint32_t index,
                                   double *value);
bool dcm_element_get_value_string(DcmError **error,
                                  const DcmElement *element,
                                  uint32_t index,
                                  const char **value);
bool dcm_element_get_value_binary(DcmError **error,
                                  const DcmElement *element,
                                  const char **value);
bool dcm_element_get_value_sequence(DcmError **error,
                                    const DcmElement *element,
                                    DcmSequence **value);

void dcm_sequence_destroy(DcmSequence *seq);
uint32_t dcm_sequence_count(const DcmSequence *seq);
DcmDataSet *dcm_sequence_get(DcmError **error,
                             const DcmSequence *seq, uint32_t index);

void dcm_frame_destroy(DcmFrame *frame);
uint32_t dcm_frame_get_number(const DcmFrame *frame);
uint32_t dcm_frame_get_length(const DcmFrame *frame);
uint16_t dcm_frame_get_rows(const DcmFrame *frame);
uint16_t dcm_frame_get_columns(const DcmFrame *frame);
uint16_t dcm_frame_get_samples_per_pixel(const DcmFrame *frame);
uint16_t dcm_frame_get_bits_allocated(const DcmFrame *frame);
uint16_t dcm_frame_get_bits_stored(const DcmFrame *frame);
uint16_t dcm_frame_get_high_bit(const DcmFrame *frame);
uint16_t dcm_frame_get_pixel_representation(const DcmFrame *frame);
uint16_t dcm_frame_get_planar_configuration(const DcmFrame *frame);
const char *dcm_frame_get_photometric_interpretation(const DcmFrame *frame);
const char *dcm_frame_get_transfer_syntax_uid(const DcmFrame *frame);
const char *dcm_frame_get_value(const DcmFrame *frame);

''')

print(f"init for libdicom ...")
dicom_lib.dcm_init()

# we track references which we must keep alive here
reference_dict = weakref.WeakKeyDictionary()

def _to_string(x):
    """Convert to a unicode string.

    If x is a byte string, assume it is utf-8 and decode to a Python unicode
    string. You must call this on text strings you get back from libvips.

    """
    if x == ffi.NULL:
        x = 'NULL'
    else:
        x = ffi.string(x)
        if isinstance(x, bytes):
            x = x.decode('utf-8')

    return x


def _to_bytes(x):
    """Convert to a byte string.

    Convert a Python unicode string or a pathlib.Path to a utf-8-encoded
    byte string. You must call this on strings you pass to libvips.

    """
    if isinstance(x, str):
        # n.b. str also converts pathlib.Path objects
        x = str(x).encode('utf-8')

    return x


def version():
    """Get the libdicom version.

    As a x.y.z semantic version string.

    """
    return _to_string(dicom_lib.dcm_get_version())


print(f"libdicom version: {version()}")

from .error import *
from .enums import *
from .vr import *
from .tag import *
from .element import *
from .dataset import *
from .sequence import *
from .filehandle import *
from .frame import *
