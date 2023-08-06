#include "stdio.h"
#include "stdlib.h"



#if defined(__CUDACC__) // NVCC
#define MY_ALIGN(n) __align__(n)
#elif defined(__GNUC__) || defined(__clang__) // GCC, CLANG
#define MY_ALIGN(n) __attribute__((aligned(n)))
#elif defined(_MSC_VER) || defined(__INTEL_COMPILER) // MSVC, INTEL
#define MY_ALIGN(n) __declspec(align(n))
#else
#error "Please provide a definition for MY_ALIGN macro for your host compiler!"


#endif

typedef struct MY_ALIGN(512) {
    size_t base MY_ALIGN(512);
    size_t size;
    size_t size_header;
    size_t *slots;
    size_t *objects;
    size_t *pointers;
    size_t *garbage;
} CBuffer;

void print_info(CBuffer *buff);



