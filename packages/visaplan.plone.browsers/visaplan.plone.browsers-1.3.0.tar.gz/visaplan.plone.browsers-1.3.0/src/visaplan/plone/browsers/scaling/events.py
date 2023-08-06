# Python compatibility:
from __future__ import absolute_import

# Standard library:
import glob
from os import unlink
from os.path import exists


def delete(self,event):
    """ """
    context=event.object
    storagepath=context.getBrowser('scaling')._storage_path()

    if hasattr(context,'UID') and context.UID():
        for path in glob.glob(storagepath+context.UID()+'*'):
            if exists(path):
                unlink(path)
