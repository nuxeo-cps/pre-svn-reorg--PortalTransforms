"""
Transform DocBook XML to HTML through XSL
"""
# $Id$

from Products.PortalTransforms.interfaces import itransform
from Products.PortalTransforms.libtransforms.utils import bin_search, basename, sansext
from Products.PortalTransforms.libtransforms.commandtransform import commandtransform
import os
from zLOG import LOG, DEBUG, WARNING

class ooo_to_docbook(commandtransform):
    __implements__ = itransform

    __name__ = "ooo_to_docbook"
    inputs   = ('application/vnd.sun.xml.writer',)
    output  = 'application/docbook+xml'

    binaryName = os.path.join(
        os.getcwd(), os.path.dirname(__file__), './ooo2dbk/ooo2dbk.py')

    def __init__(self):
        commandtransform.__init__(self, binary=self.binaryName)

    def convert(self, data, cache, **kwargs):
        kwargs['filename'] = basename((kwargs.get('filename') or 'unknown.sxw'))

        tmpdir, fullname = self.initialize_tmpdir(data, **kwargs)
        generated_file_data = self.invokeCommand(tmpdir, fullname)
        path, images = self.subObjects(tmpdir)
        objects = {}
        if images:
            self.fixImages(path, images, objects)
        self.cleanDir(tmpdir)
        cache.setData(generated_file_data)
        cache.setSubObjects(objects)
        return cache

    def invokeCommand(self, tmpdir, fullname):
        cmd = ('cd "%s" && %s --dbkfile %s.docb %s '
            '2>"%s.log-xsltproc"') % (
            tmpdir, self.binary, sansext(fullname), fullname, sansext(fullname))
        LOG(self.__name__, DEBUG, "cmd = %s" % cmd)
        os.system(cmd)
        try:
            generated_file = open("%s/%s.docb" % (tmpdir, sansext(fullname)), 'r')
            generated_file_data = generated_file.read()
            generated_file.close()
        except:
            try:
                return open("%s/error_log" % tmpdir, 'r').read()
            except:
                return ''
        return generated_file_data

def register():
    return ooo_to_docbook()
