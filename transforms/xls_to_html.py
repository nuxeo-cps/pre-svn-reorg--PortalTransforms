# -*- coding: iso-8859-15 -*-
# (C) Copyright 2004 Nuxeo SARL <http://nuxeo.com>
# Author: Stéfane Fermigier <sf@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id$

"""

"""
from Products.PortalTransforms.interfaces import itransform
from Products.PortalTransforms.libtransforms.utils import basename, sansext
from Products.PortalTransforms.libtransforms.commandtransform \
    import commandtransform
from os import system

class xls_to_html(commandtransform):
    __implements__ = itransform

    __name__ = "xls_to_html"
    inputs = ('application/vnd.ms-excel',)
    output = 'text/html'

    binaryName = "xlhtml"
    binaryArgs = "-nh -a"

    def __init__(self):
        commandtransform.__init__(self, binary=self.binaryName)

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
        # FIXME: windows users...
        basename = sansext(fullname)
        cmd = 'cd "%s" && %s %s "%s" 1> "%s.html" 2>error_log' % (
            tmpdir, self.binary, self.binaryArgs, fullname, basename)
        system(cmd)
        try:
            htmlfile = open("%s/%s.html" % (tmpdir, basename), 'r')
            html = htmlfile.read()
            htmlfile.close()
        except:
            try:
                return open("%s/error_log" % tmpdir, 'r').read()
            except:
                return ''
        return html

def register():
    return xls_to_html()
