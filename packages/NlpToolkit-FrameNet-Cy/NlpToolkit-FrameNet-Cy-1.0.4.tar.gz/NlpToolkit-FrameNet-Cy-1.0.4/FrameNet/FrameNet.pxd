from FrameNet.Frame cimport Frame


cdef class FrameNet:

    cdef list frames

    cpdef bint lexicalUnitExists(self, str synSetId)
    cpdef list getFrames(self, str synSetId)
    cpdef int size(self)
    cpdef Frame getFrame(self, int index)
