"""
Transform DocBook XML to HTML through XSL
"""
# $Id$

from Products.PortalTransforms.interfaces import itransform
from Products.PortalTransforms.libtransforms.utils import bin_search, basename, sansext
from Products.PortalTransforms.libtransforms.commandtransform import commandtransform
import os
from zLOG import LOG, DEBUG, WARNING

XSL_STYLESHEET = os.path.join(
    os.getcwd(), os.path.dirname(__file__), './docbook/xhtml/docbook.xsl')

class docbook_to_html(commandtransform):
    __implements__ = itransform

    __name__ = "docbook_to_html"
    inputs   = ('application/docbook+xml',)
    output  = 'text/html'

    binaryName = "xsltproc"

    def __init__(self):
        commandtransform.__init__(self, binary=self.binaryName)

    def convert(self, data, cache, **kwargs):
        kwargs['filename'] = basename((kwargs.get('filename') or 'unknown.docb.xml'))

        tmpdir, fullname = self.initialize_tmpdir(data, **kwargs)

        subfiles_dict = kwargs.get('subobjects', {})
        for k, v in subfiles_dict.items():
            subfile_name = k
            tmp_image_dir_path = os.path.join(tmpdir, 'images')
            if not os.path.exists(tmp_image_dir_path):
                os.mkdir(tmp_image_dir_path)
            subfile_path = os.path.join(tmp_image_dir_path, subfile_name)
            subfile = open(subfile_path, 'w+c')
            subfile.write(str(v))

        html = self.invokeCommand(tmpdir, fullname)
        html = html.replace('img src="images/', 'img src="')
        try:
            path, images = self.subObjects(os.path.join(tmpdir,
                                                        'images'))
        except OSError, e:
            LOG('docbook_to_html.convert', WARNING, 'OSError: %s' % e)
            path, images = '', []
        objects = {}
        if images:
            self.fixImages(path, images, objects)
        self.cleanDir(tmpdir)
        cache.setData(html)
        cache.setSubObjects(objects)
        return cache

    def invokeCommand(self, tmpdir, fullname):
        cmd = ('cd "%s" && %s --novalid %s %s >"%s.html" '
            '2>"%s.log-xsltproc"') % (
            tmpdir, self.binary, XSL_STYLESHEET, fullname, sansext(fullname),
            sansext(fullname))
        LOG(self.__name__, DEBUG, "cmd = %s" % cmd)
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
    return docbook_to_html()
