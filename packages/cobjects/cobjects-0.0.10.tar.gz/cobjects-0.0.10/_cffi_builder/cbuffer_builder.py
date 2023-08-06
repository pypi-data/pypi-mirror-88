# file "example_build.py"

# Note: we instantiate the same 'cffi.FFI' class as in the previous
# example, but call the result 'ffibuilder' now instead of 'ffi';
# this is to avoid confusion with the other 'ffi' object you get below

from cffi import FFI
ffibuilder = FFI()

ffibuilder.set_source("cobjects._cbuffer",
    r"""
    #include "cbuffer.h"
    """,
    include_dirs=['src/'],
    sources=['src/cbuffer.c'],
    libraries=[])   # or a list of libraries to link with

ffibuilder.cdef("""
    void print_info(void *);
""")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)

