"""
Transform OOo OpenDocument file to HTML through XSL
"""
# $Id: opendocument_to_html.py 30141 2005-11-30 15:54:35Z lgodard $
import os
import sys

from Products.PortalTransforms.interfaces import itransform
from Products.PortalTransforms.libtransforms.utils \
    import basename, sansext
from Products.PortalTransforms.libtransforms.commandtransform \
    import commandtransform
from zLOG import LOG, DEBUG, WARNING

XSL_STYLESHEET_TRANSFORM = os.path.join(
  os.getcwd(), os.path.dirname(__file__), 'od2ml', 'document2xhtml.xsl')

class opendocument_to_html(commandtransform):
    __implements__ = itransform

    __name__ = 'opendocument_to_html'
    inputs = ('application/vnd.oasis.opendocument.text',
              'application/vnd.oasis.opendocument.text-template',
             # 'application/vnd.oasis.opendocument.spreadsheet',
             # 'application/vnd.oasis.opendocument.spreadsheet-template',
             # 'application/vnd.oasis.opendocument.presentation',
             # 'application/vnd.oasis.opendocument.presentation-template',
             # 'application/vnd.oasis.opendocument.graphics',
             # 'application/vnd.oasis.opendocument.graphics-template',
              )
    output = 'text/html'

    def convert(self, data, cache, **kwargs):
        kwargs['filename'] = basename((kwargs.get('filename') or 'unknown.pdf'))

        tmpdir, fullname = self.initialize_tmpdir(data, **kwargs)
        html = self.invokeCommand(tmpdir, fullname)

        subObjectsPaths = [tmpdir, os.path.join(tmpdir, 'Pictures')]
        for subObjectsPath in subObjectsPaths:
            if os.path.exists(subObjectsPath):
                path, images = self.subObjects(subObjectsPath)
                objects = {}
                if images:
                    self.fixImages(path, images, objects)

        self.cleanDir(tmpdir)
        cache.setData(html)
        cache.setSubObjects(objects)
        return cache

    def invokeCommand(self, tmpdir, fullname):
        if sys.platform == 'win32':
            cmd = 'unzip %s -d %s' % (fullname, tmpdir)
        else:
            cmd = 'cd "%s" && unzip %s 2>error_log 1>/dev/null' % (
                tmpdir, fullname)
        os.system(cmd)
        
        #process transform
        if sys.platform == 'win32':
            cmd = 'xsltproc --novalid "%s" "%s" > "%s"' % (
                XSL_STYLESHEET_TRANSFORM,
                os.path.join(tmpdir, 'content.xml'),
                os.path.join(tmpdir, sansext(fullname)+'.html'))
        else:
            cmd = ('cd "%s" && xsltproc --novalid %s content.xml >"%s.html" '
                   '2>"%s.log-xsltproc"') % (
                                            tmpdir, 
                                            XSL_STYLESHEET_TRANSFORM, 
                                            sansext(fullname),
                                            sansext(fullname)
                                            )
        LOG(self.__name__, DEBUG, "cmd = %s" % cmd)
        os.system(cmd)
        
        try:
            htmlfile = open(os.path.join(tmpdir, "%s.html" % sansext(fullname)),
                            'r')
            html = htmlfile.read()
            htmlfile.close()
        except:
            try:
                return open(os.path.join(tmpdir, 'error_log'), 'r').read()
            except:
                return ''
        return html

def register():
    return opendocument_to_html()
