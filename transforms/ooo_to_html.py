"""

"""
from Products.PortalTransforms.interfaces import itransform
from Products.PortalTransforms.libtransforms.utils \
    import basename, sansext
from Products.PortalTransforms.libtransforms.commandtransform \
    import commandtransform
import os

XSL_STYLESHEET = os.path.join(
  os.getcwd(), os.path.dirname(__file__), './sx2ml/main_html.xsl')

class ooo_to_html(commandtransform):
    __implements__ = itransform

    __name__ = "ooo_to_html"
    inputs = ('application/vnd.sun.xml.writer',
              'application/vnd.sun.xml.impress', 
              'application/vnd.sun.xml.calc')
    output = 'text/html'

    #binaryName = "pdftohtml"
    #binaryArgs = "-noframes"

    #def __init__(self):
    #    commandtransform.__init__(self, binary=self.binaryName)

    def convert(self, data, cache, **kwargs):
        kwargs['filename'] = basename((kwargs.get('filename') or 'unknown.pdf'))

        tmpdir, fullname = self.initialize_tmpdir(data, **kwargs)
        html = self.invokeCommand(tmpdir, fullname)
        path, images = self.subObjects(tmpdir)
        objects = {}
        if images:
            self.fixImages(path, images, objects)
        self.cleanDir(tmpdir)
        cache.setData(html)
        cache.setSubObjects(objects)
        return cache

    def invokeCommand(self, tmpdir, fullname):
        cmd = 'cd "%s" && unzip %s 2>error_log 1>/dev/null' % (
            tmpdir, fullname)
        os.system(cmd)
        cmd = ('cd "%s" && xsltproc --novalid %s content.xml >"%s.html" '
            '2>"%s.log-xsltproc"') % (
            tmpdir, XSL_STYLESHEET, sansext(fullname), sansext(fullname))
        os.system(cmd)
        try:
            htmlfile = open("%s/%s.html" % (tmpdir, sansext(fullname)), 'r')
            html = htmlfile.read()
            htmlfile.close()
        except:
            try:
                return open("%s/error_log" % tmpdir, 'r').read()
            except:
                return ''
        return html

def register():
    return ooo_to_html()
