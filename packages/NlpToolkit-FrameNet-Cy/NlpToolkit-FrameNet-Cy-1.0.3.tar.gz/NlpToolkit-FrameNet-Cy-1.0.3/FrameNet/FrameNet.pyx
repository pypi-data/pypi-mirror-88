import os
import xml.etree.ElementTree


cdef class FrameNet:

    def __init__(self):
        self.frames = []
        root = xml.etree.ElementTree.parse("../framenet.xml").getroot()
        for frameNode in root:
            frame = Frame(frameNode.attrib["NAME"])
            for childNode in frameNode:
                if childNode.tag == "LEXICAL_UNITS":
                    for lexicalUnit in childNode:
                        frame.addLexicalUnit(lexicalUnit.text)
                elif childNode.tag == "FRAME_ELEMENTS":
                    for frameElement in childNode:
                        frame.addFrameElement(frameElement.text)
            self.frames.append(frame)

    cpdef bint lexicalUnitExists(self, str synSetId):
        cdef Frame frame
        for frame in self.frames:
            if frame.lexicalUnitExists(synSetId):
                return True
        return False

    cpdef list getFrames(self, str synSetId):
        cdef list result
        cdef Frame frame
        result = []
        for frame in self.frames:
            if frame.lexicalUnitExists(synSetId):
                result.append(frame)
        return result

    cpdef int size(self):
        return len(self.frames)

    cpdef Frame getFrame(self, int index):
        return self.frames[index]
