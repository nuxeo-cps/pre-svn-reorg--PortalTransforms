import os
from Products.PortalTransforms.libtransforms.utils \
    import bodyfinder, scrubHTML
from Products.PortalTransforms.libtransforms.commandtransform \
    import commandtransform

ENCODING = "iso-8859-15"

class document(commandtransform):

    def __init__(self, name, data):
        """ Initialization: create tmp work directory and copy the
        document into a file"""
        commandtransform.__init__(self, name, binary="wvHtml")
        name = self.name()
        if not name.endswith('.doc'):
            name = name + ".doc"
        self.tmpdir, self.fullname = self.initialize_tmpdir(data, filename=name)

    def convert(self, output_encoding=ENCODING):
        "Convert the document"
        tmpdir = self.tmpdir
        cmd = 'cd "%s" && %s --charset=%s "%s" "%s.html"' % (
                                                      tmpdir,
                                                      self.binary,
                                                      output_encoding,
                                                      self.fullname,
                                                      self.__name__)
        os.system(cmd)

    def html(self):
        htmlfile = open("%s/%s.html" % (self.tmpdir, self.__name__), 'r')
        html = htmlfile.read()
        htmlfile.close()
        html = scrubHTML(html)
        body = bodyfinder(html)
        return body
