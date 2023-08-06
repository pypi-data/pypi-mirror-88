"""Buffer

<<header>>
base   +   0: base,        pointer to self
base   +   8: size,        size in bytes
base   +  16: size_header, header size
base   +  24: p_slots,      pointer to slots
base   +  32: p_objects,   pointer to object list
base   +  40: p_pointers,  pointer to pointer list
base   +  48: p_garbage,   pointer to garbage list
<<slots>>
p_slots +   0: size_slots, maxsize in slots in bytes
p_slots +  16: n_slots, number of 64bit slot to slots
p_slots +  24: first slots slot
p_slots + ...:
<<objects>>
p_objects +   0: size_objects, maxsize in slots in bytes
p_objects +  16: n_objects, number of objects
p_objects +  24: pointer to first object
p_objects +  32: object type index
p_objects +  48: object size in bytes
...

object list:
    max size for object = 3*8*n of objects
    number of object
    pointer to start first object
    object type index
    object size in bytes
    pointer to start second object
    ...

pointer list:
    pointer

garbage list:
    pointer to start
    usable size in bytes
"""


import numpy as np

from ._cbuffer import ffi, lib


class fieldi64(object):
    __slots__ = ['offset', 'pref']

    def __init__(self, offset, pref=None):
        self.offset = offset
        self.pref = pref

    def get_idx(self, obj):
        index = self.offset
        if self.pref:
            index = index+getattr(obj, self.pref) - obj.base
        return index

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        else:
            idx = self.get_idx(obj)
            return int(obj._data[idx:idx+8].view('int64')[0])

    def __set__(self, obj, value):
        idx = self.get_idx(obj)
        view = obj._data[idx:idx+8].view('int64')
        view[0] = value


class viewi64(object):
    __slots__ = ['pref', 'length']

    def __init__(self, pref, length):
        self.pref = pref
        self.length = length

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        else:
            indexa = int(getattr(obj, self.pref)) - int(obj.base)
            indexb = indexa + int(getattr(obj, self.length))
            return obj._data[indexa:indexb].view('int64')


c_types = {'integer': 'int64',
           'real': 'float64'}


class CBuffer(object):
    HEADER = 112
    base = fieldi64(0)
    size = fieldi64(1*8)
    size_header = fieldi64(2*8)
    size_slots = fieldi64(0, 'p_slots')
    size_objects = fieldi64(0, 'p_objects')
    size_pointers = fieldi64(0, 'p_pointers')
    size_garbage = fieldi64(0, 'p_garbage')
    p_slots = fieldi64(3*8)
    p_objects = fieldi64(4*8)
    p_pointers = fieldi64(5*8)
    p_garbage = fieldi64(6*8)
    n_slots = fieldi64(1*8, 'p_slots')
    n_objects = fieldi64(1*8, 'p_objects')
    n_pointers = fieldi64(1*8, 'p_pointers')
    n_garbage = fieldi64(1*8, 'p_garbage')
    slots = viewi64('p_slots', 'size_slots')
    objects = viewi64('p_objects', 'size_objects')
    pointers = viewi64('p_pointers', 'size_pointers')
    garbage = viewi64('p_garbage', 'size_garbage')

    def __init__(self,
                 max_slots=1, max_objects=1,
                 max_pointers=0, max_garbage=0,
                 template=c_types,
                 data=None):
        self.typeids = {}
        self.template = template
        if data is None:
           self.allocate(max_slots, max_objects, max_pointers, max_garbage)
        else:
           self._data=data
           self._data_i64 = self._data.view('int64')

    def resolve_type(self, ftype):
        return self.template.get(ftype, ftype)

    @property
    def max_slots(self):
        return self.size_slots//8-2

    @property
    def max_objects(self):
        return (self.size_objects//8-2)//3

    @property
    def max_pointers(self):
        return self.size_pointers//8-2

    @property
    def max_garbage(self):
        return (self.size_garbage//8-2)//2

    def allocate(self, max_slots, max_objects, max_pointers, max_garbage):
        size_header = CBuffer.HEADER
        size_slots = (max_slots+2)*8
        size_objects = (max_objects*3+2)*8
        size_pointers = (max_pointers+2)*8
        size_garbage = (max_garbage*2+2)*8
        size = size_header+size_slots+size_objects+size_pointers+size_garbage
        self._data = np.zeros(size, dtype='uint8')
        self._data_i64 = self._data.view('int64')
        self.base = self._data.ctypes.data
        self.size = size
        self.size_header = CBuffer.HEADER
        self.p_slots = self.base+size_header
        self.size_slots = size_slots
        self.p_objects = self.p_slots+size_slots
        self.size_objects = size_objects
        self.p_pointers = self.p_objects+size_objects
        self.size_pointers = size_pointers
        self.p_garbage = self.p_pointers+size_pointers
        self.size_garbage = size_garbage
        self._cffi_pointer = ffi.cast('void *', self._data.ctypes.data)

    def free_slots(self):
        return self.size_slots//8-2-self.n_slots

    def free_objects(self):
        return self.size_objects//8-2-self.n_objects*3

    def free_pointers(self):
        return self.size_pointers//8-2-self.n_pointers

    def free_garbage(self):
        return self.size_garbage//8-2-self.n_garbage

    def reallocate(self, max_slots, max_objects, max_pointers, max_garbage):
        old_data_i64 = self._data_i64
        old_slots = self.slots
        old_objects = self.objects
        old_n_slots = self.n_slots
        old_n_objects = self.n_objects
        old_n_pointers = self.n_pointers
        old_n_garbage = self.n_garbage
        old_pointers = self.pointers
        old_garbage = self.garbage
        self.allocate(max_slots, max_objects, max_pointers, max_garbage)
        gap = self._data_i64[0]-old_data_i64[0]
        #copy old data
        self.slots[1:len(old_slots)] = old_slots[1:]
        self.objects[1:len(old_objects)] = old_objects[1:]
        self.pointers[1:len(old_pointers)] = old_pointers[1:]
        self.garbage[1:len(old_garbage)] = old_garbage[1:]
        self.shift_data_pointers(gap)

    def shift_data_pointers(self,gap):
        self.objects[2:2+3*self.n_objects:3] += gap
        self.pointers[2:self.n_pointers+2] += gap
        self.garbage[2:2*self.n_garbage:2] += gap
        for ptr in self.pointers[2:self.n_pointers+2]:
            self._data_i64[(ptr-self.base)//8] +=gap

    def check_pointers(self):
        base=self.base
        def check(lbl,val):
            print("%-15s %20d %20d"%(lbl,val-base,val))
        check("base",self._data_i64[0])
        check("slots",self._data_i64[3])
        check("objects" ,self._data_i64[4])
        check("pointers" ,self._data_i64[5])
        check("garbage" ,self._data_i64[6])
        for objid in range(self.n_objects):
            check("obj(%d)"%objid,self.get_object_address(objid))
        for ptrid in range(self.n_pointers):
            ptr=self.pointers[2+ptrid]
            check("ptr(%d)"%ptrid,ptr)
            ptr_data=self._data_i64[(ptr-self.base)//8]
            check("ptr_data(%d)"%ptrid,ptr_data)

    def next_object_address(self):
        return self.p_slots+(2+self.n_slots)*8

    def address_to_offset(self, address):
        return address - self.base

    def offset_to_address(self, offset):
        return self.base + offset

    def new_object(self, size, otype, pointer_list=[]):
        typeid = otype._typeid
        if typeid in self.typeids:
            if self.typeids[typeid] != otype:
                raise ValueError("Two types with same id")
        else:
            self.typeids[typeid] = otype
        realloc = False
        max_slots = self.max_slots
        max_objects = self.max_objects
        max_pointers = self.max_pointers
        max_garbage = self.max_garbage
        n_slots = self.n_slots
        n_objects = self.n_objects
        n_pointers = self.n_pointers
        n_garbage = self.n_garbage
        slots_needed = size//8+size % 8
        if self.free_slots() < slots_needed:
            max_slots = (n_slots+slots_needed)*2
            realloc = True
        if self.free_objects() < 1:
            max_objects = (n_objects+1)*2
            realloc = True
        if self.free_pointers() < len(pointer_list):
            max_pointers = (n_pointers+len(pointer_list))*2
            realloc = True
        if realloc:
            self.reallocate(max_slots, max_objects, max_pointers, max_garbage)
        p_object = self.p_slots+(2+self.n_slots)*8
        self.n_slots += slots_needed
        for p_address in pointer_list:
            self.pointers[2+self.n_pointers] = p_object + p_address
            self.n_pointers += 1
        idx_object = 2+self.n_objects*3
        self.objects[idx_object+0] = p_object
        self.objects[idx_object+1] = typeid
        self.objects[idx_object+2] = size
        self.n_objects += 1
        return p_object

    def get_object_buffer(self, objid):
        idx = 2+objid*3
        p_object = int(self.objects[idx])
        size = int(self.objects[idx+2])
        idx = p_object-self.base
        return self._data[idx:idx+size]

    def get_object_slots(self, objid):
        return get_object_buffer(objid).view('int64')

    def get_object_address(self, objid):
        idx = 2+objid*3
        p_object = int(self.objects[idx])
        return p_object

    def get_object_typeid(self, objid):
        idx = 2+objid*3
        typeid = int(self.objects[idx+1])
        return typeid

    def get_object_size(self, objid):
        idx = 2+objid*3
        size = int(self.objects[idx+2])
        return size

    def get_object(self,objid,cls=None):
        idx=2+objid*3
        ptr=self.objects[idx]
        typeid=self.objects[idx+1]
        if typeid in self.typeids and cls is None:
            cls=self.typeids[typeid]
        return cls(cbuffer=self,_offset=ptr-self.base)

    def get_objects(self):
        return [self.get_object(i) for i in range(self.n_objects)]

    def get_field(self, offset, ftype, fsize, length=None):
        if length is None:
            if hasattr(ftype, '_typeid'):
                return ftype(cbuffer=self, _offset=offset)
            else:
                return self._data[offset:offset+fsize].view(ftype)[0]
        else:
            if hasattr(ftype, '_typeid'):
                return [ftype(cbuffer=self,
                              _offset=offset+ii*fsize//length)
                        for ii in range(length)]
            else:
                return self._data[offset:offset+fsize].view(ftype)

    def set_field(self, offset, ftype, fsize, length, value):
        """offset: offset from beginning of buffer in bytes
        """
        data = self._data[offset:offset+fsize].view(ftype)
        if length is None:
            data[0] = value
        else:
            data[:] = value

    def to_ctypes(self):
        pass

    def to_cffi(self):
        return ffi.cast('void *', self._data.ctypes.data)

    def info(self):
        out = []

        def fmt(lst):
            return " ".join([f"{x:3}" for x in lst])
        for kk, vv in self.__class__.__dict__.items():
            if isinstance(vv, fieldi64):
                out.append(f"{kk:14} : {getattr(self,kk)}")
            if isinstance(vv, viewi64):
                vvv = getattr(self, kk)
                if len(vvv) > 13:
                    beg = fmt(vvv[:10])
                    end = fmt(vvv[-3:])
                    out.append(f"{kk:14} : {beg} ... {end}")
                else:
                    beg = fmt(vvv)
                    out.append(f"{kk:14} : {beg}")
        print("\n".join(out))

    def __repr__(self):
        return f"<CBuffer at {self.base}, {self.size} bytes>"

    def _test_cffilib(self):
        return lib.print_info(self._cffi_pointer)

    def tofile(self, filename):
        self._data.tofile(filename)


    @classmethod
    def fromfile(cls, filename):
        data=np.fromfile(filename,dtype='uint8')
        self=cls(data=data)
        old_base = self._data_i64[0]
        self._data_i64[0]=self._data.ctypes.data
        gap = self._data_i64[0]-old_base
        self._data_i64[3]+=gap
        self._data_i64[4]+=gap
        self._data_i64[5]+=gap
        self._data_i64[6]+=gap
        self.shift_data_pointers(gap)
        return self

CBuffer.c_types = c_types
