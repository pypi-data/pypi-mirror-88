cdef class Frame:

    def __init__(self, name: str):
        self.lexicalUnits = []
        self.frameElements = []
        self.name = name

    cpdef addLexicalUnit(self, str lexicalUnit):
        self.lexicalUnits.append(lexicalUnit)

    cpdef addFrameElement(self, str frameElement):
        self.frameElements.append(frameElement)

    cpdef bint lexicalUnitExists(self, str synSetId):
        return synSetId in self.lexicalUnits

    cpdef str getLexicalUnit(self, int index):
        return self.lexicalUnits[index]

    cpdef str getFrameElement(self, int index):
        return self.frameElements[index]

    cpdef int lexicalUnitSize(self):
        return len(self.lexicalUnits)

    cpdef int frameElementSize(self):
        return len(self.frameElements)

    cpdef str getName(self):
        return self.name
