from Products.PortalTransforms.interfaces import iclassifier
from Products.PortalTransforms.MimeTypeItem import MimeTypeItem, \
     MimeTypeException

from types import InstanceType
import re

class text_plain(MimeTypeItem):

    __implements__ = MimeTypeItem.__implements__
    __name__   = "Plain Text"
    mimetypes  = ('text/plain',)
    extensions = ('txt',)
    binary     = 0

class text_structured(MimeTypeItem):

    __implements__ = MimeTypeItem.__implements__
    __name__   = "Structured Text"
    mimetypes  = ('text/structured',)
    extensions = ('stx',)
    binary     = 0

class text_rest(MimeTypeItem):

    __implements__ = MimeTypeItem.__implements__
    __name__   = "reST"
    mimetypes  = ("text/x-rst", "text/restructured",)
    extensions = ("rst", "rest", "restx") #txt?
    binary     = 0

class text_python(MimeTypeItem):

    __implements__ = MimeTypeItem.__implements__
    __name__   = "python"
    mimetypes  = ("text/python-source", "text/x-python",)
    extensions = ("py",)
    binary     = 0


class application_rtf(MimeTypeItem):

    __implements__ = MimeTypeItem.__implements__
    __name__   = 'rtf'
    mimetypes  = ('application/rtf',)
    extensions = ('rtf',)
    binary     = 1

class application_msword(MimeTypeItem):
    __implements__ = MimeTypeItem.__implements__
    __name__   = "Microsoft Word Document"
    mimetypes  = ('application/msword',)
    extensions = ('doc',)
    binary     = 1

class application_msexcel(MimeTypeItem):
    __implements__ = MimeTypeItem.__implements__
    __name__   = "Microsoft Excel Document"
    mimetypes  = ('application/vnd.ms-excel',)
    extensions = ('xls',)
    binary     = 1

class application_mspowerpoint(MimeTypeItem):
    __implements__ = MimeTypeItem.__implements__
    __name__   = "Microsoft PowerPoint Document"
    mimetypes  = ('application/vnd.ms-powerpoint',)
    extensions = ('ppt',)
    binary     = 1

class application_writer(MimeTypeItem):
    __implements__ = MimeTypeItem.__implements__
    __name__   = "OpenOffice.org Writer Document"
    mimetypes  = ('application/vnd.sun.xml.writer',)
    extensions = ('sxw',)
    binary     = 1

class application_impress(MimeTypeItem):
    __implements__ = MimeTypeItem.__implements__
    __name__   = "OpenOffice.org Impress Document"
    mimetypes  = ('application/vnd.sun.xml.impress',)
    extensions = ('sxi',)
    binary     = 1

class application_calc(MimeTypeItem):
    __implements__ = MimeTypeItem.__implements__
    __name__   = "OpenOffice.org Calc Document"
    mimetypes  = ('application/vnd.sun.xml.calc',)
    extensions = ('sxc',)
    binary     = 1

class text_xml(MimeTypeItem):

    __implements__ = MimeTypeItem.__implements__ + (iclassifier,)

    __name__   = "Extensible Markup Language"
    mimetypes  = ('text/xml',)
    extensions = ('xml',)
    binary     = 0

    def classify(self, data):
        m = re.search('<?xml.*?>', data)
        if m:
            return 1 # True
        return None  # False

class application_octet_stream(MimeTypeItem):
    """we need to be sure this one exists"""
    __name__   = "Octet Stream"
    mimetypes = ('application/octet-stream',)
    binary     = 1
    extensions = ()

# TODO: this list should be automagically computed ising introspection.
reg_types = [
    text_plain,
    application_msword,
    application_msexcel,
    application_mspowerpoint,
    application_writer,
    application_impress,
    application_calc,
    text_xml,
    text_structured,
    text_rest,
    text_python,
    application_octet_stream,
    application_rtf,
    ]

import mimetypes as pymimetypes

def initialize(registry):
    for mt in reg_types:
        if type(mt) != InstanceType:
            mt = mt()
        registry.register(mt)

    #Find things that are not in the specially registered mimetypes
    #and add them using some default policy, none of these will impl
    #iclassifier
    for ext, mt in pymimetypes.types_map.items():
        if ext[0] == '.':
            ext = ext[1:]
        try:
            mto =  registry.lookup(mt)
        except MimeTypeException:
            # malformed MIME type
            continue
        if mto:
            mto = mto[0]
            if not ext in mto.extensions:
                registry.register_extension(ext, mto)
                mto.extensions += (ext, )
            continue
        isBin = mt.split('/', 1)[0] != "text"
        registry.register(MimeTypeItem(mt, (mt,), (ext,), isBin))
