class CField(object):
    def __init__(self, index,
             ftype,default=None, const=False,
             length=None, pointer=False,
             alignment=8,
             setter=None):
        self.index = index
        self.ftype = ftype
        self.default =  default
        self.setter=setter
        self.length=length
        self.const=const
        self.pointer=pointer
        self.alignment=alignment
    def is_scalar(self):
        return isinstance(self.ftype,str)
    def get_length(self,nargs):
        if self.length is not None:
            length=self.length
            if isinstance(length,str):
               length=eval(length,{},nargs)
            return length
    def get_size(self,ftype,offset,nargs):
        if hasattr(ftype,'get_itemsize'):
            size=ftype.get_itemsize(nargs)
        else:
            size=ftype.itemsize
        length=self.get_length(nargs)
        if self.length is not None:
            size*=length
        return size
    def _field_getter(self,obj):
        offset=obj._offsets[self.index]
        ftype=obj._ftypes[self.index]
        fsize=obj._fsizes[self.index]
        length=obj._flength[self.index]
        return obj._buffer.get_field(offset,ftype,fsize,length)
    def _field_setter(self,obj,value):
        const = obj._fconst[self.index]
        if const is False:
             offset=obj._offsets[self.index]
             ftype=obj._ftypes[self.index]
             fsize=obj._fsizes[self.index]
             length=obj._flength[self.index]
             obj._buffer.set_field(offset,ftype,fsize,length,value)
             if self.setter is not None:
                 self.setter(obj)
    def __get__(self,obj,cls=None):
        if obj is None:
            return self
        else:
            return self._field_getter(obj)
    def __set__(self,obj,value):
        return self._field_setter(obj,value)
    def __repr__(self):
        return str((self.index,self.ftype,self.length))

