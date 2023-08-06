cdef class Frame:

    cdef str name
    cdef list lexicalUnits
    cdef list frameElements

    cpdef addLexicalUnit(self, str lexicalUnit)
    cpdef addFrameElement(self, str frameElement)
    cpdef bint lexicalUnitExists(self, str synSetId)
    cpdef str getLexicalUnit(self, int index)
    cpdef str getFrameElement(self, int index)
    cpdef int lexicalUnitSize(self)
    cpdef int frameElementSize(self)
    cpdef str getName(self)
